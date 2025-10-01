-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 14, 2023 at 01:54 PM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 7.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bms`
--

-- --------------------------------------------------------

--
-- Table structure for table `bankguarantee`
--

CREATE TABLE `bankguarantee` (
  `sid` int(11) NOT NULL,
  `unitname` varchar(50) NOT NULL,
  `unitemail` varchar(50) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `unitaddress` varchar(6000) NOT NULL,
  `unitnumber` varchar(12) NOT NULL,
  `bankheadname` varchar(50) NOT NULL,
  `bankname` varchar(50) NOT NULL,
  `bankemailid` varchar(50) NOT NULL,
  `bankphonenumber` varchar(20) NOT NULL,
  `bankaddress` varchar(6000) NOT NULL,
  `bgnumber` varchar(20) NOT NULL,
  `bgdate` varchar(20) NOT NULL,
  `stampnumber` varchar(20) NOT NULL,
  `validperiod` varchar(20) NOT NULL,
  `claimperiod` varchar(20) NOT NULL,
  `amount` decimal(20,0) NOT NULL,
  `accountnumber` varchar(20) NOT NULL,
  `securityvalue` decimal(20,0) NOT NULL,
  `submitdate` varchar(20) NOT NULL,
  `renewaldate` varchar(20) NOT NULL,
  `claimamount` decimal(20,0) NOT NULL,
  `zonalbankname` varchar(50) NOT NULL,
  `zonalofficemail` varchar(75) NOT NULL,
  `zocontactprsnname` varchar(50) NOT NULL,
  `zophonenumber` varchar(50) NOT NULL,
  `zoaddress` varchar(600) NOT NULL,
  `renewalprocessed` varchar(10) NOT NULL,
  `zoprocessed` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bankguarantee`
--

INSERT INTO `bankguarantee` (`sid`, `unitname`, `unitemail`, `gender`, `unitaddress`, `unitnumber`, `bankheadname`, `bankname`, `bankemailid`, `bankphonenumber`, `bankaddress`, `bgnumber`, `bgdate`, `stampnumber`, `validperiod`, `claimperiod`, `amount`, `accountnumber`, `securityvalue`, `submitdate`, `renewaldate`, `claimamount`, `zonalbankname`, `zonalofficemail`, `zocontactprsnname`, `zophonenumber`, `zoaddress`, `renewalprocessed`, `zoprocessed`) VALUES
(711, 'CHITTI BABU', 'chitti.chindirala@gmail.com', 'male', '#45, 12th corss, 22nd Main, RaghavendraLayout, Padmanabhanagar', '9844705446', 'Dr.Shekar', 'UNION BANK', '9900087613', '#71', '#71, BASKIII Stage, Padmanabhanagar', '123456789', '03-11-2023', '986754321', '03-11-2023', '5-1-2024', '10000', '0602002100319130', '100000', '3-11-2023', '17-05-2023', '1000000', 'SBI bank', 'sbi@gmail.com', 'Mr Ramana', '9876543210', '#31,  1st floor,  6th main,  Padmanabhanagar', 'No', 'No'),
(712, 'sindhu', 'sindhujachindirala@gmail.com', 'female', '#45, 12th corss, 22nd Main, RaghavendraLayout, Padmanabhanagar', '8971466297', 'Dr.Shekar suri', 'KOTAK BANK', '9900087613', '#71', '#71, BASKIII Stage, Padmanabhanagar', '123456789', '03-11-2023', '986754321', '03-11-2023', '5-1-2024', '10000', '0602002100319130', '100000', '3-11-2023', '5-1-2024', '1000000', 'SBI bank', 'sbi@gmail.com', 'Mr Ramana', '9876543210', '#31,  1st floor,  6th main,  Padmanabhanagar', 'No', 'No'),
(713, 'Mr.Raju', 'Mr.Raju@gmail.com', 'female', '#45, 12th corss, 22nd Main, RaghavendraLayout, Padmanabhanagar', '8971466297', 'Dr.Sathish', 'SBI BANK', '9900087613', '#71', '#71, BASKIII Stage, Padmanabhanagar', '123456789', '03-11-2023', '986754321', '03-11-2023', '5-1-2024', '10000', '0602002100319130', '100000', '3-11-2023', '5-1-2024', '1000000', 'SBI bank', 'sbi@gmail.com', 'Mr Ramana', '9876543210', '#31,  1st floor,  6th main,  Padmanabhanagar', 'No', 'No'),
(714, 'Mr.Mahesh', 'Mr.Mahesh@gmail.com', 'male', '#45, 12th corss, 22nd Main, RaghavendraLayout, Padmanabhanagar', '8971466297', 'Dr.prabhakar', 'YES BANK', '9900087613', '#71', '#71, BASKIII Stage, Padmanabhanagar', '123456789', '03-11-2023', '986754321', '03-11-2023', '5-1-2024', '10000', '0602002100319130', '100000', '3-11-2023', '5-1-2024', '1000000', 'SBI bank', 'sbi@gmail.com', 'Mr Ramana', '9876543210', '#31,  1st floor,  6th main,  Padmanabhanagar', 'No', 'No'),
(715, 'Mr.Kumar', 'Mr.Kumar@gmail.com', 'female', '#45, 12th corss, 22nd Main, RaghavendraLayout, Padmanabhanagar', '9765432145', 'Dr.Murali', 'ICICI BANK', '9900087613', '#71', '#71, BASKIII Stage, Padmanabhanagar', '123456789', '03-11-2023', '986754321', '03-11-2023', '5-1-2024', '10000', '0602002100319130', '100000', '3-11-2023', '5-1-2024', '1000000', 'SBI bank', 'sbi@gmail.com', 'Mr Ramana', '9876543210', '#31,  1st floor,  6th main,  Padmanabhanagar', 'No', 'No'),
(716, 'Mr.Sekhar', 'Mr.Sekhar@gmail.com', 'male', '#45, 12th corss, 22nd Main, RaghavendraLayout, Padmanabhanagar', '8971466297', 'Dr.Kiran', 'SRI CHARAN BANK', '9900087613', '#71', '#71, BASKIII Stage, Padmanabhanagar', '123456789', '03-11-2023', '986754321', '03-11-2023', '5-1-2024', '10000', '0602002100319130', '100000', '3-11-2023', '5-1-2024', '1000000', 'SBI bank', 'sbi@gmail.com', 'Mr Ramana', '9876543210', '#31,  1st floor,  6th main,  Padmanabhanagar', 'No', 'No');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
(15, 'rcreddy', 'rcreddy@gmail.com', 'pbkdf2:sha256:260000$iOLjf76Ym08kun5P$3c6cc3a8afab91e5e2c7e9ac8ac5ebff5803355cbbfed6abf733b114c93a7b6d');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bankguarantee`
--
ALTER TABLE `bankguarantee`
  ADD PRIMARY KEY (`sid`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bankguarantee`
--
ALTER TABLE `bankguarantee`
  MODIFY `sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=717;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
