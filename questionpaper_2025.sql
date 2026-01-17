-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 10, 2025 at 09:20 AM
-- Server version: 8.3.0
-- PHP Version: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `questionpaper_2025`
--

-- --------------------------------------------------------

--
-- Table structure for table `questionpaper_2025_data`
--

DROP TABLE IF EXISTS `questionpaper_2025_data`;
CREATE TABLE IF NOT EXISTS `questionpaper_2025_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(255) NOT NULL,
  `user` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `directory` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `questionpaper_2025_data`
--

INSERT INTO `questionpaper_2025_data` (`id`, `uid`, `user`, `username`, `directory`) VALUES
(1, 'uid_IYG6GnQIX5', 'user@user.com', 'user', 'uid_i7soaylnSs'),
(2, 'uid_2hYaORWr1v', 'user@user.com', 'user', 'uid_q7ajCsCPDi');

-- --------------------------------------------------------

--
-- Table structure for table `questionpaper_2025_user`
--

DROP TABLE IF EXISTS `questionpaper_2025_user`;
CREATE TABLE IF NOT EXISTS `questionpaper_2025_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `questionpaper_2025_user`
--

INSERT INTO `questionpaper_2025_user` (`id`, `uid`, `name`, `email`, `password`, `phone`) VALUES
(1, 'uid_jHH7mrOZUl', 'user', 'user@user.com', 'user', '9876543210');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
