-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 25, 2018 at 09:52 AM
-- Server version: 10.1.30-MariaDB
-- PHP Version: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ebloodbank`
--

-- --------------------------------------------------------

--
-- Table structure for table `blood_center`
--

CREATE TABLE `blood_center` (
  `id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `address` varchar(60) NOT NULL,
  `email_address` varchar(50) DEFAULT NULL,
  `telephone_number` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `blood_center`
--

INSERT INTO `blood_center` (`id`, `account_id`, `name`, `address`, `email_address`, `telephone_number`) VALUES
(1, 0, 'Philippine Red Cross - Cavite Chapter', 'Samonte Park, San Roque Cavite City', 'nbs.recruitment@redcross.org.ph', '(046) 431-0562');

-- --------------------------------------------------------

--
-- Table structure for table `blood_donation`
--

CREATE TABLE `blood_donation` (
  `id` int(11) NOT NULL,
  `blood_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `phlebotomist` int(11) DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL,
  `transaction_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `blood_purchase`
--

CREATE TABLE `blood_purchase` (
  `id` int(11) NOT NULL,
  `blood_id` int(11) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `seller_id` int(11) DEFAULT NULL,
  `date_purchased` date NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `blood_request`
--

CREATE TABLE `blood_request` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `hospital_id` int(11) DEFAULT NULL,
  `patient` varchar(50) NOT NULL,
  `quantity` int(11) NOT NULL,
  `blood_group` char(3) NOT NULL,
  `purpose` varchar(30) DEFAULT NULL,
  `date_created` datetime NOT NULL,
  `date_processed` datetime NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `blood_resource`
--

CREATE TABLE `blood_resource` (
  `id` int(11) NOT NULL,
  `blood_group` char(3) NOT NULL,
  `bag_type` varchar(10) NOT NULL,
  `event_id` int(11) NOT NULL,
  `center_id` int(11) NOT NULL,
  `extraction_date` datetime NOT NULL,
  `cost` decimal(6,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event_information`
--

CREATE TABLE `event_information` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  `venue` varchar(60) NOT NULL,
  `event_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event_participate`
--

CREATE TABLE `event_participate` (
  `id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_account`
--

CREATE TABLE `user_account` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `date_created` datetime NOT NULL,
  `last_active` datetime NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_account`
--

INSERT INTO `user_account` (`id`, `user_id`, `role_id`, `username`, `password`, `date_created`, `last_active`, `status`) VALUES
(1, 0, 1, 'admin', 'a', '2018-07-06 00:00:00', '2018-07-06 00:00:00', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `user_address`
--

CREATE TABLE `user_address` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `house_no` int(11) DEFAULT NULL,
  `street` varchar(30) DEFAULT NULL,
  `barangay` varchar(30) DEFAULT NULL,
  `town_municipality` varchar(20) DEFAULT NULL,
  `province_city` varchar(20) DEFAULT NULL,
  `zip_code` int(11) NOT NULL,
  `type` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_contact`
--

CREATE TABLE `user_contact` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `telephone_no` varchar(20) DEFAULT NULL,
  `mobile_no` varchar(15) DEFAULT NULL,
  `email_address` varchar(50) DEFAULT NULL,
  `is_donor` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_personal`
--

CREATE TABLE `user_personal` (
  `id` int(11) NOT NULL,
  `surname` varchar(20) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(20) DEFAULT NULL,
  `birth_date` date NOT NULL,
  `blood_group` char(3) NOT NULL,
  `civil_status` char(1) NOT NULL,
  `gender` char(1) NOT NULL,
  `nationality` varchar(10) NOT NULL,
  `religion` varchar(30) DEFAULT NULL,
  `education` varchar(30) DEFAULT NULL,
  `occupation` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_role`
--

CREATE TABLE `user_role` (
  `id` int(11) NOT NULL,
  `name` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_role`
--

INSERT INTO `user_role` (`id`, `name`) VALUES
(1, 'admin_main'),
(2, 'admin_hospital'),
(3, 'seeker/donor'),
(4, 'phlebotomist'),
(5, 'volunteer'),
(6, 'event');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `blood_center`
--
ALTER TABLE `blood_center`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `blood_donation`
--
ALTER TABLE `blood_donation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `blood_purchase`
--
ALTER TABLE `blood_purchase`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `blood_request`
--
ALTER TABLE `blood_request`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `blood_resource`
--
ALTER TABLE `blood_resource`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_information`
--
ALTER TABLE `event_information`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_participate`
--
ALTER TABLE `event_participate`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_account`
--
ALTER TABLE `user_account`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_address`
--
ALTER TABLE `user_address`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_contact`
--
ALTER TABLE `user_contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_personal`
--
ALTER TABLE `user_personal`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_role`
--
ALTER TABLE `user_role`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `blood_center`
--
ALTER TABLE `blood_center`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `blood_donation`
--
ALTER TABLE `blood_donation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blood_resource`
--
ALTER TABLE `blood_resource`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `event_information`
--
ALTER TABLE `event_information`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user_account`
--
ALTER TABLE `user_account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user_address`
--
ALTER TABLE `user_address`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user_contact`
--
ALTER TABLE `user_contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user_personal`
--
ALTER TABLE `user_personal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user_role`
--
ALTER TABLE `user_role`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
