-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2024-03-22 05:18:08
-- 服务器版本： 10.4.20-MariaDB
-- PHP 版本： 8.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `software_engineering`
--

-- --------------------------------------------------------

--
-- 表的结构 `place`
--

CREATE TABLE `place` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `longitude` double(15,10) NOT NULL,
  `latitude` double(15,10) NOT NULL,
  `city` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `place`
--

INSERT INTO `place` (`id`, `name`, `longitude`, `latitude`, `city`, `created_at`) VALUES
(1, 'Central Park', 40.7850910000, -73.9682850000, 'New York', '2024-03-22 04:04:23'),
(2, 'Eiffel Tower', 48.8583720000, 2.2944810000, 'Paris', '2024-03-22 04:04:23'),
(3, 'Sydney Opera House', -33.8567840000, 151.2152960000, 'Sydney', '2024-03-22 04:04:23'),
(4, 'The Bund', 31.2392030000, 121.4977320000, 'Shanghai', '2024-03-22 04:08:37'),
(5, 'Yu Garden', 31.2277000000, 121.4923000000, 'Shanghai', '2024-03-22 04:08:37'),
(6, 'Shanghai Tower', 31.2337000000, 121.5050000000, 'Shanghai', '2024-03-22 04:08:37'),
(7, 'Nanjing Road', 31.2340000000, 121.4747000000, 'Shanghai', '2024-03-22 04:08:37'),
(8, 'Oriental Pearl Tower', 31.2423000000, 121.4958000000, 'Shanghai', '2024-03-22 04:08:37');

--
-- 转储表的索引
--

--
-- 表的索引 `place`
--
ALTER TABLE `place`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `place`
--
ALTER TABLE `place`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
