-- MySQL dump 10.16  Distrib 10.1.23-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: SmartTrainer
-- ------------------------------------------------------
-- Server version	10.1.23-MariaDB-9+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings` (
  `nodes` int(11) DEFAULT NULL,
  `rounds` int(11) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  `delay` int(11) DEFAULT NULL,
  `program` varchar(30) DEFAULT NULL,
  `sleep` int(11) DEFAULT NULL,
  `sets` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (3,15,30,700,'default',10,1),(0,0,100,0,'program_1',NULL,NULL),(0,0,100,0,'program_2',NULL,NULL);
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_5105_highscore`
--

DROP TABLE IF EXISTS `tbl_5105_highscore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_5105_highscore` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PlayerName` varchar(100) DEFAULT NULL,
  `time` datetime DEFAULT CURRENT_TIMESTAMP,
  `TotalTime` float(6,4) DEFAULT NULL,
  `Time_1` decimal(6,4) DEFAULT NULL,
  `Time_2` decimal(6,4) DEFAULT NULL,
  `Time_3` decimal(6,4) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_5105_highscore`
--

LOCK TABLES `tbl_5105_highscore` WRITE;
/*!40000 ALTER TABLE `tbl_5105_highscore` DISABLE KEYS */;
INSERT INTO `tbl_5105_highscore` VALUES (1,'makkan','2018-12-22 11:58:30',11.3680,3.6030,4.8530,2.9090),(2,'tony','2018-12-22 11:59:39',8.2300,2.2630,3.7470,2.2170),(3,'tony','2018-12-22 12:12:37',7.5340,2.7420,3.1090,1.6810);
/*!40000 ALTER TABLE `tbl_5105_highscore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_times`
--

DROP TABLE IF EXISTS `tbl_times`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_times` (
  `Player` varchar(255) DEFAULT NULL,
  `Rounds` int(11) DEFAULT NULL,
  `Total_time` varchar(255) DEFAULT NULL,
  `T1` varchar(255) DEFAULT NULL,
  `T2` varchar(255) DEFAULT NULL,
  `T3` varchar(255) DEFAULT NULL,
  `T4` varchar(255) DEFAULT NULL,
  `T5` varchar(255) DEFAULT NULL,
  `T6` varchar(255) DEFAULT NULL,
  `T7` varchar(255) DEFAULT NULL,
  `T8` varchar(255) DEFAULT NULL,
  `T9` varchar(255) DEFAULT NULL,
  `T10` varchar(255) DEFAULT NULL,
  `T11` varchar(255) DEFAULT NULL,
  `T12` varchar(255) DEFAULT NULL,
  `T13` varchar(255) DEFAULT NULL,
  `T14` varchar(255) DEFAULT NULL,
  `T15` varchar(255) DEFAULT NULL,
  `T16` varchar(255) DEFAULT NULL,
  `T17` varchar(255) DEFAULT NULL,
  `T18` varchar(255) DEFAULT NULL,
  `T19` varchar(255) DEFAULT NULL,
  `T20` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_times`
--

LOCK TABLES `tbl_times` WRITE;
/*!40000 ALTER TABLE `tbl_times` DISABLE KEYS */;
INSERT INTO `tbl_times` VALUES ('Zlatan',15,'10.0','1.190000','1.581000','1.125000','1.171000','1.063000','1.019000','2.737000','1.428000','1.780000','1.981000','1.679000','1.086000','1.021000','1.818000','1.030000','0','0','0','0','0.5');
/*!40000 ALTER TABLE `tbl_times` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_user`
--

DROP TABLE IF EXISTS `tbl_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) DEFAULT NULL,
  `user_username` varchar(45) DEFAULT NULL,
  `user_password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_user`
--

LOCK TABLES `tbl_user` WRITE;
/*!40000 ALTER TABLE `tbl_user` DISABLE KEYS */;
INSERT INTO `tbl_user` VALUES (1,'1','2','pbkdf2:sha256:50000$'),(2,'Herman Johnsson','herman.johnsson93@gm','pbkdf2:sha256:50000$');
/*!40000 ALTER TABLE `tbl_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-22 13:04:44
