-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Apr 25, 2017 at 04:20 PM
-- Server version: 5.7.17-0ubuntu0.16.04.1
-- PHP Version: 7.0.15-0ubuntu0.16.04.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `PiCamYoutube`
--

-- --------------------------------------------------------

--
-- Table structure for table `VideoData`
--

CREATE TABLE `VideoData` (
  `INDEX` int(11) NOT NULL,
  `DATEANDTIME` datetime NOT NULL,
  `VIDEONAME` varchar(500) NOT NULL,
  `CAMERAID` varchar(25) NOT NULL,
  `UPLOADED` tinyint(1) NOT NULL,
  `UPLOADATTEMPTS` int(11) NOT NULL DEFAULT '0',
  `UPLOADRESULT` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `VideoData`
--
ALTER TABLE `VideoData`
  ADD PRIMARY KEY (`INDEX`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `VideoData`
--
ALTER TABLE `VideoData`
  MODIFY `INDEX` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

