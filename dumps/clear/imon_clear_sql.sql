-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: mysql:3306
-- Время создания: Сен 01 2025 г., 19:41
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

DROP TABLE IF EXISTS `anoms_d1`;
CREATE TABLE `anoms_d1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `metric_value` int NOT NULL,
  `posted` int NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `direction` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_group_id` int NOT NULL DEFAULT '0',
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
  `metric_value` int NOT NULL,
  `posted` int NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `direction` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_group_id` int NOT NULL DEFAULT '0',
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
  `metric_value` int NOT NULL,
  `posted` int NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `direction` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_group_id` int NOT NULL DEFAULT '0',
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
  `metric_value` int NOT NULL,
  `posted` int NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `direction` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_group_id` int NOT NULL DEFAULT '0',
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
  `metric_value` int NOT NULL,
  `posted` int NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `direction` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_group_id` int NOT NULL DEFAULT '0',
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
  `job_comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `metrics`
--

DROP TABLE IF EXISTS `metrics`;
CREATE TABLE `metrics` (
  `id` int NOT NULL,
  `parentid` int NOT NULL,
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

-- --------------------------------------------------------

--
-- Структура таблицы `metrics_d1`
--

DROP TABLE IF EXISTS `metrics_d1`;
CREATE TABLE `metrics_d1` (
  `id` int NOT NULL,
  `dt` datetime(6) NOT NULL,
  `source_id` int NOT NULL DEFAULT '0',
  `source_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(199) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `metric_group_id` int NOT NULL DEFAULT '0',
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
  `source_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(199) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `metric_group_id` int NOT NULL DEFAULT '0',
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
  `source_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(199) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `metric_group_id` int NOT NULL DEFAULT '0',
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
  `source_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(199) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `metric_group_id` int NOT NULL DEFAULT '0',
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
  `source_alias` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_id` int NOT NULL,
  `metric_parentid` int NOT NULL DEFAULT '0',
  `value` bigint NOT NULL,
  `dp` smallint NOT NULL DEFAULT '0',
  `region_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `device_alias` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `trafsrc_alias` varchar(199) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'all',
  `metric_group_id` int NOT NULL DEFAULT '0',
  `metric_project_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `metric_project_alias` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `metric_project_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `metric_projects`
--

INSERT INTO `metric_projects` (`id`, `metric_project_alias`, `metric_project_name`) VALUES
(1, 'project1', 'Project 1'),
(2, 'project2', 'Project 2'),
(3, 'project3', 'Project 3');

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
  `task_max_execution_sec` int NOT NULL DEFAULT '240'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  ADD KEY `dt` (`dt`);

--
-- Индексы таблицы `metrics_h1`
--
ALTER TABLE `metrics_h1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`);

--
-- Индексы таблицы `metrics_m1`
--
ALTER TABLE `metrics_m1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`);

--
-- Индексы таблицы `metrics_mo1`
--
ALTER TABLE `metrics_mo1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`);

--
-- Индексы таблицы `metrics_w1`
--
ALTER TABLE `metrics_w1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dt` (`dt`);

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
-- Индексы таблицы `tasks`
--
ALTER TABLE `tasks`
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
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
