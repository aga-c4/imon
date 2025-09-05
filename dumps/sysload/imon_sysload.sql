-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: mysql:3306
-- Время создания: Сен 04 2025 г., 17:29
-- Версия сервера: 8.3.0
-- Версия PHP: 8.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `imon`
--

-- --------------------------------------------------------

--
-- Структура таблицы `metrics`
--

DROP TABLE IF EXISTS `metrics`;
CREATE TABLE `metrics` (
  `id` int NOT NULL,
  `parentid` int NOT NULL DEFAULT '0',
  `metric_active` int NOT NULL DEFAULT '0',
  `metric_monitor` int NOT NULL DEFAULT '0',
  `accum_items` int NOT NULL DEFAULT '1',
  `metric_source_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `accuracy` int NOT NULL DEFAULT '1',
  `metric_api_alias` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_api_filters` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_dp` smallint NOT NULL DEFAULT '0',
  `metric_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_modification` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_ts_types` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `neg_reverce` int NOT NULL DEFAULT '0',
  `metric_group_id` int NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  `metric_device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `metric_region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `metric_trafsrc_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `metrics`
--

INSERT INTO `metrics` (`id`, `parentid`, `metric_active`, `metric_monitor`, `accum_items`, `metric_source_alias`, `metric_alias`, `metric_name`, `accuracy`, `metric_api_alias`, `metric_api_filters`, `metric_dp`, `metric_type`, `metric_modification`, `metric_ts_types`, `neg_reverce`, `metric_group_id`, `metric_project_id`, `metric_device_alias`, `metric_region_alias`, `metric_trafsrc_alias`) VALUES
(1, 0, 1, 1, 1, 'sysload', 'requests_hit_count', 'requests_hit_count', 1, 'requests_hit_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(2, 0, 1, 1, 1, 'sysload', 'requests_start_count', 'requests_start_count', 1, 'requests_start_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(3, 0, 1, 1, 1, 'sysload', 'requests_finish_success_count', 'requests_finish_success_count', 1, 'requests_finish_success_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(4, 0, 1, 1, 1, 'sysload', 'requests_finish_exception_count', 'requests_finish_exception_count', 1, 'requests_finish_exception_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(101, 0, 1, 1, 1, 'sysload', 'requests_start_by_hit', 'requests_start_by_hit', 1, '', '', 2, 'res', '100*m2/m1', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(102, 0, 1, 1, 1, 'sysload', 'requests_finish_success_by_start', 'requests_finish_success_by_start', 1, '', '', 2, 'res', '100*m3/m2', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(103, 0, 1, 1, 1, 'sysload', 'requests_finish_exception_by_start', 'requests_finish_exception_by_start', 1, '', '', 2, 'res', '100*m4/m2', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(201, 0, 1, 1, 1, 'sysload', 'success_max_memory', 'success_max_memory', 1, 'success_max_memory', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(202, 0, 1, 1, 1, 'sysload', 'success_execution_time', 'success_execution_time', 1, 'success_execution_time', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(203, 0, 1, 1, 1, 'sysload', 'success_db_requests', 'success_db_requests', 1, 'success_db_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(204, 0, 1, 1, 1, 'sysload', 'success_db_requests_time', 'success_db_requests_time', 1, 'success_db_requests_time', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(205, 0, 1, 1, 1, 'sysload', 'success_api_requests', 'success_api_requests', 1, 'success_api_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(206, 0, 1, 1, 1, 'sysload', 'success_api_requests_time', 'success_api_requests_time', 1, 'success_api_requests_time', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(207, 0, 1, 1, 1, 'sysload', 'success_db_requests_time_by_request', 'success_db_requests_time_by_request', 1, '', '', 4, 'res', 'm204/m203', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(208, 0, 1, 1, 1, 'sysload', 'success_api_requests_time_by_request', 'success_api_requests_time_by_request', 1, '', '', 4, 'res', 'm206/m205', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(301, 0, 1, 1, 1, 'sysload', 'exception_max_memory', 'exception_max_memory', 1, 'exception_max_memory', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(302, 0, 1, 1, 1, 'sysload', 'exception_execution_time', 'exception_execution_time', 1, 'exception_execution_time', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(303, 0, 1, 1, 1, 'sysload', 'exception_db_requests', 'exception_db_requests', 1, 'exception_db_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(304, 0, 1, 1, 1, 'sysload', 'exception_db_requests_time', 'exception_db_requests_time', 1, 'exception_db_requests_time', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(305, 0, 1, 1, 1, 'sysload', 'exception_api_requests', 'exception_api_requests', 1, 'exception_api_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(306, 0, 1, 1, 1, 'sysload', 'exception_api_requests_time', 'exception_api_requests_time', 1, 'exception_api_requests_time', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(307, 0, 1, 1, 1, 'sysload', 'exception_db_requests_time_by_request', 'exception_db_requests_time_by_request', 1, '', '', 4, 'res', 'm304/m303', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(308, 0, 1, 1, 1, 'sysload', 'exception_api_requests_time_by_request', 'exception_api_requests_time_by_request', 1, '', '', 4, 'res', 'm306/m305', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1101, 0, 1, 1, 1, 'sysload', 'max_mmax_memory_by_startemory', 'max_memory_by_start', 1, '', '', 2, 'res', '100*(m201+m301)/m2', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1102, 0, 1, 1, 1, 'sysload', 'execution_time_by_start', 'execution_time_by_start', 1, '', '', 2, 'res', '100*(m202+m302)/m2', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1103, 0, 1, 1, 1, 'sysload', 'db_requests_by_start', 'db_requests_by_start', 1, '', '', 2, 'res', '100*(m203+m303)/m2', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1104, 0, 1, 1, 1, 'sysload', 'db_requests_time_by_start', 'db_requests_time_by_start', 1, '', '', 2, 'res', '100*(m204+m304)/m2', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1105, 0, 1, 1, 1, 'sysload', 'api_requests_by_start', 'api_requests_by_start', 1, '', '', 2, 'res', '100*(m205+m305)/m2', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1106, 0, 1, 1, 1, 'sysload', 'api_requests_time_by_start', 'api_requests_time_by_start', 1, '', '', 2, 'res', '100*(m206+m306)/m2', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1201, 0, 1, 1, 1, 'sysload', 'success_max_memory_by_start', 'success_max_memory_by_start', 1, '', '', 2, 'res', '100*m201/m3', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1202, 0, 1, 1, 1, 'sysload', 'success_execution_time_by_start', 'success_execution_time_by_start', 1, '', '', 2, 'res', '100*m202/m3', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1203, 0, 1, 1, 1, 'sysload', 'success_db_requests_by_start', 'success_db_requests_by_start', 1, '', '', 2, 'res', '100*m203/m3', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1204, 0, 1, 1, 1, 'sysload', 'success_db_requests_time_by_start', 'success_db_requests_time_by_start', 1, '', '', 2, 'res', '100*m204/m3', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1205, 0, 1, 1, 1, 'sysload', 'success_api_requests_by_start', 'success_api_requests_by_start', 1, '', '', 2, 'res', '100*m205/m3', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1206, 0, 1, 1, 1, 'sysload', 'success_api_requests_time_by_start', 'success_api_requests_time_by_start', 1, '', '', 2, 'res', '100*m206/m3', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1301, 0, 1, 1, 1, 'sysload', 'exception_max_memory_by_start', 'exception_max_memory_by_start', 1, '', '', 2, 'res', '100*m301/m4', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1302, 0, 1, 1, 1, 'sysload', 'exception_execution_time_by_start', 'exception_execution_time_by_start', 1, '', '', 2, 'res', '100*m302/m4', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1303, 0, 1, 1, 1, 'sysload', 'exception_db_requests_by_start', 'exception_db_requests_by_start', 1, '', '', 2, 'res', '100*m303/m4', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1304, 0, 1, 1, 1, 'sysload', 'exception_db_requests_time_by_start', 'exception_db_requests_time_by_start', 1, '', '', 2, 'res', '100*m304/m4', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1305, 0, 1, 1, 1, 'sysload', 'exception_api_requests_by_start', 'exception_api_requests_by_start', 1, '', '', 2, 'res', '100*m305/m4', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all'),
(1306, 0, 1, 1, 1, 'sysload', 'exception_api_requests_time_by_start', 'exception_api_requests_time_by_start', 1, '', '', 2, 'res', '100*m306/m4', 'm1,h1,d1,w1,m1', 0, 1, 1, 'all', 'all', 'all');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `metrics`
--
ALTER TABLE `metrics`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `metrics`
--
ALTER TABLE `metrics`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1307;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
