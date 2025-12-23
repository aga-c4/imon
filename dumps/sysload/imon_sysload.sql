-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Хост: mysql-svc.mysql.svc.cluster.local:3306
-- Время создания: Дек 23 2025 г., 09:51
-- Версия сервера: 9.5.0
-- Версия PHP: 8.3.26

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

DROP TABLE IF EXISTS `anoms_d1`;
CREATE TABLE `anoms_d1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anoms_h1`
--

DROP TABLE IF EXISTS `anoms_h1`;
CREATE TABLE `anoms_h1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anoms_m1`
--

DROP TABLE IF EXISTS `anoms_m1`;
CREATE TABLE `anoms_m1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anoms_mo1`
--

DROP TABLE IF EXISTS `anoms_mo1`;
CREATE TABLE `anoms_mo1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anoms_w1`
--

DROP TABLE IF EXISTS `anoms_w1`;
CREATE TABLE `anoms_w1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` tinyint NOT NULL DEFAULT '0',
  `direction` tinyint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `jobs`
--

DROP TABLE IF EXISTS `jobs`;
CREATE TABLE `jobs` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `task_id` int NOT NULL,
  `job_execution_sec` int NOT NULL DEFAULT '0',
  `job_max_mem_kb` int NOT NULL DEFAULT '0',
  `job_dt_fin` datetime(6) NOT NULL,
  `job_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'run',
  `job_comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `job_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `metric_monitor_send` int NOT NULL DEFAULT '0',
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
  `metric_trafsrc_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `metrics`
--

INSERT INTO `metrics` (`id`, `parentid`, `metric_active`, `metric_monitor`, `metric_monitor_send`, `accum_items`, `metric_source_alias`, `metric_alias`, `metric_name`, `accuracy`, `metric_api_alias`, `metric_api_filters`, `metric_dp`, `metric_type`, `metric_modification`, `metric_ts_types`, `neg_reverce`, `up_dt_funct`, `notags`, `metric_group_id`, `metric_project_id`, `metric_device_alias`, `metric_region_alias`, `metric_trafsrc_alias`) VALUES
(1, 0, 1, 0, 0, 1, 'sysload', 'requests_hit_count', 'requests_hit_count', 1, 'requests_hit_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 1, 2, 1, 'all', 'all', 'all'),
(2, 0, 1, 1, 1, 1, 'sysload', 'requests_start_count', 'requests_start_count', 1, 'requests_start_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(3, 0, 1, 0, 0, 1, 'sysload', 'requests_finish_success_count', 'requests_finish_success_count', 1, 'requests_finish_success_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 0, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(4, 0, 1, 0, 0, 1, 'sysload', 'requests_finish_exception_count', 'requests_finish_exception_count', 1, 'requests_finish_exception_count', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(5, 0, 1, 0, 0, 1, 'sysload', 'system_cpu_usage', 'system_cpu_usage', 1, 'system_cpu_usage', '', 1, 'src', '', 'm1,h1,d1,w1,m1', 1, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(6, 0, 1, 0, 0, 1, 'sysload', 'system_load_average', 'system_load_average', 1, 'system_load_average', '', 1, 'src', '', 'm1,h1,d1,w1,m1', 1, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(7, 0, 1, 0, 0, 1, 'sysload', 'system_memory_max', 'system_memory_max', 1, 'system_memory_max', '', 2, 'src', '', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(8, 0, 1, 0, 0, 1, 'sysload', 'system_memory_usage', 'system_memory_usage', 1, 'system_memory_usage', '', 2, 'src', '', 'm1,h1,d1,w1,m1', 1, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(9, 0, 1, 0, 0, 1, 'sysload', 'system_memory_usage_pr', 'system_memory_usage_pr', 1, '', '', 2, 'res', '100*m8/m7', 'm1,h1,d1,w1,m1', 1, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(20, 0, 1, 0, 0, 1, 'sysload', 'logging_max_memory', 'logging_max_memory', 1, 'logging_max_memory', '', 2, 'src', '', 'm1,h1,d1,w1,m1', 1, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(21, 0, 1, 0, 0, 1, 'sysload', 'logging_max_memory_by_avg_pr', 'logging_max_memory_by_avg_pr', 1, '', '', 2, 'res', '100*m20/(m201/m2)', 'm1,h1,d1,w1,m1', 1, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(22, 0, 1, 0, 0, 1, 'sysload', 'logging_execution_time', 'logging_execution_time', 1, 'logging_execution_time', '', 2, 'src', '', 'm1,h1,d1,w1,m1', 1, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(23, 0, 1, 0, 0, 1, 'sysload', 'logging_execution_time_by_avg_pr', 'logging_execution_time_by_avg_pr', 1, '', '', 2, 'res', '100*m22/(m202/m2)', 'm1,h1,d1,w1,m1', 1, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(151, 0, 1, 0, 0, 1, 'sysload', 'requests_start_by_hit_pr', 'requests_start_by_hit_pr', 1, '', '', 3, 'res', '100*m2/ma1', 'm1,h1,d1,w1,m1', 0, 'avg', 1, 2, 1, 'all', 'all', 'all'),
(152, 0, 1, 0, 1, 1, 'sysload', 'requests_finish_success_by_start_pr', 'requests_finish_success_by_start_pr', 1, '', '', 3, 'res', '100*m3/m2', 'm1,h1,d1,w1,m1', 0, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(153, 0, 1, 1, 0, 1, 'sysload', 'requests_finish_exception_by_start_pr', 'requests_finish_exception_by_start_pr', 1, '', '', 3, 'res', '100*m4/m2', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(201, 0, 1, 0, 0, 1, 'sysload', 'success_max_memory', 'success_max_memory', 1, 'success_max_memory', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(202, 0, 1, 1, 1, 1, 'sysload', 'success_execution_time', 'success_execution_time', 1, 'success_execution_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 1, 1, 'all', 'all', 'all'),
(203, 0, 1, 0, 0, 1, 'sysload', 'success_db_requests', 'success_db_requests', 1, 'success_db_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(204, 202, 1, 0, 0, 1, 'sysload', 'success_db_requests_time', 'success_db_requests_time', 1, 'success_db_requests_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(205, 0, 1, 0, 0, 1, 'sysload', 'success_api_requests', 'success_api_requests', 1, 'success_api_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(206, 202, 1, 0, 0, 1, 'sysload', 'success_api_requests_time', 'success_api_requests_time', 1, 'success_api_requests_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(301, 0, 1, 0, 0, 1, 'sysload', 'exception_max_memory', 'exception_max_memory', 1, 'exception_max_memory', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(302, 0, 1, 0, 0, 1, 'sysload', 'exception_execution_time', 'exception_execution_time', 1, 'exception_execution_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(303, 0, 1, 0, 0, 1, 'sysload', 'exception_db_requests', 'exception_db_requests', 1, 'exception_db_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(304, 302, 1, 0, 0, 1, 'sysload', 'exception_db_requests_time', 'exception_db_requests_time', 1, 'exception_db_requests_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(305, 0, 1, 0, 0, 1, 'sysload', 'exception_api_requests', 'exception_api_requests', 1, 'exception_api_requests', '', 0, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(306, 302, 1, 0, 0, 1, 'sysload', 'exception_api_requests_time', 'exception_api_requests_time', 1, 'exception_api_requests_time', '', 3, 'src', '', 'm1,h1,d1,w1,m1', 1, 'sum', 0, 2, 1, 'all', 'all', 'all'),
(1201, 0, 1, 1, 1, 1, 'sysload', 'success_max_memory_by_start', 'success_max_memory_by_start', 1, '', '', 3, 'res', 'm201/m3', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1202, 0, 1, 1, 1, 1, 'sysload', 'success_execution_time_by_start', 'success_execution_time_by_start', 1, '', '', 3, 'res', 'm202/m3', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1203, 0, 1, 0, 0, 1, 'sysload', 'success_db_requests_by_start', 'success_db_requests_by_start', 1, '', '', 3, 'res', 'm203/m3', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1204, 0, 1, 1, 1, 1, 'sysload', 'success_db_requests_time_by_start', 'success_db_requests_time_by_start', 1, '', '', 3, 'res', 'm204/m3', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1205, 0, 1, 0, 0, 1, 'sysload', 'success_api_requests_by_start', 'success_api_requests_by_start', 1, '', '', 3, 'res', 'm205/m3', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1206, 0, 1, 1, 1, 1, 'sysload', 'success_api_requests_time_by_start', 'success_api_requests_time_by_start', 1, '', '', 3, 'res', 'm206/m3', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 1, 1, 'all', 'all', 'all'),
(1207, 0, 1, 0, 0, 1, 'sysload', 'success_db_requests_time_by_request_pr', 'success_db_requests_time_by_request', 1, '', '', 3, 'res', 'm204/m203', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1208, 0, 1, 0, 0, 1, 'sysload', 'success_api_requests_time_by_request_pr', 'success_api_requests_time_by_request', 1, '', '', 3, 'res', 'm206/m205', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1209, 0, 1, 0, 0, 1, 'sysload', 'success_db_requests_time_by_time_pr', 'success_db_requests_time_by_time_pr', 1, '', '', 3, 'res', '100*m204/m202', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1210, 0, 1, 0, 0, 1, 'sysload', 'success_api_requests_time_by_time_pr', 'success_api_requests_time_by_time_pr', 1, '', '', 3, 'res', '100*m206/m202', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1301, 0, 1, 0, 0, 1, 'sysload', 'exception_max_memory_by_start', 'exception_max_memory_by_start', 1, '', '', 3, 'res', 'm301/m4', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1302, 0, 1, 0, 0, 1, 'sysload', 'exception_execution_time_by_start', 'exception_execution_time_by_start', 1, '', '', 3, 'res', 'm302/m4', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1303, 0, 1, 0, 0, 1, 'sysload', 'exception_db_requests_by_start', 'exception_db_requests_by_start', 1, '', '', 3, 'res', 'm303/m4', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1304, 0, 1, 0, 0, 1, 'sysload', 'exception_db_requests_time_by_start', 'exception_db_requests_time_by_start', 1, '', '', 3, 'res', 'm304/m4', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1305, 0, 1, 0, 0, 1, 'sysload', 'exception_api_requests_by_start', 'exception_api_requests_by_start', 1, '', '', 3, 'res', 'm305/m4', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1306, 0, 1, 0, 0, 1, 'sysload', 'exception_api_requests_time_by_start', 'exception_api_requests_time_by_start', 1, '', '', 3, 'res', 'm306/m4', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1307, 0, 1, 0, 0, 1, 'sysload', 'exception_db_requests_time_by_request', 'exception_db_requests_time_by_request', 1, '', '', 3, 'res', 'm304/m303', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1308, 0, 1, 0, 0, 1, 'sysload', 'exception_api_requests_time_by_request', 'exception_api_requests_time_by_request', 1, '', '', 3, 'res', 'm306/m305', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1309, 0, 1, 0, 0, 1, 'sysload', 'exception_db_requests_time_by_time_pr', 'exception_db_requests_time_by_time_pr', 1, '', '', 3, 'res', '100*m304/m302', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1310, 0, 1, 0, 0, 1, 'sysload', 'exception_api_requests_time_by_time_pr', 'exception_api_requests_time_by_time_pr', 1, '', '', 3, 'res', '100*m306/m302', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1401, 0, 1, 0, 0, 1, 'sysload', 'success_max_memory_by_alltg_pr', 'success_max_memory_by_alltg_pr', 1, '', '', 3, 'res', '100*m201/ma201', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1402, 0, 1, 0, 0, 1, 'sysload', 'success_execution_time_by_alltg_pr', 'success_execution_time_by_alltg_pr', 1, '', '', 3, 'res', '100*m202/ma202', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1403, 0, 1, 0, 0, 1, 'sysload', 'success_db_requests_alltg_pr', 'success_db_requests_by_alltg_pr', 1, '', '', 3, 'res', '100*m203/ma203', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1404, 0, 1, 0, 0, 1, 'sysload', 'success_db_requests_time_by_alltg_pr', 'success_db_requests_time_by_alltg_pr', 1, '', '', 3, 'res', '100*m204/ma204', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1405, 0, 1, 0, 0, 1, 'sysload', 'success_api_requests_by_alltg_pr', 'success_api_requests_by_alltg_pr', 1, '', '', 3, 'res', '100*m205/ma205', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1406, 0, 1, 0, 0, 1, 'sysload', 'success_api_requests_time_alltg_pr', 'success_api_requests_time_by_alltg_pr', 1, '', '', 3, 'res', '100*m206/ma206', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1501, 0, 1, 0, 0, 1, 'sysload', 'exception_max_memory_by_alltg_pr', 'exception_max_memory_by_alltg_pr', 1, '', '', 3, 'res', '100*m301/ma301', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1502, 0, 1, 0, 0, 1, 'sysload', 'exception_execution_time_by_alltg_pr', 'exception_execution_time_by_alltg_pr', 1, '', '', 3, 'res', '100*m302/ma302', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1503, 0, 1, 0, 0, 1, 'sysload', 'exception_db_requests_by_alltg_pr', 'exception_db_requests_by_alltg_pr', 1, '', '', 3, 'res', '100*m303/ma303', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1504, 0, 1, 0, 0, 1, 'sysload', 'exception_db_requests_time_by_alltg_pr', 'exception_db_requests_time_by_alltg_pr', 1, '', '', 3, 'res', '100*m304/ma304', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1505, 0, 1, 0, 0, 1, 'sysload', 'exception_api_requests_by_alltg_pr', 'exception_api_requests_alltg_pr', 1, '', '', 3, 'res', '100*m305/ma305', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all'),
(1506, 0, 1, 0, 0, 1, 'sysload', 'exception_api_requests_time_by_alltg_pr', 'exception_api_requests_time_by_alltg_pr', 1, '', '', 3, 'res', '100*m306/ma306', 'm1,h1,d1,w1,m1', 1, 'avg', 0, 2, 1, 'all', 'all', 'all');

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_d1`
--

DROP TABLE IF EXISTS `metrics_d1`;
CREATE TABLE `metrics_d1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_h1`
--

DROP TABLE IF EXISTS `metrics_h1`;
CREATE TABLE `metrics_h1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_m1`
--

DROP TABLE IF EXISTS `metrics_m1`;
CREATE TABLE `metrics_m1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_mo1`
--

DROP TABLE IF EXISTS `metrics_mo1`;
CREATE TABLE `metrics_mo1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_w1`
--

DROP TABLE IF EXISTS `metrics_w1`;
CREATE TABLE `metrics_w1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_tag_id` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metric_accounts`
--

DROP TABLE IF EXISTS `metric_accounts`;
CREATE TABLE `metric_accounts` (
  `id` int NOT NULL,
  `active` int NOT NULL DEFAULT '0',
  `account_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `metric_accounts`
--

INSERT INTO `metric_accounts` (`id`, `active`, `account_name`) VALUES
(1, 1, 'Samo'),
(2, 1, 'Shrilanka'),
(3, 1, 'Amega'),
(4, 1, 'Space');

-- --------------------------------------------------------

--
-- Структура таблицы `metric_groups`
--

DROP TABLE IF EXISTS `metric_groups`;
CREATE TABLE `metric_groups` (
  `id` int NOT NULL,
  `metric_group_alias` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_group_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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

DROP TABLE IF EXISTS `metric_projects`;
CREATE TABLE `metric_projects` (
  `id` int NOT NULL,
  `active` int NOT NULL DEFAULT '0',
  `account_id` int NOT NULL DEFAULT '0',
  `metric_project_alias` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_project_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `last_dt_gen_use` int NOT NULL DEFAULT '1',
  `monitoring` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `metric_projects`
--

INSERT INTO `metric_projects` (`id`, `active`, `account_id`, `metric_project_alias`, `metric_project_name`, `last_dt_gen_use`, `monitoring`) VALUES
(1, 1, 1, 'b2b_current', 'B2B current', 1, 0),
(2, 1, 1, 'b2b_stable', 'B2B stable', 1, 0),
(3, 1, 2, 'shri_b2b', 'shri_b2b', 1, 1),
(4, 1, 2, 'shri_ho', 'shri_ho', 1, 1),
(5, 1, 2, 'shri_b2c', 'shri_b2c', 1, 1),
(10, 1, 3, 'amega_b2b', 'amega-b2b', 1, 1),
(12, 1, 3, 'amega_ho', 'amega_ho', 1, 1),
(13, 1, 4, 'space_b2b', 'space_b2b', 1, 0),
(14, 1, 4, 'space_b2c', 'space_b2c', 1, 0),
(15, 1, 4, 'space_hb', 'space_hb', 1, 0),
(16, 1, 4, 'space_airport', 'space_airport', 1, 0),
(17, 0, 4, 'space_guidebook', 'space_guidebook', 1, 0),
(18, 1, 4, 'space_guestservice', 'space_guestservice', 1, 0),
(19, 1, 4, 'space_all', 'space_all', 1, 1),
(20, 1, 4, 'space_main', 'space_main', 1, 0),
(21, 1, 4, 'space_apiold', 'space_apiold', 1, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `tags`
--

DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `id` int NOT NULL,
  `project_id` int NOT NULL DEFAULT '0',
  `tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `tasks`
--

DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks` (
  `id` int NOT NULL,
  `task_active` int NOT NULL DEFAULT '0',
  `metric_id` int NOT NULL DEFAULT '0',
  `granularity` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `message_lvl` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `task_comment` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `task_settings` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task_robot` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `task_max_execution_sec` int NOT NULL DEFAULT '240',
  `task_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `tasks`
--

INSERT INTO `tasks` (`id`, `task_active`, `metric_id`, `granularity`, `message_lvl`, `task_comment`, `task_settings`, `task_robot`, `task_max_execution_sec`, `task_project_id`) VALUES
(1, 0, 1, 'h1', 'important', 'anom_requests_hit_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(2, 1, 2, 'h1', 'critical', 'anom_requests_start_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(3, 0, 3, 'h1', 'important', 'anom_requests_finish_success_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(4, 0, 4, 'h1', 'important', 'anom_requests_finish_exception_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(5, 0, 5, 'h1', 'important', 'anom_system_cpu_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(6, 0, 6, 'h1', 'important', 'anom_system_load_average_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(7, 0, 7, 'h1', 'important', 'anom_system_memory_max_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(8, 0, 8, 'h1', 'important', 'anom_system_memory_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(9, 0, 9, 'h1', 'important', 'anom_system_memory_usage_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(10, 0, 20, 'h1', 'important', 'anom_logging_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(11, 0, 21, 'h1', 'important', 'anom_logging_max_memory_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(12, 0, 22, 'h1', 'important', 'anom_logging_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(13, 0, 23, 'h1', 'important', 'anom_logging_execution_time_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(14, 0, 151, 'h1', 'important', 'anom_requests_start_by_hit_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(15, 1, 152, 'h1', 'critical', 'anom_requests_finish_success_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(16, 0, 153, 'h1', 'important', 'anom_requests_finish_exception_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(17, 0, 201, 'h1', 'important', 'anom_success_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(18, 0, 202, 'h1', 'important', 'anom_success_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(19, 0, 203, 'h1', 'important', 'anom_success_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(20, 0, 204, 'h1', 'important', 'anom_success_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(21, 0, 205, 'h1', 'important', 'anom_success_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(22, 0, 206, 'h1', 'important', 'anom_success_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(23, 0, 301, 'h1', 'important', 'anom_exception_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(24, 0, 302, 'h1', 'important', 'anom_exception_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(25, 0, 303, 'h1', 'important', 'anom_exception_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(26, 0, 304, 'h1', 'important', 'anom_exception_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(27, 0, 305, 'h1', 'important', 'anom_exception_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(28, 0, 306, 'h1', 'important', 'anom_exception_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(29, 1, 1201, 'h1', 'critical', 'anom_success_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(30, 1, 1202, 'h1', 'critical', 'anom_success_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(31, 0, 1203, 'h1', 'important', 'anom_success_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(32, 1, 1204, 'h1', 'critical', 'anom_success_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(33, 0, 1205, 'h1', 'important', 'anom_success_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(34, 1, 1206, 'h1', 'critical', 'anom_success_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(35, 0, 1207, 'h1', 'important', 'anom_success_db_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(36, 0, 1208, 'h1', 'important', 'anom_success_api_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(37, 0, 1209, 'h1', 'important', 'anom_success_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(38, 0, 1210, 'h1', 'important', 'anom_success_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(39, 0, 1301, 'h1', 'important', 'anom_exception_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(40, 0, 1302, 'h1', 'important', 'anom_exception_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(41, 0, 1303, 'h1', 'important', 'anom_exception_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(42, 0, 1304, 'h1', 'important', 'anom_exception_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(43, 0, 1305, 'h1', 'important', 'anom_exception_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(44, 0, 1306, 'h1', 'important', 'anom_exception_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(45, 0, 1307, 'h1', 'important', 'anom_exception_db_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(46, 0, 1308, 'h1', 'important', 'anom_exception_api_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(47, 0, 1309, 'h1', 'important', 'anom_exception_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(48, 0, 1310, 'h1', 'important', 'anom_exception_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(49, 0, 1401, 'h1', 'important', 'anom_success_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(50, 0, 1402, 'h1', 'important', 'anom_success_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(51, 0, 1403, 'h1', 'important', 'anom_success_db_requests_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(52, 0, 1404, 'h1', 'important', 'anom_success_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(53, 0, 1405, 'h1', 'important', 'anom_success_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(54, 0, 1406, 'h1', 'important', 'anom_success_api_requests_time_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(55, 0, 1501, 'h1', 'important', 'anom_exception_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(56, 0, 1502, 'h1', 'important', 'anom_exception_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(57, 0, 1503, 'h1', 'important', 'anom_exception_db_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(58, 0, 1504, 'h1', 'important', 'anom_exception_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(59, 0, 1505, 'h1', 'important', 'anom_exception_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(60, 0, 1506, 'h1', 'important', 'anom_exception_api_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(61, 0, 1, 'h1', 'important', 'anom_requests_hit_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(62, 1, 2, 'h1', 'critical', 'anom_requests_start_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(63, 0, 3, 'h1', 'important', 'anom_requests_finish_success_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(64, 0, 4, 'h1', 'important', 'anom_requests_finish_exception_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(65, 0, 5, 'h1', 'important', 'anom_system_cpu_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(66, 0, 6, 'h1', 'important', 'anom_system_load_average_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(67, 0, 7, 'h1', 'important', 'anom_system_memory_max_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(68, 0, 8, 'h1', 'important', 'anom_system_memory_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(69, 0, 9, 'h1', 'important', 'anom_system_memory_usage_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(70, 0, 20, 'h1', 'important', 'anom_logging_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(71, 0, 21, 'h1', 'important', 'anom_logging_max_memory_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(72, 0, 22, 'h1', 'important', 'anom_logging_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(73, 0, 23, 'h1', 'important', 'anom_logging_execution_time_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(74, 0, 151, 'h1', 'important', 'anom_requests_start_by_hit_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(75, 1, 152, 'h1', 'critical', 'anom_requests_finish_success_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(76, 0, 153, 'h1', 'important', 'anom_requests_finish_exception_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(77, 0, 201, 'h1', 'important', 'anom_success_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(78, 1, 202, 'h1', 'critical', 'anom_success_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(79, 0, 203, 'h1', 'important', 'anom_success_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(80, 0, 204, 'h1', 'important', 'anom_success_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(81, 0, 205, 'h1', 'important', 'anom_success_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(82, 0, 206, 'h1', 'important', 'anom_success_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(83, 0, 301, 'h1', 'important', 'anom_exception_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(84, 0, 302, 'h1', 'important', 'anom_exception_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(85, 0, 303, 'h1', 'important', 'anom_exception_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(86, 0, 304, 'h1', 'important', 'anom_exception_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(87, 0, 305, 'h1', 'important', 'anom_exception_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(88, 0, 306, 'h1', 'important', 'anom_exception_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(89, 1, 1201, 'h1', 'critical', 'anom_success_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(90, 1, 1202, 'h1', 'critical', 'anom_success_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(91, 0, 1203, 'h1', 'important', 'anom_success_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(92, 1, 1204, 'h1', 'critical', 'anom_success_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(93, 0, 1205, 'h1', 'important', 'anom_success_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(94, 1, 1206, 'h1', 'critical', 'anom_success_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(95, 0, 1207, 'h1', 'important', 'anom_success_db_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(96, 0, 1208, 'h1', 'important', 'anom_success_api_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(97, 0, 1209, 'h1', 'important', 'anom_success_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(98, 0, 1210, 'h1', 'important', 'anom_success_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(99, 0, 1301, 'h1', 'important', 'anom_exception_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(100, 0, 1302, 'h1', 'important', 'anom_exception_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(101, 0, 1303, 'h1', 'important', 'anom_exception_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(102, 0, 1304, 'h1', 'important', 'anom_exception_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(103, 0, 1305, 'h1', 'important', 'anom_exception_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(104, 0, 1306, 'h1', 'important', 'anom_exception_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(105, 0, 1307, 'h1', 'important', 'anom_exception_db_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(106, 0, 1308, 'h1', 'important', 'anom_exception_api_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(107, 0, 1309, 'h1', 'important', 'anom_exception_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(108, 0, 1310, 'h1', 'important', 'anom_exception_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(109, 0, 1401, 'h1', 'important', 'anom_success_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(110, 0, 1402, 'h1', 'important', 'anom_success_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(111, 0, 1403, 'h1', 'important', 'anom_success_db_requests_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(112, 0, 1404, 'h1', 'important', 'anom_success_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(113, 0, 1405, 'h1', 'important', 'anom_success_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(114, 0, 1406, 'h1', 'important', 'anom_success_api_requests_time_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(115, 0, 1501, 'h1', 'important', 'anom_exception_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(116, 0, 1502, 'h1', 'important', 'anom_exception_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(117, 0, 1503, 'h1', 'important', 'anom_exception_db_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(118, 0, 1504, 'h1', 'important', 'anom_exception_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(119, 0, 1505, 'h1', 'important', 'anom_exception_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(120, 0, 1506, 'h1', 'important', 'anom_exception_api_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 3),
(121, 0, 1, 'h1', 'important', 'anom_requests_hit_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(122, 1, 2, 'h1', 'critical', 'anom_requests_start_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(123, 0, 3, 'h1', 'important', 'anom_requests_finish_success_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(124, 0, 4, 'h1', 'important', 'anom_requests_finish_exception_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(125, 0, 5, 'h1', 'important', 'anom_system_cpu_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(126, 0, 6, 'h1', 'important', 'anom_system_load_average_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(127, 0, 7, 'h1', 'important', 'anom_system_memory_max_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(128, 0, 8, 'h1', 'important', 'anom_system_memory_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(129, 0, 9, 'h1', 'important', 'anom_system_memory_usage_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(130, 0, 20, 'h1', 'important', 'anom_logging_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(131, 0, 21, 'h1', 'important', 'anom_logging_max_memory_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(132, 0, 22, 'h1', 'important', 'anom_logging_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(133, 0, 23, 'h1', 'important', 'anom_logging_execution_time_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(134, 0, 151, 'h1', 'important', 'anom_requests_start_by_hit_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(135, 1, 152, 'h1', 'critical', 'anom_requests_finish_success_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(136, 0, 153, 'h1', 'important', 'anom_requests_finish_exception_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(137, 0, 201, 'h1', 'important', 'anom_success_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(138, 1, 202, 'h1', 'critical', 'anom_success_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(139, 0, 203, 'h1', 'important', 'anom_success_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(140, 0, 204, 'h1', 'important', 'anom_success_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(141, 0, 205, 'h1', 'important', 'anom_success_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(142, 0, 206, 'h1', 'important', 'anom_success_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(143, 0, 301, 'h1', 'important', 'anom_exception_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(144, 0, 302, 'h1', 'important', 'anom_exception_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(145, 0, 303, 'h1', 'important', 'anom_exception_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(146, 0, 304, 'h1', 'important', 'anom_exception_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(147, 0, 305, 'h1', 'important', 'anom_exception_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(148, 0, 306, 'h1', 'important', 'anom_exception_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(149, 1, 1201, 'h1', 'critical', 'anom_success_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(150, 1, 1202, 'h1', 'critical', 'anom_success_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(151, 0, 1203, 'h1', 'important', 'anom_success_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(152, 1, 1204, 'h1', 'critical', 'anom_success_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(153, 0, 1205, 'h1', 'important', 'anom_success_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(154, 1, 1206, 'h1', 'critical', 'anom_success_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(155, 0, 1207, 'h1', 'important', 'anom_success_db_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(156, 0, 1208, 'h1', 'important', 'anom_success_api_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(157, 0, 1209, 'h1', 'important', 'anom_success_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(158, 0, 1210, 'h1', 'important', 'anom_success_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(159, 0, 1301, 'h1', 'important', 'anom_exception_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(160, 0, 1302, 'h1', 'important', 'anom_exception_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(161, 0, 1303, 'h1', 'important', 'anom_exception_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(162, 0, 1304, 'h1', 'important', 'anom_exception_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(163, 0, 1305, 'h1', 'important', 'anom_exception_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(164, 0, 1306, 'h1', 'important', 'anom_exception_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(165, 0, 1307, 'h1', 'important', 'anom_exception_db_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(166, 0, 1308, 'h1', 'important', 'anom_exception_api_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(167, 0, 1309, 'h1', 'important', 'anom_exception_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(168, 0, 1310, 'h1', 'important', 'anom_exception_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(169, 0, 1401, 'h1', 'important', 'anom_success_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(170, 0, 1402, 'h1', 'important', 'anom_success_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(171, 0, 1403, 'h1', 'important', 'anom_success_db_requests_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(172, 0, 1404, 'h1', 'important', 'anom_success_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(173, 0, 1405, 'h1', 'important', 'anom_success_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(174, 0, 1406, 'h1', 'important', 'anom_success_api_requests_time_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(175, 0, 1501, 'h1', 'important', 'anom_exception_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(176, 0, 1502, 'h1', 'important', 'anom_exception_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(177, 0, 1503, 'h1', 'important', 'anom_exception_db_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(178, 0, 1504, 'h1', 'important', 'anom_exception_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(179, 0, 1505, 'h1', 'important', 'anom_exception_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(180, 0, 1506, 'h1', 'important', 'anom_exception_api_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 4),
(181, 0, 1, 'h1', 'important', 'anom_requests_hit_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(182, 1, 2, 'h1', 'critical', 'anom_requests_start_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(183, 0, 3, 'h1', 'important', 'anom_requests_finish_success_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(184, 0, 4, 'h1', 'important', 'anom_requests_finish_exception_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(185, 0, 5, 'h1', 'important', 'anom_system_cpu_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(186, 0, 6, 'h1', 'important', 'anom_system_load_average_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(187, 0, 7, 'h1', 'important', 'anom_system_memory_max_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10);
INSERT INTO `tasks` (`id`, `task_active`, `metric_id`, `granularity`, `message_lvl`, `task_comment`, `task_settings`, `task_robot`, `task_max_execution_sec`, `task_project_id`) VALUES
(188, 0, 8, 'h1', 'important', 'anom_system_memory_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(189, 0, 9, 'h1', 'important', 'anom_system_memory_usage_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(190, 0, 20, 'h1', 'important', 'anom_logging_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(191, 0, 21, 'h1', 'important', 'anom_logging_max_memory_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(192, 0, 22, 'h1', 'important', 'anom_logging_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(193, 0, 23, 'h1', 'important', 'anom_logging_execution_time_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(194, 0, 151, 'h1', 'important', 'anom_requests_start_by_hit_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(195, 1, 152, 'h1', 'critical', 'anom_requests_finish_success_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(196, 0, 153, 'h1', 'important', 'anom_requests_finish_exception_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(197, 0, 201, 'h1', 'important', 'anom_success_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(198, 1, 202, 'h1', 'critical', 'anom_success_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(199, 0, 203, 'h1', 'important', 'anom_success_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(200, 0, 204, 'h1', 'important', 'anom_success_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(201, 0, 205, 'h1', 'important', 'anom_success_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(202, 0, 206, 'h1', 'important', 'anom_success_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(203, 0, 301, 'h1', 'important', 'anom_exception_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(204, 0, 302, 'h1', 'important', 'anom_exception_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(205, 0, 303, 'h1', 'important', 'anom_exception_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(206, 0, 304, 'h1', 'important', 'anom_exception_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(207, 0, 305, 'h1', 'important', 'anom_exception_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(208, 0, 306, 'h1', 'important', 'anom_exception_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(209, 1, 1201, 'h1', 'critical', 'anom_success_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(210, 1, 1202, 'h1', 'critical', 'anom_success_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(211, 0, 1203, 'h1', 'important', 'anom_success_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(212, 1, 1204, 'h1', 'critical', 'anom_success_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(213, 0, 1205, 'h1', 'important', 'anom_success_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(214, 1, 1206, 'h1', 'critical', 'anom_success_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(215, 0, 1207, 'h1', 'important', 'anom_success_db_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(216, 0, 1208, 'h1', 'important', 'anom_success_api_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(217, 0, 1209, 'h1', 'important', 'anom_success_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(218, 0, 1210, 'h1', 'important', 'anom_success_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(219, 0, 1301, 'h1', 'important', 'anom_exception_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(220, 0, 1302, 'h1', 'important', 'anom_exception_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(221, 0, 1303, 'h1', 'important', 'anom_exception_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(222, 0, 1304, 'h1', 'important', 'anom_exception_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(223, 0, 1305, 'h1', 'important', 'anom_exception_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(224, 0, 1306, 'h1', 'important', 'anom_exception_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(225, 0, 1307, 'h1', 'important', 'anom_exception_db_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(226, 0, 1308, 'h1', 'important', 'anom_exception_api_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(227, 0, 1309, 'h1', 'important', 'anom_exception_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(228, 0, 1310, 'h1', 'important', 'anom_exception_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(229, 0, 1401, 'h1', 'important', 'anom_success_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(230, 0, 1402, 'h1', 'important', 'anom_success_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(231, 0, 1403, 'h1', 'important', 'anom_success_db_requests_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(232, 0, 1404, 'h1', 'important', 'anom_success_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(233, 0, 1405, 'h1', 'important', 'anom_success_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(234, 0, 1406, 'h1', 'important', 'anom_success_api_requests_time_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(235, 0, 1501, 'h1', 'important', 'anom_exception_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(236, 0, 1502, 'h1', 'important', 'anom_exception_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(237, 0, 1503, 'h1', 'important', 'anom_exception_db_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(238, 0, 1504, 'h1', 'important', 'anom_exception_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(239, 0, 1505, 'h1', 'important', 'anom_exception_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(240, 0, 1506, 'h1', 'important', 'anom_exception_api_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 10),
(241, 0, 1, 'h1', 'important', 'anom_requests_hit_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(242, 1, 2, 'h1', 'critical', 'anom_requests_start_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(243, 0, 3, 'h1', 'important', 'anom_requests_finish_success_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(244, 0, 4, 'h1', 'important', 'anom_requests_finish_exception_count_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(245, 0, 5, 'h1', 'important', 'anom_system_cpu_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(246, 0, 6, 'h1', 'important', 'anom_system_load_average_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(247, 0, 7, 'h1', 'important', 'anom_system_memory_max_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(248, 0, 8, 'h1', 'important', 'anom_system_memory_usage_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(249, 0, 9, 'h1', 'important', 'anom_system_memory_usage_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(250, 0, 20, 'h1', 'important', 'anom_logging_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(251, 0, 21, 'h1', 'important', 'anom_logging_max_memory_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(252, 0, 22, 'h1', 'important', 'anom_logging_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(253, 0, 23, 'h1', 'important', 'anom_logging_execution_time_by_avg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(254, 0, 151, 'h1', 'important', 'anom_requests_start_by_hit_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(255, 1, 152, 'h1', 'critical', 'anom_requests_finish_success_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(256, 0, 153, 'h1', 'important', 'anom_requests_finish_exception_by_start_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(257, 0, 201, 'h1', 'important', 'anom_success_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(258, 1, 202, 'h1', 'critical', 'anom_success_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(259, 0, 203, 'h1', 'important', 'anom_success_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(260, 0, 204, 'h1', 'important', 'anom_success_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(261, 0, 205, 'h1', 'important', 'anom_success_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(262, 0, 206, 'h1', 'important', 'anom_success_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(263, 0, 301, 'h1', 'important', 'anom_exception_max_memory_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(264, 0, 302, 'h1', 'important', 'anom_exception_execution_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(265, 0, 303, 'h1', 'important', 'anom_exception_db_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(266, 0, 304, 'h1', 'important', 'anom_exception_db_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(267, 0, 305, 'h1', 'important', 'anom_exception_api_requests_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(268, 0, 306, 'h1', 'important', 'anom_exception_api_requests_time_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(269, 1, 1201, 'h1', 'critical', 'anom_success_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(270, 1, 1202, 'h1', 'critical', 'anom_success_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(271, 0, 1203, 'h1', 'important', 'anom_success_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(272, 1, 1204, 'h1', 'critical', 'anom_success_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(273, 0, 1205, 'h1', 'important', 'anom_success_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(274, 1, 1206, 'h1', 'critical', 'anom_success_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(275, 0, 1207, 'h1', 'important', 'anom_success_db_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(276, 0, 1208, 'h1', 'important', 'anom_success_api_requests_time_by_request_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(277, 0, 1209, 'h1', 'important', 'anom_success_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(278, 0, 1210, 'h1', 'important', 'anom_success_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(279, 0, 1301, 'h1', 'important', 'anom_exception_max_memory_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(280, 0, 1302, 'h1', 'important', 'anom_exception_execution_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(281, 0, 1303, 'h1', 'important', 'anom_exception_db_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(282, 0, 1304, 'h1', 'important', 'anom_exception_db_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(283, 0, 1305, 'h1', 'important', 'anom_exception_api_requests_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(284, 0, 1306, 'h1', 'important', 'anom_exception_api_requests_time_by_start_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(285, 0, 1307, 'h1', 'important', 'anom_exception_db_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(286, 0, 1308, 'h1', 'important', 'anom_exception_api_requests_time_by_request_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(287, 0, 1309, 'h1', 'important', 'anom_exception_db_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(288, 0, 1310, 'h1', 'important', 'anom_exception_api_requests_time_by_time_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(289, 0, 1401, 'h1', 'important', 'anom_success_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(290, 0, 1402, 'h1', 'important', 'anom_success_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(291, 0, 1403, 'h1', 'important', 'anom_success_db_requests_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(292, 0, 1404, 'h1', 'important', 'anom_success_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(293, 0, 1405, 'h1', 'important', 'anom_success_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(294, 0, 1406, 'h1', 'important', 'anom_success_api_requests_time_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(295, 0, 1501, 'h1', 'important', 'anom_exception_max_memory_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(296, 0, 1502, 'h1', 'important', 'anom_exception_execution_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(297, 0, 1503, 'h1', 'important', 'anom_exception_db_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(298, 0, 1504, 'h1', 'important', 'anom_exception_db_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(299, 0, 1505, 'h1', 'important', 'anom_exception_api_requests_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12),
(300, 0, 1506, 'h1', 'important', 'anom_exception_api_requests_time_by_alltg_pr_h1', '{\"data\":{\"region_alias\": \"\", \"device_alias\": \"\"}, \"anoms\":{\"direction\": \"both\", \"max_anoms\": 0.2, \"alpha\": 0.01, \"piecewise_median_period_weeks\": 2}}', 'twanom', 240, 12);

-- --------------------------------------------------------

--
-- Структура таблицы `upload_dates`
--

DROP TABLE IF EXISTS `upload_dates`;
CREATE TABLE `upload_dates` (
  `id` int NOT NULL,
  `granularity` varchar(4) NOT NULL DEFAULT 'm1',
  `project_id` int NOT NULL DEFAULT '0',
  `source_id` int NOT NULL DEFAULT '0',
  `dt` datetime NOT NULL DEFAULT '1980-01-01 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `anoms_d1`
--
ALTER TABLE `anoms_d1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`);

--
-- Индексы таблицы `anoms_h1`
--
ALTER TABLE `anoms_h1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`);

--
-- Индексы таблицы `anoms_m1`
--
ALTER TABLE `anoms_m1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`);

--
-- Индексы таблицы `anoms_mo1`
--
ALTER TABLE `anoms_mo1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`);

--
-- Индексы таблицы `anoms_w1`
--
ALTER TABLE `anoms_w1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`);

--
-- Индексы таблицы `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `metrics`
--
ALTER TABLE `metrics`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `metrics_d1`
--
ALTER TABLE `metrics_d1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE;

--
-- Индексы таблицы `metrics_h1`
--
ALTER TABLE `metrics_h1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE;

--
-- Индексы таблицы `metrics_m1`
--
ALTER TABLE `metrics_m1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE;

--
-- Индексы таблицы `metrics_mo1`
--
ALTER TABLE `metrics_mo1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE;

--
-- Индексы таблицы `metrics_w1`
--
ALTER TABLE `metrics_w1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE;

--
-- Индексы таблицы `metric_groups`
--
ALTER TABLE `metric_groups`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `metric_projects`
--
ALTER TABLE `metric_projects`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `tags`
--
ALTER TABLE `tags`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `upload_dates`
--
ALTER TABLE `upload_dates`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `anoms_d1`
--
ALTER TABLE `anoms_d1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `anoms_h1`
--
ALTER TABLE `anoms_h1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `anoms_m1`
--
ALTER TABLE `anoms_m1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `anoms_mo1`
--
ALTER TABLE `anoms_mo1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `anoms_w1`
--
ALTER TABLE `anoms_w1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `metrics`
--
ALTER TABLE `metrics`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1507;

--
-- AUTO_INCREMENT для таблицы `metrics_d1`
--
ALTER TABLE `metrics_d1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `metrics_h1`
--
ALTER TABLE `metrics_h1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `metrics_m1`
--
ALTER TABLE `metrics_m1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `metrics_mo1`
--
ALTER TABLE `metrics_mo1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `metrics_w1`
--
ALTER TABLE `metrics_w1`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `metric_groups`
--
ALTER TABLE `metric_groups`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `metric_projects`
--
ALTER TABLE `metric_projects`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT для таблицы `tags`
--
ALTER TABLE `tags`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=301;

--
-- AUTO_INCREMENT для таблицы `upload_dates`
--
ALTER TABLE `upload_dates`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
