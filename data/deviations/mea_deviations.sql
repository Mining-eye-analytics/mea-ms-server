CREATE DATABASE  IF NOT EXISTS `mea_deviations` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `mea_deviations`;
-- MySQL dump 10.13  Distrib 8.0.33, for macos13 (arm64)
--
-- Host: 10.10.10.66    Database: mea_deviations
-- ------------------------------------------------------
-- Server version	5.7.42-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('ab28fb9ed503');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crossing_counting`
--

DROP TABLE IF EXISTS `crossing_counting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crossing_counting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `realtime_images_id` int(11) NOT NULL,
  `type_object` varchar(100) NOT NULL,
  `count` int(11) DEFAULT NULL,
  `track_id` int(11) DEFAULT NULL,
  `direction` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `crossing_counting_ibfk_1` (`realtime_images_id`),
  CONSTRAINT `crossing_counting_ibfk_1` FOREIGN KEY (`realtime_images_id`) REFERENCES `realtime_images` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=87886 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crossing_counting`
--

LOCK TABLES `crossing_counting` WRITE;
/*!40000 ALTER TABLE `crossing_counting` DISABLE KEYS */;
/*!40000 ALTER TABLE `crossing_counting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `realtime_deviations`
--

DROP TABLE IF EXISTS `realtime_deviations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `realtime_deviations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `realtime_images_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `type_validation` enum('not_yet','true','false') NOT NULL DEFAULT 'not_yet',
  `type_object` varchar(100) NOT NULL,
  `violate_count` int(11) DEFAULT NULL,
  `comment` varchar(250) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `realtime_deviations_ibfk_1` (`parent_id`),
  KEY `realtime_deviations_ibfk_2` (`realtime_images_id`),
  CONSTRAINT `realtime_deviations_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `realtime_deviations` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `realtime_deviations_ibfk_2` FOREIGN KEY (`realtime_images_id`) REFERENCES `realtime_images` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=487561 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `realtime_deviations`
--

LOCK TABLES `realtime_deviations` WRITE;
/*!40000 ALTER TABLE `realtime_deviations` DISABLE KEYS */;
/*!40000 ALTER TABLE `realtime_deviations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `realtime_images`
--

DROP TABLE IF EXISTS `realtime_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `realtime_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cctv_id` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `avg_panjang_bbox_hd` float DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=576887 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `realtime_images`
--

LOCK TABLES `realtime_images` WRITE;
/*!40000 ALTER TABLE `realtime_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `realtime_images` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-17 19:42:29
