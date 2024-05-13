-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2024-05-13 12:33:20
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
-- 表的结构 `businessowner`
--

CREATE TABLE `businessowner` (
  `id` int(11) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `businessowner`
--

INSERT INTO `businessowner` (`id`, `email`, `company_name`, `name`, `password`, `phone_number`, `city`, `description`) VALUES
(1, 'owner1@example.com', 'ABC Company', 'John Doe', 'password123', 1234567890, 'Shanghai', 'This is a description for owner 1.'),
(2, 'owner2@example.com', 'XYZ Inc.', 'Jane Smith', 'password456', 1987654321, 'Shanghai', 'This is a description for owner 2.');

-- --------------------------------------------------------

--
-- 表的结构 `client`
--

CREATE TABLE `client` (
  `id` int(11) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `client`
--

INSERT INTO `client` (`id`, `email`, `name`, `password`, `phone_number`, `city`) VALUES
(1, 'client1@example.com', 'Alice Johnson', 'password123', 1234567890, 'Shanghai'),
(2, 'client2@example.com', 'Bob Smith', 'password456', 1987654321, 'Shanghai');

-- --------------------------------------------------------

--
-- 表的结构 `events`
--

CREATE TABLE `events` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `description` text DEFAULT NULL,
  `max_ppl` int(11) DEFAULT NULL,
  `current_ppl` int(11) DEFAULT 0,
  `score` float DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `place_id` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `events`
--

INSERT INTO `events` (`id`, `name`, `time`, `description`, `max_ppl`, `current_ppl`, `score`, `price`, `place_id`, `owner_id`) VALUES
(7, 'Concert', '2024-05-20 18:00:00', 'Enjoy a live concert with your friends!', 100, 50, 4, 25, 6, 1),
(8, 'Tour', '2024-06-10 10:00:00', 'Explore stunning views in Yu Garden.', 50, 30, 4, 10, 7, 1),
(9, 'Tour', '2024-07-15 14:00:00', 'Experience the beauty of Jingan Temple.', 20, 10, 5, 50, 9, 1);

-- --------------------------------------------------------

--
-- 表的结构 `follow`
--

CREATE TABLE `follow` (
  `id` int(11) NOT NULL,
  `prime_id` int(11) DEFAULT NULL,
  `following_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `follow`
--

INSERT INTO `follow` (`id`, `prime_id`, `following_id`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- 表的结构 `map`
--

CREATE TABLE `map` (
  `id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `place_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `map`
--

INSERT INTO `map` (`id`, `client_id`, `place_id`) VALUES
(1, 1, 6),
(2, 1, 7),
(3, 1, 8);

-- --------------------------------------------------------

--
-- 表的结构 `participate`
--

CREATE TABLE `participate` (
  `id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `participate`
--

INSERT INTO `participate` (`id`, `client_id`, `event_id`) VALUES
(3, 1, 7),
(4, 1, 8);

-- --------------------------------------------------------

--
-- 表的结构 `place`
--

CREATE TABLE `place` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `location_long` decimal(10,5) DEFAULT NULL,
  `location_lati` decimal(10,5) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `place`
--

INSERT INTO `place` (`id`, `name`, `location_long`, `location_lati`, `city`) VALUES
(6, 'The Bund', '121.48560', '31.23660', 'Shanghai'),
(7, 'Yu Garden', '121.49210', '31.22880', 'Shanghai'),
(8, 'Shanghai Tower', '121.50540', '31.23370', 'Shanghai'),
(9, 'Jingan Temple', '121.44530', '31.22370', 'Shanghai'),
(10, 'Oriental Pearl Tower', '121.49980', '31.23980', 'Shanghai');

-- --------------------------------------------------------

--
-- 表的结构 `review`
--

CREATE TABLE `review` (
  `id` int(11) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `rating` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `review`
--

INSERT INTO `review` (`id`, `event_id`, `client_id`, `content`, `rating`) VALUES
(1, 9, 1, 'I thoroughly enjoyed my visit to Jing\'an Temple. The serene atmosphere and stunning architecture provided a peaceful escape from the bustling city. Highly recommended!', 5);

--
-- 转储表的索引
--

--
-- 表的索引 `businessowner`
--
ALTER TABLE `businessowner`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- 表的索引 `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- 表的索引 `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `place_id` (`place_id`),
  ADD KEY `owner_id` (`owner_id`);

--
-- 表的索引 `follow`
--
ALTER TABLE `follow`
  ADD PRIMARY KEY (`id`),
  ADD KEY `prime_id` (`prime_id`),
  ADD KEY `following_id` (`following_id`);

--
-- 表的索引 `map`
--
ALTER TABLE `map`
  ADD PRIMARY KEY (`id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `place_id` (`place_id`);

--
-- 表的索引 `participate`
--
ALTER TABLE `participate`
  ADD PRIMARY KEY (`id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `event_id` (`event_id`);

--
-- 表的索引 `place`
--
ALTER TABLE `place`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`),
  ADD KEY `client_id` (`client_id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `businessowner`
--
ALTER TABLE `businessowner`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `client`
--
ALTER TABLE `client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- 使用表AUTO_INCREMENT `follow`
--
ALTER TABLE `follow`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用表AUTO_INCREMENT `map`
--
ALTER TABLE `map`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用表AUTO_INCREMENT `participate`
--
ALTER TABLE `participate`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用表AUTO_INCREMENT `place`
--
ALTER TABLE `place`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用表AUTO_INCREMENT `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 限制导出的表
--

--
-- 限制表 `events`
--
ALTER TABLE `events`
  ADD CONSTRAINT `events_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `place` (`id`),
  ADD CONSTRAINT `events_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `businessowner` (`id`);

--
-- 限制表 `follow`
--
ALTER TABLE `follow`
  ADD CONSTRAINT `follow_ibfk_1` FOREIGN KEY (`prime_id`) REFERENCES `businessowner` (`id`),
  ADD CONSTRAINT `follow_ibfk_2` FOREIGN KEY (`following_id`) REFERENCES `client` (`id`);

--
-- 限制表 `map`
--
ALTER TABLE `map`
  ADD CONSTRAINT `map_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  ADD CONSTRAINT `map_ibfk_2` FOREIGN KEY (`place_id`) REFERENCES `place` (`id`);

--
-- 限制表 `participate`
--
ALTER TABLE `participate`
  ADD CONSTRAINT `participate_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  ADD CONSTRAINT `participate_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`);

--
-- 限制表 `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
