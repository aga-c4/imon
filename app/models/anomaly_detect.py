"""
Description:
    Механизм обнаружения аномалий в сезонном одномерном временном ряду 
    (univariate time series), состоящем из пар timestamp, count

Usage:
    anomaly_detect(x, max_anoms=0.1, direction="pos", alpha=0.05, 
                        only_last=None, threshold="None", e_value=False, 
                        longterm=False, piecewise_median_period_weeks=2,
                        y_log=False, verbose=False)

Arguments:

        x: Временной ряд в виде data frame с двумя столбцами, первый из 
            которых - это временные метки, второй - наблюдаемые значения

max_anoms: Максимальное количество аномалий, которые S-H-ESD выявит 
            в процентах от данных.

direction: Варианты детектируемых аномалий. 
            Варианты: "pos" | "neg" | "both".

direction_reverce: Если True, то в выдаче pos и neg аномалии поменяются местами                     

    alpha: Уровень статистической значимости, с которого фиксируются или
            отклоняются аномалии.

only_last: Находить аномалии и сообщать о них только в течение последнего 
            дня или часа в временном ряду. 
            Варианты: None | "day" | "hr".

threshold: Сообщать только о положительно идущих значениях, выходящих 
            за пределы указанного порогового значения. 
            Варианты: None | "med_max" | "p95" | "p99".
            Фильтрует все негативные аномалии и те аномалии, 
            величина которых меньше одного из указанных пороговых значений
            которые включают в себя: медиану ежедневных максимальных значений (med_max),
            95-й процентиль ежедневных максимальных значений (p95) и 99-й
            процентиль ежедневных максимальных значений (p99).

  e_value: Добавить дополнительный столбец к выходным данным anoms, содержащий
            ожидаемое значение.

 longterm: повышает эффективность обнаружения аномалий для временных рядов
            продолжительностью более месяца. Подробности в Details. Эта опция 
            должна быть установлена, когда входящий временной ряд больше месяца. 
            Эта опция позволяет использовать подход описаный в Vallis, Hochenbaum, 
            and Kejariwal (2014).

 piecewise_median_period_weeks: Кусочно-медианное временное окно (The 
            piecewise median time window), как описано в 
            Vallis, Hochenbaum, and Kejariwal (2014).
            Значение по умолчанию равно 2.

    y_log: Примените логарифмическое масштабирование к оси y. Это помогает при просмотре
            графиков, которые имеют чрезвычайно большие положительные аномалии относительно
            остальных данных.

  verbose: Включить отладочные сообщения
 
  resampling: должна ли granularity в миллисекундах или секундах быть изменена на минимальную. 
              Значение по умолчанию равно False.
             
  period_override: Переопределение автоматически сгенерированного периода (1440)
                    Значение по умолчанию равно None
                    

Value:

    Возвращаемое значение представляет собой список со следующими компонентами.

    anoms: Data frame, содержащий index, values, и опционально ожидаемые значения.

    Можно сохранить "anoms" в файл следующим образом:
    write.csv(<return list name>[["anoms"]], file=<filename>)

References:

     Vallis, O., Hochenbaum, J. and Kejariwal, A., (2014) "A Novel
     Technique for Long-Term Anomaly Detection in the Cloud", 6th
     USENIX, Philadelphia, PA.

     Rosner, B., (May 1983), "Percentage Points for a Generalized ESD
     Many-Outlier Procedure" , Technometrics, 25(2), pp. 165-172.    

Examples:
    from models.anomaly_detect import anomaly_detect
    # Для поиска всех аномалий только в последнем дне:
    anomaly_detect(raw_data, max_anoms=0.02, direction="both", only_last="day")
    # Для поиска аномалий только в последнем часе с приведением времени (ms, sec) к минимальной гранулярности:
    anomaly_detect(raw_data, max_anoms=0.02, direction="both", only_last="hr" resampling=True)
    # Для поиска аномалий только в последнем часе с переопределением периода на 1440
    anomaly_detect(raw_data, max_anoms=0.02, direction="both", only_last="hr", period_override=1440)
"""

import numpy as np
import scipy as sp
import pandas as pd
import datetime
import statsmodels.api as sm
import logging

logger = logging.getLogger(__name__)

def _handle_granularity_error(level):
    """
    Выдает ValueError с подробным сообщением об ошибке, если вычисленная степень 
    детализации (granularity) меньше минуты (sec or ms) и не активирован resampling.

      level : String
        granularity, которая менее минимальной для выдачи в сообщении
    """
    e_message = f"{level} granularity is not supported. Ensure granularity => minute or enable resampling"
    raise ValueError(e_message)

def _resample_to_min(data, period_override=None):
    """
    Приведение набора данных к минимально возможной детализации (granularity)

      data : pandas DataFrame
        входящий Pandas DataFrame
      period_override : int
        indicates whether resampling should be done with overridden value instead of min (1440)

    """
    data = data.resample('60s', label='right').sum()
    if _override_period(period_override):
        period = period_override
    else:
        period = 1440
    return (data, period)


def _override_period(period_override):
    """
    Показывает может ли период быть переопределен, если период, 
    полученный на основе детализации (granularity), не соответствует 
    сгенерированному периоду.

      period_override : int
        указанный пользователем период, который переопределяет значение, 
        рассчитанное на основе детализации (granularity).
    """
    return period_override is not None


def _get_period(gran_period, period_arg=None):
    """
    Возвращает сгенерированный период или переопределенный period 
    в зависимости от параметра period_arg
      gran_period : int
        период, сгенерированный на основе детализации (granularity)
      period_arg : значение переопределяющее период, которое равно 
        либо None, либо int - период для переопределения периода, 
        сгенерированного на основе детализации.
    """
    if _override_period(period_arg):
        return period_arg
    else:
        return gran_period


def _get_data_tuple(raw_data, period_override, resampling=False):
    """
    Генерирует кортеж, состоящий из обработанных входных данных, 
    вычисленного или переопределенного периода и степени детализации (granularity)
      raw_data : pandas DataFrame
        входные данные
      period_override : int
        период, указанный в списке параметров anomaly_detect_ts, None, если он не указан
      resampling : True | False
        указывает, следует ли повторно выполнить выборку данных raw_data 
        с поддерживающейся степенью детализации (granularity), если это применимо
    """
    data = raw_data.sort_index()
    timediff = _get_time_diff(data)

    if timediff.days > 0:
        period = _get_period(7, period_override)
        granularity = 'day'
    elif timediff.seconds / 60 / 60 >= 1:
        granularity = 'hr'
        period = _get_period(24, period_override)
    elif timediff.seconds / 60 >= 1:
        granularity = 'min'
        period = _get_period(1440, period_override)
    elif timediff.seconds > 0:
        granularity = 'sec'
    elif timediff.seconds > 0:
        granularity = 'sec'
        '''
            Агрегирует данные с минутной детализацией (granularity), 
            если детализация потока данных равна sec и resampling=True.
            Если resampling=False, то будет вызван ValueError
        '''
        if resampling is True:
            period = _resample_to_min(data, period_override)
        else:
            _handle_granularity_error('sec')
    else:
        '''
            Агрегирует данные с минутной детализацией (granularity), 
            если детализация потока данных равна ms и resampling=True.
            Если resampling=False, то будет вызван ValueError
        '''
        if resampling is True:
            data, period = _resample_to_min(data, period_override)
            granularity = None
        else:
            _handle_granularity_error('ms')

    return (data, period, granularity)


def _get_time_diff(data):
    """
    Возвращает разницу во времени, используемую для определения степени 
    детализации (granularity) и для создания периода (period)

      data : pandas DataFrame
        состоит из входных данных
    """
    return data.index[1] - data.index[0]


def _get_max_anoms(data, max_anoms):
    """
    Проверяет, подготавливает и возвращает параметр max_anoms, 
    используемый для обнаружения аномалий временных рядов S-H-ESD

      data : pandas DataFrame
        состоит из входных данных
      max_anoms : float
        значение max_anoms
    """
    if max_anoms == 0:
        logger.warning('0 max_anoms results in max_outliers being 0.')
    return 1 / data.size if max_anoms < 1 / data.size else max_anoms


def _process_long_term_data(data, period, granularity, piecewise_median_period_weeks):
    """
    Обрабатывает результирующий набор. Вызывается, если для параметра 
    long term установлено значение true

      data : list of floats
        результирующий набор аномалий
      period : int
        вычисленное или переопределенное значение периода
      granularity : string
        вычисленная или переопределенная степень детализации (granularity)
      piecewise_median_period_weeks : int
        используется для определения дней и наблюдений за период
    """

    # Предварительно выделяет список размером, равным количеству фрагментов 
    # piecewise_median_period_weeks в x + любой оставшийся фрагмент.
    # Обработка крайних случаев для ежедневных данных и данных в одном столбце
    num_obs_in_period = period * piecewise_median_period_weeks + \
        1 if granularity == 'day' else period * 7 * piecewise_median_period_weeks
    num_days_in_period = (7 * piecewise_median_period_weeks) + \
        1 if granularity == 'day' else (7 * piecewise_median_period_weeks)

    all_data = []
    # Подмножество х в piecewise_median_period_weeks фрагментах
    for i in range(1, data.size + 1, num_obs_in_period):
        start_date = data.index[i]
        # если осталось хотя бы 14 дней, донаберите его, в противном случае 
        # подмножество last_date - 14 дней
        end_date = start_date + datetime.timedelta(days=num_days_in_period)
        if end_date < data.index[-1]:
            all_data.append(data.loc[lambda x: (x.index >= start_date) & (x.index <= end_date)])
            # all_data = pd.concat([all_data, data.loc[lambda x: (x.index >= start_date) & (x.index <= end_date)]]) # AGA-C4: ранее так фиксил, теперь так не пашет
        else:
            all_data.append(data.loc[lambda x: x.index >= data.index[-1] - datetime.timedelta(days=num_days_in_period)])
            # all_data = pd.concat([all_data, data.loc[lambda x: x.index >= data.index[-1] - datetime.timedelta(days=num_days_in_period)]]) # AGA-C4: ранее так фиксил, теперь так не пашет
    return all_data


def _get_only_last_results(data, all_anoms, granularity, only_last):
    """
    Возвращает результаты только за последний день или час

      data : pandas DataFrame
        набор входных данных
      all_anoms : list of floats
        все аномалии, возвращаемые алгоритмом
      granularity : string day | hr | min
        поддерживаемый уровень детализации (granularity)
      only_last : string day | hr
        Конечный период, подмножество аномалий которого будет возвращено
    """
    start_date = data.index[-1] - datetime.timedelta(days=7)
    start_anoms = data.index[-1] - datetime.timedelta(days=1)

    if only_last == 'hr':
        # Нам нужно изменить start_date и start_anoms для часового параметра only_last
        start_date = datetime.datetime.combine(
            (data.index[-1] - datetime.timedelta(days=2)).date(), datetime.time.min)
        start_anoms = data.index[-1] - datetime.timedelta(hours=1)

    # подмножество данных за последние дни
    x_subset_single_day = data.loc[data.index > start_anoms]
    # При построении графика аномалий за последний день, мы показываем только 
    # предыдущие недельные данные
    x_subset_week = data.loc[lambda df: (
        df.index <= start_anoms) & (df.index > start_date)]
    return all_anoms.loc[all_anoms.index >= x_subset_single_day.index[0]]


def _perform_threshold_filter(anoms, periodic_max, threshold):
    """
    Фильтрует список аномалий в соответствии с пороговым (threshold) фильтром

      anoms : list of floats
        список аномалий, возвращенных алгоритмом
      periodic_max : float
        рассчитанное максимальное дневное значение
      threshold : med_max" | "p95" | "p99"
        заданное пользователем пороговое значение (threshold), используемое 
        для фильтрации отклонений
    """
    if threshold == 'med_max':
        thresh = periodic_max.median()
    elif threshold == 'p95':
        thresh = periodic_max.quantile(0.95)
    elif threshold == 'p99':
        thresh = periodic_max.quantile(0.99)
    else:
        raise AttributeError(
            'Invalid threshold, threshold options are None | med_max | p95 | p99')

    return anoms.loc[anoms.values >= thresh]


def _get_max_outliers(data, max_percent_anomalies):
    """
    Вычисляет значения max_outliers (макс_отклонения) для набора входных данных

      data : pandas DataFrame
        набор входных данных
      max_percent_anomalies : float
        входное максимальное количество аномалий в процентах от значений набора данных
    """
    max_outliers = int(np.trunc(data.size * max_percent_anomalies))
    assert max_outliers, 'With longterm=True, AnomalyDetection splits the data into 2 week periods by default. You have {0} observations in a period, which is too few. Set a higher piecewise_median_period_weeks.'.format(
        data.size)
    return max_outliers


def _get_decomposed_data_tuple(data, num_obs_per_period):
    """
    Возвращает кортеж, состоящий из двух версий входного набора данных: 
    с разбивкой по сезонам (seasonally-decomposed) и сглаженной (smoothed)

      data : pandas DataFrame
        набор входных данных
      num_obs_per_period : int
        количество наблюдений в каждом периоде
    """

    # Декомпозиция данных возвращает одномерный остаток, который будет использоваться для 
    # обнаружения аномалий. При желании мы можем не проводить декомпозицию.
    # Внимание!: R использует stl, в данной реализации используется MA, что может повлиять на результат
    decomposed = sm.tsa.seasonal_decompose(data, period=num_obs_per_period, two_sided=False) # AGA-C4: Ранее вместо period использовали freeze
    smoothed = data - decomposed.resid.fillna(0)
    data = data - decomposed.seasonal - data.mean()
    return (data, smoothed)


def anomaly_detect(x, max_anoms=0.1, direction="both", direction_reverce=False, alpha=0.05, only_last=None,
                      threshold=None, e_value=False, longterm=False, piecewise_median_period_weeks=2,
                      y_log=False, verbose=False, resampling=False, period_override=None):

    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("The debug logs will be logged because verbose=%s", verbose)

    # validation
    assert isinstance(x, pd.Series), 'Data must be a series(Pandas.Series)'
    assert x.values.dtype in [int, float], 'Values of the series must be number'
    # print("x.index.dtype:", str(x.index.dtype))
    assert str(x.index.dtype).startswith("datetime64[ns"), 'Index of the series must be datetime'
    # assert x.index.dtype == np.dtype('datetime64[ns]'), 'Index of the series must be datetime'
    assert max_anoms <= 0.49 and max_anoms >= 0, 'max_anoms must be non-negative and less than 50% '
    assert direction in ['pos', 'neg', 'both'], 'direction options: pos | neg | both'
    assert only_last in [None, 'day', 'hr'], 'only_last options: None | day | hr'
    assert threshold in [None, 'med_max', 'p95', 'p99'], 'threshold options: None | med_max | p95 | p99'
    assert piecewise_median_period_weeks >= 2, 'piecewise_median_period_weeks must be greater than 2 weeks'
    logger.debug('Completed validation of input parameters')

    if alpha < 0.01 or alpha > 0.1:
        logger.warning('alpha is the statistical significance and is usually between 0.01 and 0.1')

    data, period, granularity = _get_data_tuple(x, period_override, resampling)
    if granularity == 'day':
        num_days_per_line = 7
        only_last = 'day' if only_last == 'hr' else only_last

    max_anoms = _get_max_anoms(data, max_anoms)

    # Если  longterm=True, разбить данные на подмножества фреймов данных и сохранить в all_data
    all_data = _process_long_term_data(data, period, granularity, piecewise_median_period_weeks) if longterm else [data] 
    all_anoms = pd.Series()
    all_anoms_pos = pd.Series()
    all_anoms_neg = pd.Series()

    seasonal_plus_trend = pd.Series()

    # Обнаруживать аномалии во всех данных (либо все данные за один проход, либо за 2-недельные блоки, если longterm=True)
    for series in all_data:
        shesd = _detect_anoms_upd(series, k=max_anoms, alpha=alpha, num_obs_per_period=period, direction=direction, verbose=verbose)
        shesd_anoms = shesd['anoms']
        shesd_anoms_pos = shesd['anoms_pos']
        shesd_anoms_neg = shesd['anoms_neg']
        shesd_stl = shesd['stl']

        # Использует временные метки (timestamps) обнаруженных аномалий для извлечения фактических аномалий (timestamp и value) из данных
        anoms = pd.Series() if shesd_anoms.empty else series.loc[shesd_anoms.index]
        anoms_pos = pd.Series() if shesd_anoms_pos.empty else series.loc[shesd_anoms_pos.index]
        anoms_neg = pd.Series() if shesd_anoms_neg.empty else series.loc[shesd_anoms_neg.index]

        # Фильтрует аномалии, используя одну из пороговых функций, если это применимо
        if threshold:
            # Рассчитывает дневные максимальные значения
            periodic_max = data.resample('1D').max()
            anoms = _perform_threshold_filter(anoms, periodic_max, threshold)
            anoms_pos = _perform_threshold_filter(anoms_pos, periodic_max, threshold)
            anoms_neg = _perform_threshold_filter(anoms_neg, periodic_max, threshold)

        all_anoms = pd.concat([all_anoms, anoms])
        all_anoms_pos = pd.concat([all_anoms_pos, anoms_pos])
        all_anoms_neg = pd.concat([all_anoms_neg, anoms_neg])
        seasonal_plus_trend = pd.concat([seasonal_plus_trend, shesd_stl])

    # De-dupe
    all_anoms.drop_duplicates(inplace=True)
    seasonal_plus_trend.drop_duplicates(inplace=True)

    # Если указано значение only_last, создает подмножество данных, соответствующее самому последнему дню или часу
    if only_last:
        all_anoms = _get_only_last_results(data, all_anoms, granularity, only_last)
        all_anoms_pos = _get_only_last_results(data, all_anoms_pos, granularity, only_last)
        all_anoms_neg = _get_only_last_results(data, all_anoms_neg, granularity, only_last)

    # Если аномалий нет, залогирует это и вернет пустой результат anoms
    if all_anoms.empty:
        if verbose:
            logger.info('No anomalies detected.')

        return {
            'anoms': pd.Series(),
            'anoms_pos': pd.Series(),
            'anoms_neg': pd.Series(),
            'expected': None
        }

    if not direction_reverce:
        return {
            'anoms': all_anoms,
            'anoms_pos': all_anoms_pos,
            'anoms_neg': all_anoms_neg,
            'expected': seasonal_plus_trend if e_value else None,
        }
    else:
        return {
            'anoms': all_anoms,
            'anoms_pos': all_anoms_neg,
            'anoms_neg': all_anoms_pos,
            'expected': seasonal_plus_trend if e_value else None,
        }


def _detect_anoms(data, k=0.49, alpha=0.05, num_obs_per_period=None, direction="pos", verbose=False):
    """
    Обнаруживает аномалии во временном ряду с использованием алгоритма S-H-ESD.

    Args:
         data: Временной ряд для поиска аномалий.
         k: Максимальное количество аномалий, которое S-H-ESD найдет в процентах от data.
         alpha: Уровень статистической значимости, для принятия или отклонения аномалий.
         num_obs_per_period: Определяет количество наблюдений в одном периоде и используется 
                             при сезонной декомпозиции. 
         direction: Варианты детектируемых аномалий. Варианты: "pos" | "neg" | "both".
         verbose: Включить отладочные сообщения
    Returns:
       Список, содержащий аномалии (anoms) и компоненты декомпозиции (stl).
    """

    # Проверка
    assert num_obs_per_period, "must supply period length for time series decomposition"
    assert direction in ['pos', 'neg', 'both'], 'direction options: pos | neg | both'
    assert data.size >= num_obs_per_period * 2, 'Anomaly detection needs at least 2 periods worth of data'
    assert data[data.isnull()].empty, 'Data contains NA. We suggest replacing NA with interpolated values before detecting anomaly'
    
    # one_tail:  Если значение TRUE, то обнаруживаются только положительные или отрицательные аномалии, 
    # в зависимости от того, имеет ли upper_tail значение TRUE или FALSE.
    one_tail = True if direction in ['pos', 'neg'] else False

    # upper_tail: Если значение TRUE и one_tail=TRUE, то обнаруживаются только положительные аномалии (right-tailed). 
    # Если значение FALSE и one_tail=TRUE, то обнаруживаются только отрицательные аномалии (left-tailed).
    upper_tail = True if direction in ['pos', 'both'] else False

    data, smoothed = _get_decomposed_data_tuple(data, num_obs_per_period)
    n = data.size
    max_outliers = _get_max_outliers(data, k)
    R_idx = pd.Series()
    # Вычисляет тестовую статистику до тех пор, пока r=max_outliers не будут удалены из выборки
    for i in range(1, max_outliers + 1):
        if verbose:
            logger.info(i, '/', max_outliers, ' completed')

        mad = (data - data.mean()).abs().mean()
        if not mad:
            break

        if not one_tail:
            # В текущих условиях это direction=both
            ares = abs(data - data.median())
        elif upper_tail:
            # В текущих условиях это direction=pos
            ares = data - data.median()
        else:
            # В текущих условиях это direction=neg
            ares = data.median() - data

        ares = ares / mad
        tmp_anom_index = ares[ares.values == ares.max()].index
        cand = pd.Series(data.loc[tmp_anom_index], index=tmp_anom_index)
        data.drop(tmp_anom_index, inplace=True)

        # Вычисление критического значения.
        p = 1 - alpha / (n - i + 1) if one_tail else (1 - alpha / (2 * (n - i + 1)))
        t = sp.stats.t.ppf(p, n - i - 1)
        lam = t * (n - i) / np.sqrt((n - i - 1 + t ** 2) * (n - i + 1))
        if ares.max() > lam:
            R_idx = pd.concat([R_idx, cand])

    return {
        'anoms': R_idx,
        'anoms_pos': pd.Series(),
        'anoms_neg': pd.Series(),
        'stl': smoothed
    }

def _detect_anoms_upd(data, k=0.49, alpha=0.05, num_obs_per_period=None, direction="both", c=False, verbose=False):
    """
    Обнаруживает аномалии во временном ряду с использованием алгоритма S-H-ESD.

    Args:
        data: Временной ряд для поиска аномалий.
        k: Максимальное количество аномалий, которое S-H-ESD найдет в процентах от data.
        alpha: Уровень статистической значимости, для принятия или отклонения аномалий.
        num_obs_per_period: Определяет количество наблюдений в одном периоде и используется 
                            при сезонной декомпозиции. 
        direction: Варианты детектируемых аномалий. Варианты: "pos" | "neg" | "both".
        verbose: Включить отладочные сообщения
    Returns:
       Список, содержащий аномалии (anoms) и компоненты декомпозиции (stl).
    """

    # Проверка
    assert num_obs_per_period, "must supply period length for time series decomposition"
    assert direction in ['pos', 'neg', 'both'], 'direction options: pos | neg | both'
    assert data.size >= num_obs_per_period * 2, 'Anomaly detection needs at least 2 periods worth of data'
    assert data[data.isnull()].empty, 'Data contains NA. We suggest replacing NA with interpolated values before detecting anomaly'

    data, smoothed = _get_decomposed_data_tuple(data, num_obs_per_period)
    n = data.size
    max_outliers = _get_max_outliers(data, k)
    R_idx = pd.Series()
    R_idx_pos = pd.Series()
    R_idx_neg = pd.Series()
    # Ищет аномалии до тех пор, пока r=max_outliers не будут удалены из выборки
    for i in range(1, max_outliers + 1):
        if verbose:
            logger.info(i, '/', max_outliers, ' completed')

        mad = (data - data.mean()).abs().mean()
        if not mad:
            break  

        ares = data - data.median()    

        ares = ares / mad
        ares_max = ares.max()
        ares_min = ares.min()
        tmp_anom_index_max = ares[ares.values == ares_max].index
        tmp_anom_index_min = ares[ares.values == ares_min].index
        extrem_direction = ''
        if direction=='pos' or (direction=='both' and abs(ares_max)>=abs(ares_min)):
            tmp_anom_index = tmp_anom_index_max
            extrem_direction = 'pos'
        elif direction=='neg' or (direction=='both' and abs(ares_max)<abs(ares_min)):
            tmp_anom_index = tmp_anom_index_min
            extrem_direction = 'neg'
        cand = pd.Series(data.loc[tmp_anom_index], index=tmp_anom_index)
        data.drop(tmp_anom_index, inplace=True)

        # Вычисление критического значения.
        p = 1 - alpha / (2 * (n - i + 1))
        t = sp.stats.t.ppf(p, n - i - 1)
        lam = t * (n - i) / np.sqrt((n - i - 1 + t ** 2) * (n - i + 1))
        if (extrem_direction=='pos' and ares_max > lam):
            R_idx_pos = pd.concat([R_idx_pos, cand])
            R_idx = pd.concat([R_idx, cand])

        if (extrem_direction=='neg' and abs(ares_min) > lam):
            R_idx_neg = pd.concat([R_idx_neg, cand])
            R_idx = pd.concat([R_idx, cand])

    return {
        'anoms': R_idx,
        'anoms_pos': R_idx_pos,
        'anoms_neg': R_idx_neg,
        'stl': smoothed
    }

