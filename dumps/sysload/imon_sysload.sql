-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: mysql:3306
-- Время создания: Сен 29 2025 г., 12:31
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
-- Структура таблицы `anoms_d1`
--

CREATE TABLE IF NOT EXISTS `anoms_d1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anoms_h1`
--

CREATE TABLE IF NOT EXISTS `anoms_h1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anoms_m1`
--

CREATE TABLE IF NOT EXISTS `anoms_m1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anoms_mo1`
--

CREATE TABLE IF NOT EXISTS `anoms_mo1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anoms_w1`
--

CREATE TABLE IF NOT EXISTS `anoms_w1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `jobs`
--

CREATE TABLE IF NOT EXISTS `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `task_id` int NOT NULL,
  `job_execution_sec` int NOT NULL DEFAULT '0',
  `job_max_mem_kb` int NOT NULL DEFAULT '0',
  `job_dt_fin` datetime(6) NOT NULL,
  `job_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'run',
  `job_comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics`
--

CREATE TABLE IF NOT EXISTS `metrics` (
  `id` int NOT NULL AUTO_INCREMENT,
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
  `up_dt_funct` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'sum',
  `notags` int NOT NULL DEFAULT '0',
  `metric_group_id` int NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  `metric_device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `metric_region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `metric_trafsrc_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1307 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `metrics`
--

INSERT INTO `metrics` (`id`, `parentid`, `metric_active`, `metric_monitor`, `accum_items`, `metric_source_alias`, `metric_alias`, `metric_name`, `accuracy`, `metric_api_alias`, `metric_api_filters`, `metric_dp`, `metric_type`, `metric_modification`, `metric_ts_types`, `neg_reverce`, `up_dt_funct`, `notags`, `metric_group_id`, `metric_project_id`, `metric_device_alias`, `metric_region_alias`, `metric_trafsrc_alias`) VALUES
(1, 0, 1, 1, 1, 'sysload', 'requests_hit_count', 'requests_hit_count', 1, 'requests_hit_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 1, 1, 1, 'all', 'all', 'all'),
(2, 0, 1, 1, 1, 'sysload', 'requests_start_count', 'requests_start_count', 1, 'requests_start_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(3, 0, 1, 1, 1, 'sysload', 'requests_finish_success_count', 'requests_finish_success_count', 1, 'requests_finish_success_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(4, 0, 1, 1, 1, 'sysload', 'requests_finish_exception_count', 'requests_finish_exception_count', 1, 'requests_finish_exception_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(5, 0, 1, 1, 1, 'sysload', 'system_cpu_usage', 'system_cpu_usage', 1, 'system_cpu_usage', '', 1, 'src', '', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(6, 0, 1, 1, 1, 'sysload', 'system_load_average', 'system_load_average', 1, 'system_load_average', '', 1, 'src', '', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(7, 0, 1, 1, 1, 'sysload', 'system_memory_max', 'system_memory_max', 1, 'system_memory_max', '', 2, 'src', '', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(8, 0, 1, 1, 1, 'sysload', 'system_memory_usage', 'system_memory_usage', 1, 'system_memory_usage', '', 2, 'src', '', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(9, 0, 1, 1, 1, 'sysload', 'system_memory_usage_pr', 'system_memory_usage_pr', 1, '', '', 2, 'res', '100*m8/m7', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(20, 0, 1, 1, 1, 'sysload', 'logging_max_memory', 'logging_max_memory', 1, 'logging_max_memory', '', 2, 'src', '', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(21, 0, 1, 1, 1, 'sysload', 'logging_max_memory_by_avg_pr', 'logging_max_memory_by_avg_pr', 1, '', '', 2, 'res', '100*m20/((m201+m301)/m2)', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(22, 0, 1, 1, 1, 'sysload', 'logging_execution_time', 'logging_execution_time', 1, 'logging_execution_time', '', 2, 'src', '', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(23, 0, 1, 1, 1, 'sysload', 'logging_execution_time_by_avg_pr', 'logging_execution_time_by_avg_pr', 1, '', '', 2, 'res', '100*m22/((m202+m302)/m2)', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(151, 0, 1, 1, 1, 'sysload', 'requests_start_by_hit_pr', 'requests_start_by_hit_pr', 1, '', '', 3, 'res', '100*m2/ma1', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 1, 1, 'all', 'all', 'all'),
(152, 0, 1, 1, 1, 'sysload', 'requests_finish_success_by_start_pr', 'requests_finish_success_by_start_pr', 1, '', '', 3, 'res', '100*m3/m2', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(153, 0, 1, 1, 1, 'sysload', 'requests_finish_exception_by_start_pr', 'requests_finish_exception_by_start_pr', 1, '', '', 3, 'res', '100*m4/m2', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(201, 0, 1, 1, 1, 'sysload', 'success_max_memory', 'success_max_memory', 1, 'success_max_memory', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(202, 0, 1, 1, 1, 'sysload', 'success_execution_time', 'success_execution_time', 1, 'success_execution_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(203, 0, 1, 1, 1, 'sysload', 'success_db_requests', 'success_db_requests', 1, 'success_db_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(204, 0, 1, 1, 1, 'sysload', 'success_db_requests_time', 'success_db_requests_time', 1, 'success_db_requests_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(205, 0, 1, 1, 1, 'sysload', 'success_api_requests', 'success_api_requests', 1, 'success_api_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(206, 0, 1, 1, 1, 'sysload', 'success_api_requests_time', 'success_api_requests_time', 1, 'success_api_requests_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(207, 0, 1, 1, 1, 'sysload', 'success_db_requests_time_by_request_pr', 'success_db_requests_time_by_request_pr', 1, '', '', 3, 'res', 'm204/m203', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(208, 0, 1, 1, 1, 'sysload', 'success_api_requests_time_by_request_pr', 'success_api_requests_time_by_request_pr', 1, '', '', 3, 'res', 'm206/m205', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(301, 0, 1, 1, 1, 'sysload', 'exception_max_memory', 'exception_max_memory', 1, 'exception_max_memory', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(302, 0, 1, 1, 1, 'sysload', 'exception_execution_time', 'exception_execution_time', 1, 'exception_execution_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(303, 0, 1, 1, 1, 'sysload', 'exception_db_requests', 'exception_db_requests', 1, 'exception_db_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(304, 0, 1, 1, 1, 'sysload', 'exception_db_requests_time', 'exception_db_requests_time', 1, 'exception_db_requests_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(305, 0, 1, 1, 1, 'sysload', 'exception_api_requests', 'exception_api_requests', 1, 'exception_api_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(306, 0, 1, 1, 1, 'sysload', 'exception_api_requests_time', 'exception_api_requests_time', 1, 'exception_api_requests_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(307, 0, 1, 1, 1, 'sysload', 'exception_db_requests_time_by_request_pr', 'exception_db_requests_time_by_request_pr', 1, '', '', 3, 'res', 'm304/m303', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(308, 0, 1, 1, 1, 'sysload', 'exception_api_requests_time_by_request_pr', 'exception_api_requests_time_by_request_pr', 1, '', '', 3, 'res', 'm306/m305', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1101, 0, 1, 1, 1, 'sysload', 'max_memory_by_start_pr', 'max_memory_by_start_pr', 1, '', '', 3, 'res', '100*(m201+m301)/m2', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1102, 0, 1, 1, 1, 'sysload', 'execution_time_by_start_pr', 'execution_time_by_start_pr', 1, '', '', 3, 'res', '100*(m202+m302)/m2', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1103, 0, 1, 1, 1, 'sysload', 'db_requests_by_start_pr', 'db_requests_by_start_pr', 1, '', '', 3, 'res', '100*(m203+m303)/m2', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1104, 0, 1, 1, 1, 'sysload', 'db_requests_time_by_start_pr', 'db_requests_time_by_start_pr', 1, '', '', 3, 'res', '100*(m204+m304)/m2', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1105, 0, 1, 1, 1, 'sysload', 'api_requests_by_start_pr', 'api_requests_by_start_pr', 1, '', '', 3, 'res', '100*(m205+m305)/m2', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1106, 0, 1, 1, 1, 'sysload', 'api_requests_time_by_start_pr', 'api_requests_time_by_start_pr', 1, '', '', 3, 'res', '100*(m206+m306)/m2', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1201, 0, 1, 1, 1, 'sysload', 'success_max_memory_by_start_pr', 'success_max_memory_by_start_pr', 1, '', '', 3, 'res', '100*m201/m3', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1202, 0, 1, 1, 1, 'sysload', 'success_execution_time_by_start_pr', 'success_execution_time_by_start_pr', 1, '', '', 3, 'res', '100*m202/m3', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1203, 0, 1, 1, 1, 'sysload', 'success_db_requests_by_start_pr', 'success_db_requests_by_start_pr', 1, '', '', 3, 'res', '100*m203/m3', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1204, 0, 1, 1, 1, 'sysload', 'success_db_requests_time_by_start_pr', 'success_db_requests_time_by_start_pr', 1, '', '', 3, 'res', '100*m204/m3', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1205, 0, 1, 1, 1, 'sysload', 'success_api_requests_by_start_pr', 'success_api_requests_by_start_pr', 1, '', '', 3, 'res', '100*m205/m3', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1206, 0, 1, 1, 1, 'sysload', 'success_api_requests_time_by_start', 'success_api_requests_time_by_start', 1, '', '', 3, 'res', '100*m206/m3', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1301, 0, 1, 1, 1, 'sysload', 'exception_max_memory_by_start_pr', 'exception_max_memory_by_start_pr', 1, '', '', 3, 'res', '100*m301/m4', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1302, 0, 1, 1, 1, 'sysload', 'exception_execution_time_by_start_pr', 'exception_execution_time_by_start_pr', 1, '', '', 3, 'res', '100*m302/m4', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1303, 0, 1, 1, 1, 'sysload', 'exception_db_requests_by_start_pr', 'exception_db_requests_by_start_pr', 1, '', '', 3, 'res', '100*m303/m4', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1304, 0, 1, 1, 1, 'sysload', 'exception_db_requests_time_by_start_pr', 'exception_db_requests_time_by_start_pr', 1, '', '', 3, 'res', '100*m304/m4', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1305, 0, 1, 1, 1, 'sysload', 'exception_api_requests_by_start_pr', 'exception_api_requests_by_start_pr', 1, '', '', 3, 'res', '100*m305/m4', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1306, 0, 1, 1, 1, 'sysload', 'exception_api_requests_time_by_start_pr', 'exception_api_requests_time_by_start_pr', 1, '', '', 3, 'res', '100*m306/m4', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all');

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_d1`
--

CREATE TABLE IF NOT EXISTS `metrics_d1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_h1`
--

CREATE TABLE IF NOT EXISTS `metrics_h1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_m1`
--

CREATE TABLE IF NOT EXISTS `metrics_m1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_mo1`
--

CREATE TABLE IF NOT EXISTS `metrics_mo1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_w1`
--

CREATE TABLE IF NOT EXISTS `metrics_w1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metric_groups`
--

CREATE TABLE IF NOT EXISTS `metric_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `metric_group_alias` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_group_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `metric_groups`
--

INSERT INTO `metric_groups` (`id`, `metric_group_alias`, `metric_group_name`) VALUES
(1, 'critical', 'Critical'),
(2, 'important', 'important'),
(3, 'all', 'Unimportant'),
(4, 'little', 'Low');

-- --------------------------------------------------------

--
-- Структура таблицы `metric_projects`
--

CREATE TABLE IF NOT EXISTS `metric_projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `metric_project_alias` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_project_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `metric_projects`
--

INSERT INTO `metric_projects` (`id`, `metric_project_alias`, `metric_project_name`) VALUES
(1, 'b2b_current', 'B2B current'),
(2, 'b2b_stable', 'B2B stable'),
(3, 'honew', 'HO New');

-- --------------------------------------------------------

--
-- Структура таблицы `tags`
--

CREATE TABLE IF NOT EXISTS `tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL DEFAULT '0',
  `tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `tasks`
--

CREATE TABLE IF NOT EXISTS `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_active` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL DEFAULT '0',
  `granularity` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `message_lvl` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `task_comment` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `task_settings` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task_robot` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `task_max_execution_sec` int NOT NULL DEFAULT '240',
  `task_project_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
