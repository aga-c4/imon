#!/usr/bin/python3
# coding=utf-8

config = {
    "system": {
        "proc_ttl": 2 * 60 * 60, # Максимальное время жизни процесса 
        "message_dt_lag_sec": 7 * 24 * 60 * 60, # Отошлем сообщения о последней неповторяющейся аномалии в течении message_dt_lag_sec
        "timezone": "Europe/Moscow",
        "proc_path": "tmp/process",
    },
    "granularity_allow": ['m1', 'h1', 'd1', 'w1', 'mo1'], # Допустимые варианты granularity
    "granularity_list": { # Описание вариантов granularity
        "m1": {
            "api_group": "minute", 
            "sec": 60, # Секунд в таймфрейме
            "dblimit": 5, # Количество дней данных, хранимых в базе
            "days_before_max": 5, # Максимальное количество дней сбора данной метрики с API  
            "update_ts_lag": 30 * 60, # Время в секундах до текущего момента для метрик, которые мы будем апдейтить перед добавлением новых. При заборе первый результат не учитываем, т.к. он не полный. Делаем запас
            "get_item_lag_sec": 10 * 60, # Лаг в секундах после которого необходимо забрать очередной элемент метрики. Раскидал, чтоб не сильно мешали друг другу.
            "message_dt_lag_sec": 4 * 60 * 60}, # Отошлем сообщения о последней неповторяющейся аномалии в течении message_dt_lag_sec
        "h1": {
            "api_group": "hour", 
            "sec": 60 * 60, # Секунд в таймфрейме
            "dblimit": 3*30, # Количество дней данных, хранимых в базе
            "days_before_max": 83, # Максимальное количество дней сбора данной метрики с API  
            "update_ts_lag": 6 * 60 * 60, # Время в секундах до текущего момента для метрик, которые мы будем апдейтить перед добавлением новых. При заборе первый результат не учитываем, т.к. он не полный. Делаем запас
            "get_item_lag_sec": 60 * 60, # Лаг в секундах после которого необходимо забрать очередной элемент метрики. Раскидал, чтоб не сильно мешали друг другу.
            "message_dt_lag_sec": 24 * 60 * 60}, # Отошлем сообщения о последней неповторяющейся аномалии в течении message_dt_lag_sec
        "d1": {
            "api_group": "day", 
            "sec": 24 * 60 * 60, # Секунд в таймфрейме 
            "dblimit": 3*12*30, # Количество дней данных, хранимых в базе
            "days_before_max": 1000, # Максимальное количество дней сбора данной метрики с API  
            "update_ts_lag": 4 * 24 * 60 * 60, # Время в секундах до текущего момента для метрик, которые мы будем апдейтить перед добавлением новых. При заборе первый результат не учитываем, т.к. он не полный. Делаем запас
            "get_item_lag_sec": 4 * 60 * 60, # Лаг в секундах после которого необходимо забрать очередной элемент метрики. Раскидал, чтоб не сильно мешали друг другу.
            "message_dt_lag_sec": 2 * 24 * 60 * 60}, # Отошлем сообщения о последней неповторяющейся аномалии в течении message_dt_lag_sec
        "w1": {
            "api_group": "week", 
            "sec": 7 * 24 * 60 * 60, # Секунд в таймфрейме 
            "dblimit": 3*12*30, # Количество дней данных, хранимых в базе
            "days_before_max": 1000, # Максимальное количество дней сбора данной метрики с API  
            "update_ts_lag": 8 * 24 * 60 * 60, # Время в секундах до текущего момента для метрик, которые мы будем апдейтить перед добавлением новых. При заборе первый результат не учитываем, т.к. он не полный. Делаем запас
            "get_item_lag_sec": 5 * 60 * 60, # Лаг в секундах после которого необходимо забрать очередной элемент метрики. Раскидал, чтоб не сильно мешали друг другу.
            "message_dt_lag_sec": 8 * 24 * 60 * 60}, # Отошлем сообщения о последней неповторяющейся аномалии в течении message_dt_lag_sec
        "mo1": {
            "api_group": "month",
            "sec": 30 * 24 * 60 * 60, # Секунд в таймфрейме 
            "dblimit": 3*12*30, # Количество дней данных, хранимых в базе
            "days_before_max": 1000, # Максимальное количество дней сбора данной метрики с API  
            "update_ts_lag": 65 * 24 * 60 * 60, # Время в секундах до текущего момента для метрик, которые мы будем апдейтить перед добавлением новых. При заборе первый результат не учитываем, т.к. он не полный. Делаем запас
            "get_item_lag_sec": 6 * 60 * 60, # Лаг в секундах после которого необходимо забрать очередной элемент метрики. Раскидал, чтоб не сильно мешали друг другу.   
            "message_dt_lag_sec": 35 * 24 * 60 * 60}, # Отошлем сообщения о последней неповторяющейся аномалии в течении message_dt_lag_sec
    },
    "db": {    
        "host": "mysql",
        "port": 3306,
        "db": "imon",
        "user": "root",
        "passwd": "root",
        "timezone": "UTC"
    },
    "sources_allow": ["sysload"],
    "sources": {
        "metrica": {
            "id": 1,
            "counter_ids": "000000",
            "timezone": "Europe/Moscow",
            "token": "Разместите тут токен",
            "metrics_pkg_qty": 5,
            "source_get_api_lag_sec": 1,
            "sample_metric_ids": [],
            "tmp_path": "tmp/yamget"
        },    
        "app_metrica": {
            "id": 2,
            "counter_ids": "000000",
            "timezone": "Europe/Moscow",
            "token": "Разместите тут токен",
            "metrics_pkg_qty": 1,
            "source_get_api_lag_sec": 1,
            "sample_metric_ids": [],
            "tmp_path": "tmp/yamappget"
        },    
        "app_events": {
            "id": 3,
            "counter_ids": "000000",
            "timezone": "Europe/Moscow",
            "token": "Разместите тут токен",
            "metrics_pkg_qty": 5,
            "source_get_api_lag_sec": 1,
            "sample_metric_ids": [],
            "tmp_path": "tmp/yamappget"
        }, 
        "mysql1": {
            "id": 4,
            "metrics_pkg_qty": 1,
            "source_get_api_lag_sec": 1,
            "timezone": "Europe/Moscow",
            "tmp_path": "tmp/mysql1get",
            "db": {    
                "host": "",
                "port": 3306,
                "db": "",
                "user": "",
                "passwd": ""
            }
        },
        "sysload": {
            "id": 5,
            "api_url": "http://URL...",
            "timezone": "Europe/Moscow",
            "token": "testtoken",
            "source_get_api_lag_sec": 0,
            "tmp_path": "tmp/srcget",
            "insecure": False
        },        
    },
    "telegram": {
        0: { # Идентификатор проекта, 0 для проекта по умолчанию
            # Настройки по умолчанию, другие проекты могут переопределять часть настроек по умолчанию
            # Если channels переопределен, то необходимо указать ВСЕ каналы, или недостающие будут очищены
            "api_token": "",
            "channels": {
                "log": "",
                "error": "",
                "all": "",
                "important": "", 
                "critical": "",
                "news": ""
            }    
        }
    },
    "message_str": {
        "msg_link": { # Варианты ссылок по проектам, ключ - идентификатор проекта (строка)
            "default": " <a href='http://.../all-metrics?orgId=1&var-metric_id={msg_metric_id}&var-granularity={msg_granularity}'>Подробнее</a>",
            "1": " <a href='http://.../site-metrics?orgId=1&var-metric_id={msg_metric_id}&var-granularity={msg_granularity}'>Подробнее</a>",
            "2": " <a href='http://.../app-metrics?orgId=1&var-metric_id={msg_metric_id}&var-granularity={msg_granularity}'>Подробнее</a>"
        },
        "msg_anom_pos": "{metric_name}: Превышение нормы!",
        "msg_anom_neg": "{metric_name}: Ниже нормы!",
        "msg_anom_all": "{metric_name}: Аномальное значение!"
    },

    # Пример настройки новостей
    "newsmaker": {
        "gm_digest_d1": {
            "active": True,
            "title": "===[ ⏰ Good morning DIGEST ]===",
            "bottom": "===[ End of the Morning DIGEST ]===",
            "group": "digest",
            "message_lvl": "news",
            "device_alias": "", 
            "trafsrc_alias": "",
            "granularity": "d1", # Грануляция отчета, от нее зависят ряд параметров
            "dt_to": "2024-10-01 00:00:00", # Дата от которой строится отчет, может быть текущая current или строка даты-времени с таймзоной
            "dt_delta_fr": { # На сколько единиц времени назад начнется отчет, учитывается только одно наибольшее отклонение, значение 0 - не учитывается. Отсчет ведется от первой секунды начала текущего периода
                "month": 0,
                "days": 15,
                "hours": 0
            },    
            "messages": [
                {
                    "title": "Воронка САЙТА",
                    "type": "funnel",
                    "granularity": "d1",
                    "dt_delta_fr": { 
                        "days": 1
                    },  
                    "metric_ids": [2, 7, 41, 21, 23],
                    "metric_title": ["Сессии", "Просмотр товара", "Добавили в корзину", "Начало оформления заказа", "Успешный заказ"]
                },
                {
                    "title": "Пользователи САЙТА",
                    "type": "stack",
                    "metric_ids": [201,200], 
                    "metric_title": ["Вернувшиеся", "Новые"]
                },
                {
                    "title": "Сессии и пользователи САЙТА",
                    "type": "trace",
                    "metric_ids": [2,1], 
                    "metric_title": ["Сессии","Пользователи"]
                },
                {
                    "title": "Сессии по источникам САЙТА - сессии",
                    "type": "stack",
                    "metric_ids": [442, 452, 422, 472, 492, 502, 512], 
                    "metric_title": ["Google", "Yandex", "Adv", "Direct", "Referral", "Email", "Social"]
                },
                {
                    "title": "Заказы САЙТА",
                    "type": "trace",
                    "metric_ids": [23], 
                    "metric_title": ["Заказы"]
                },
                {
                    "title": "Полнота передачи заказов САЙТА",
                    "type": "trace",
                    "metric_ids": [181], 
                    "metric_title": ["Полнота передачи, %"]
                },
                {
                    "title": "Воронка ПРИЛОЖЕНИЯ",
                    "type": "funnel",
                    "metric_ids": [86, 151, 96, 102, 124],
                    "metric_title": ["Сессии", "Просмотр товара", "Добавили в корзину", "Начало оформления заказа", "Успешный заказ"]
                },
                {
                    "title": "Сессии и пользователи ПРИЛОЖЕНИЯ",
                    "type": "trace",
                    "metric_ids": [86,85], 
                    "metric_title": ["Сессии","Пользователи"]
                },
                {
                    "title": "Заказы ПРИЛОЖЕНИЯ",
                    "type": "trace",
                    "metric_ids": [124], 
                    "metric_title": ["Сессии"]
                },
                {
                    "title": "Полнота передачи заказов ПРИЛОЖЕНИЯ",
                    "type": "trace",
                    "metric_ids": [161], 
                    "metric_title": ["Полнота передачи, %"]
                }
            ]
        },
        "gm_digest_w1": {
            "active": True,
            "title": "===[ Weekly DIGEST ]===",
            "bottom": "===[ End of the Weekly DIGEST ]===",
            "group": "digest",
            "message_lvl": "news",
            "device_alias": "", 
            "trafsrc_alias": "",
            "granularity": "w1", # Грануляция отчета, от нее зависят ряд параметров
            "dt_to": "2024-10-01 00:00:00", # Дата от которой строится отчет, может быть текущая current или строка даты-времени с таймзоной
            "dt_delta_fr": { # На сколько единиц времени назад начнется отчет, учитывается только одно наибольшее отклонение, значение 0 - не учитывается. Отсчет ведется от первой секунды начала текущего периода
                "month": 0,
                "days": 7*15,
                "hours": 0
            },    
            "messages": [
                {
                    "title": "Воронка САЙТА",
                    "type": "funnel",
                    "dt_delta_fr": { 
                        "days": 7
                    },  
                    "metric_ids": [2, 7, 41, 21, 23],
                    "metric_title": ["Сессии", "Просмотр товара", "Добавили в корзину", "Начало оформления заказа", "Успешный заказ"]
                },
                {
                    "title": "Пользователи САЙТА",
                    "type": "stack",
                    "metric_ids": [201,200], 
                    "metric_title": ["Вернувшиеся", "Новые"]
                },
                {
                    "title": "Сессии, пользователи САЙТА",
                    "type": "trace",
                    "metric_ids": [2,1], 
                    "metric_title": ["Сессии","Пользователи"]
                },
                {
                    "title": "Сессии по источникам САЙТА - сессии",
                    "type": "stack",
                    "metric_ids": [442, 452, 422, 472, 492, 502, 512], 
                    "metric_title": ["Google", "Yandex", "Adv", "Direct", "Referral", "Email", "Social"]
                },
                {
                    "title": "Заказы САЙТА",
                    "type": "trace",
                    "metric_ids": [23], 
                    "metric_title": ["Заказы"]
                },
                {
                    "title": "Полнота передачи заказов САЙТА",
                    "type": "trace",
                    "metric_ids": [181], 
                    "metric_title": ["Полнота передачи, %"]
                },
                {
                    "title": "Воронка ПРИЛОЖЕНИЯ",
                    "type": "funnel",
                    "metric_ids": [86, 151, 96, 102, 124],
                    "metric_title": ["Сессии", "Просмотр товара", "Добавили в корзину", "Начало оформления заказа", "Успешный заказ"]
                },
                {
                    "title": "Сессии ПРИЛОЖЕНИЯ",
                    "type": "trace",
                    "metric_ids": [86,85], 
                    "metric_title": ["Сессии","Пользователи"]
                },
                {
                    "title": "Заказы ПРИЛОЖЕНИЯ",
                    "type": "trace",
                    "metric_ids": [124], 
                    "metric_title": ["Сессии"]
                },
                {
                    "title": "Полнота передачи заказов ПРИЛОЖЕНИЯ",
                    "type": "trace",
                    "metric_ids": [161], 
                    "metric_title": ["Полнота передачи, %"]
                }
            ]
        },
        "gm_digest_m1": {
            "active": True,
            "title": "===[ Month DIGEST ]===",
            "bottom": "===[ End of the Month DIGEST ]===",
            "group": "digest",
            "message_lvl": "news",
            "device_alias": "", 
            "trafsrc_alias": "",
            "granularity": "m1", # Грануляция отчета, от нее зависят ряд параметров
            "dt_to": "2024-10-01 00:00:00", # Дата от которой строится отчет, может быть текущая current или строка даты-времени с таймзоной
            "dt_delta_fr": { # На сколько единиц времени назад начнется отчет, учитывается только одно наибольшее отклонение, значение 0 - не учитывается. Отсчет ведется от первой секунды начала текущего периода
                "month": 15,
                "days": 0,
                "hours": 0
            },    
            "messages": [
                {
                    "title": "Воронка САЙТА",
                    "type": "funnel",
                    "dt_delta_fr": { 
                        "month": 1
                    },  
                    "metric_upd": "sum", # Если задано, то применяется над всем рядом (sum | avg | min | max)
                    "metric_ids": [2, 7, 41, 21, 23],
                    "metric_title": ["Сессии", "Просмотр товара", "Добавили в корзину", "Начало оформления заказа", "Успешный заказ"]
                },
                {
                    "title": "Пользователи САЙТА",
                    "type": "stack",
                    "metric_ids": [201,200], 
                    "metric_title": ["Вернувшиеся", "Новые"]
                },
                {
                    "title": "Сессии САЙТА",
                    "type": "trace",
                    "metric_ids": [2,1], 
                    "metric_title": ["Сессии","Пользователи"]
                },
                {
                    "title": "Сессии по источникам САЙТА - сессии",
                    "type": "stack",
                    "metric_ids": [442, 452, 422, 472, 492, 502, 512], 
                    "metric_title": ["Google", "Yandex", "Adv", "Direct", "Referral", "Email", "Social"]
                },
                {
                    "title": "Заказы САЙТА",
                    "type": "trace",
                    "metric_ids": [23], 
                    "metric_title": ["Заказы"]
                },
                {
                    "title": "Полнота передачи заказов САЙТА",
                    "type": "trace",
                    "metric_ids": [181], 
                    "metric_title": ["Полнота передачи, %"]
                },
                {
                    "title": "Воронка ПРИЛОЖЕНИЯ",
                    "type": "funnel",
                    "metric_ids": [86, 151, 96, 102, 124],
                    "metric_title": ["Сессии", "Просмотр товара", "Добавили в корзину", "Начало оформления заказа", "Успешный заказ"]
                },
                {
                    "title": "Сессии ПРИЛОЖЕНИЯ",
                    "type": "trace",
                    "metric_ids": [86,85], 
                    "metric_title": ["Сессии","Пользователи"]
                },
                {
                    "title": "Заказы ПРИЛОЖЕНИЯ",
                    "type": "trace",
                    "metric_ids": [124], 
                    "metric_title": ["Сессии"]
                },
                {
                    "title": "Полнота передачи заказов ПРИЛОЖЕНИЯ",
                    "type": "trace",
                    "metric_ids": [161], 
                    "metric_title": ["Полнота передачи, %"]
                }
            ]
        }
    }
}

