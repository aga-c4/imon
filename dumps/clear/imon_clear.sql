-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: mysql-svc.mysql.svc.cluster.local:3306
-- Время создания: Окт 07 2025 г., 10:25
-- Версия сервера: 9.4.0
-- Версия PHP: 8.2.27

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
) ENGINE=InnoDB AUTO_INCREMENT=1507 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=47361 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=243333 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1909947 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7022 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  KEY `dt` (`dt`,`metric_project_id`,`metric_tag_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=16289 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `last_dt_gen_use` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `tags`
--

CREATE TABLE IF NOT EXISTS `tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL DEFAULT '0',
  `tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=349 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
