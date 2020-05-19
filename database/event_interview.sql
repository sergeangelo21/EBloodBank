-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 03, 2018 at 04:14 AM
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
-- Table structure for table `event_interview`
--

CREATE TABLE `event_interview` (
  `id` int(11) NOT NULL,
  `question` varchar(100) NOT NULL,
  `header` varchar(30) DEFAULT NULL,
  `answer` char(1) NOT NULL,
  `control` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `event_interview`
--

INSERT INTO `event_interview` (`id`, `question`, `header`, `answer`, `control`) VALUES
(1, 'Do you feel well and healthy today?', NULL, 'Y', 1),
(2, 'In the past 4 WEEKS have you taken any medications and/or vaccinations', NULL, 'N', 1),
(3, 'In the past 3 DAYS have you taken aspirin', NULL, 'N', 1),
(4, 'Donated whole blood, platelets or plasma?', 'IN THE PAST 3 MONTHS HAVE YOU:', 'N', 1),
(5, 'Received blood, blood products and/or had tissue/organ transplant or graft?', 'IN THE PAST 12 MONTHS HAVE YOU', 'N', 1),
(6, 'Had surgical operation or dental extraction?', 'IN THE PAST 12 MONTHS HAVE YOU', 'N', 1),
(7, 'Had a tattoo applied, ear and body piercing, acupuncture, needle stick injury or accidental contact ', 'IN THE PAST 12 MONTHS HAVE YOU', 'N', 1),
(8, 'Had sexual contact with high risks individuals or in exchange for material or monetary gain?', 'IN THE PAST 12 MONTHS HAVE YOU', 'N', 1),
(9, 'Engaged in unprotected, unsafe or casual sex?', 'IN THE PAST 12 MONTHS HAVE YOU', 'N', 1),
(10, 'Had jaundice/hepatitis/personal contact with person who had hepatitis?', 'IN THE PAST 12 MONTHS HAVE YOU', 'N', 1),
(11, 'Been incarcerated, jailed or imprisoned?', 'IN THE PAST 12 MONTHS HAVE YOU', 'N', 1),
(12, 'Spent time or have relatives in the United Kingdom or Europe?', 'IN THE PAST 12 MONTHS HAVE YOU', 'N', 1),
(13, 'Travelled or lived-in outside of your place of residence of the Philippines?', 'HAVE YOU EVER:', 'N', 1),
(14, 'Taken prohibited drugs (orally, by nose, or by injection)?', 'HAVE YOU EVER:', 'N', 1),
(15, 'Use clotting factor concentrates?', 'HAVE YOU EVER:', 'N', 1),
(16, 'Had a positive test for the HIV virus, Hepatitis virus, Syphilis and Malaria?', 'HAVE YOU EVER:', 'N', 1),
(17, 'Had Malariia or Hepatitis in the past?', 'HAVE YOU EVER:', 'N', 1),
(18, 'Had or was treated for genital wart, syphilis, gonorhea or other sexually transmitted diseases?', 'HAVE YOU EVER:', 'N', 1),
(19, 'Cancer, Blood disease or bleeding disorder haemophilia?', 'HAD ANY OF THE FOLLOWING:', 'N', 1),
(20, 'Heart disease/surgery, rheumatic fever or chest pain?', 'HAD ANY OF THE FOLLOWING:', 'N', 1),
(21, 'Lung disease, tuberculosis or asthma?', 'HAD ANY OF THE FOLLOWING:', 'N', 1),
(22, 'Kidney disease, thyroid disease, diabetes, epilepsy?', 'HAD ANY OF THE FOLLOWING:', 'N', 1),
(23, 'Chicken pox and/or cold sores?', 'HAD ANY OF THE FOLLOWING:', 'N', 1),
(24, 'Any other chronic medical condition or surgical operations?', 'HAD ANY OF THE FOLLOWING:', 'N', 1),
(25, 'Had rash and/or fever? Was/Were this/these also associated with arthralgia or arthritis or conjuncti', 'HAVE YOU RECENTLY:', 'N', 1),
(26, 'Been to any places in the Philippines or countries infected with ZIKA Virus?', 'IN THE PAST 6 MONTHS HAVE YOU', 'N', 1),
(27, 'Had sexual contact with a person who was confirmed to ZIKA Virus infection?', 'IN THE PAST 6 MONTHS HAVE YOU', 'N', 1),
(28, 'Had sexual contact with a person who has been to any places in the Philippines or countries infected', 'IN THE PAST 6 MONTHS HAVE YOU', 'N', 1),
(29, 'Are you giving blood only because you want to be tested to HIV/AIDS virus or Hepatitis virus?', 'IN THE PAST 6 MONTHS HAVE YOU', 'N', 1),
(30, 'Are you aware that an HIV/Hepattitis infected person can still transmit the virus despite a negative', 'IN THE PAST 6 MONTHS HAVE YOU', 'N', 1),
(31, 'Have you within the last 12 HOURS had taken liquor, beer or any drinks with alcohol?', 'IN THE PAST 6 MONTHS HAVE YOU', 'N', 1),
(32, 'Have you ever been refused as a blood donor or told not to donate blood for any reasons?', 'IN THE PAST 6 MONTHS HAVE YOU', 'N', 1),
(33, 'Are you currently pregnant?', 'FOR FEMALE DONORS ONLY', 'N', 1),
(34, 'Have you ever been pregnant?', 'FOR FEMALE DONORS ONLY', 'N', 1),
(35, 'When was your last delivery?', 'FOR FEMALE DONORS ONLY', 'N', 2),
(36, 'Did you have an abortion in the past 1 YEAR?', 'FOR FEMALE DONORS ONLY', 'N', 1),
(37, 'When was your last menstrual period?', 'FOR FEMALE DONORS ONLY', 'N', 2),
(38, 'Are you currently breastfeeding?', 'FOR FEMALE DONORS ONLY', 'N', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `event_interview`
--
ALTER TABLE `event_interview`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `event_interview`
--
ALTER TABLE `event_interview`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
