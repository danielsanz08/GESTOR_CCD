-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ccd
-- ------------------------------------------------------
-- Server version	8.4.3

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add custom user',6,'add_customuser'),(22,'Can change custom user',6,'change_customuser'),(23,'Can delete custom user',6,'delete_customuser'),(24,'Can view custom user',6,'view_customuser'),(25,'Can add articulo',7,'add_articulo'),(26,'Can change articulo',7,'change_articulo'),(27,'Can delete articulo',7,'delete_articulo'),(28,'Can view articulo',7,'view_articulo'),(29,'Can add pedido articulo',8,'add_pedidoarticulo'),(30,'Can change pedido articulo',8,'change_pedidoarticulo'),(31,'Can delete pedido articulo',8,'delete_pedidoarticulo'),(32,'Can view pedido articulo',8,'view_pedidoarticulo'),(33,'Can add pedido',9,'add_pedido'),(34,'Can change pedido',9,'change_pedido'),(35,'Can delete pedido',9,'delete_pedido'),(36,'Can view pedido',9,'view_pedido');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_libreria_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_libreria_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `libreria_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(6,'libreria','customuser'),(7,'papeleria','articulo'),(9,'papeleria','pedido'),(8,'papeleria','pedidoarticulo'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-05-27 00:55:17.471416'),(2,'contenttypes','0002_remove_content_type_name','2025-05-27 00:55:17.770574'),(3,'auth','0001_initial','2025-05-27 00:55:18.734137'),(4,'auth','0002_alter_permission_name_max_length','2025-05-27 00:55:18.963735'),(5,'auth','0003_alter_user_email_max_length','2025-05-27 00:55:18.983706'),(6,'auth','0004_alter_user_username_opts','2025-05-27 00:55:19.008721'),(7,'auth','0005_alter_user_last_login_null','2025-05-27 00:55:19.024368'),(8,'auth','0006_require_contenttypes_0002','2025-05-27 00:55:19.031214'),(9,'auth','0007_alter_validators_add_error_messages','2025-05-27 00:55:19.064480'),(10,'auth','0008_alter_user_username_max_length','2025-05-27 00:55:19.079485'),(11,'auth','0009_alter_user_last_name_max_length','2025-05-27 00:55:19.094332'),(12,'auth','0010_alter_group_name_max_length','2025-05-27 00:55:19.144213'),(13,'auth','0011_update_proxy_permissions','2025-05-27 00:55:19.165066'),(14,'auth','0012_alter_user_first_name_max_length','2025-05-27 00:55:19.176914'),(15,'libreria','0001_initial','2025-05-27 00:55:20.259797'),(16,'admin','0001_initial','2025-05-27 00:55:20.831236'),(17,'admin','0002_logentry_remove_auto_add','2025-05-27 00:55:20.843599'),(18,'admin','0003_logentry_add_action_flag_choices','2025-05-27 00:55:20.858570'),(19,'libreria','0002_alter_customuser_cargo','2025-05-27 00:55:20.905767'),(20,'libreria','0003_customuser_area','2025-05-27 00:55:21.010455'),(21,'libreria','0004_customuser_fecha_registro','2025-05-27 00:55:21.117751'),(22,'papeleria','0001_initial','2025-05-27 00:55:21.438387'),(23,'papeleria','0002_alter_articulo_tipo','2025-05-27 00:55:21.661429'),(24,'papeleria','0003_pedido_articulo','2025-05-27 00:55:22.477162'),(25,'papeleria','0004_rename_pedido_articulo_pedidoarticulo','2025-05-27 00:55:22.583189'),(26,'papeleria','0005_alter_pedidoarticulo_tipo','2025-05-27 00:55:23.210947'),(27,'papeleria','0006_alter_pedidoarticulo_articulo_and_more','2025-05-27 00:55:24.138891'),(28,'papeleria','0007_alter_pedidoarticulo_tipo','2025-05-27 00:55:24.602669'),(29,'papeleria','0008_remove_pedidoarticulo_cliente_and_more','2025-05-27 00:55:25.819367'),(30,'papeleria','0009_alter_articulo_observacion','2025-05-27 00:55:25.834348'),(31,'papeleria','0010_articulo_proveedor_pedidoarticulo_area','2025-05-27 00:55:26.007255'),(32,'papeleria','0011_alter_pedido_estado','2025-05-27 00:55:26.050903'),(33,'papeleria','0012_alter_pedidoarticulo_tipo','2025-05-27 00:55:26.646756'),(34,'papeleria','0013_alter_pedidoarticulo_tipo','2025-05-27 00:55:27.055050'),(35,'sessions','0001_initial','2025-05-27 00:55:27.167863');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `libreria_customuser`
--

DROP TABLE IF EXISTS `libreria_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `libreria_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `role` varchar(13) NOT NULL,
  `cargo` varchar(50) NOT NULL,
  `module` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `area` varchar(30) NOT NULL,
  `fecha_registro` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `libreria_customuser`
--

LOCK TABLES `libreria_customuser` WRITE;
/*!40000 ALTER TABLE `libreria_customuser` DISABLE KEYS */;
INSERT INTO `libreria_customuser` VALUES (1,'pbkdf2_sha256$870000$sdA2vD1W6BeUWs0iMuHbBW$CSw+ZgOWsAOlaZKEzs4uBVyI6joq8U4oT+exatAAzbs=','2025-05-27 01:22:32.510397',0,'daniel','jonnathansz73@gmail.com','Administrador','aprendiz sena','Papeleria',1,0,'Administrativa','2025-05-26'),(2,'pbkdf2_sha256$870000$EXFmQ9evioytsWu7JFfv7g$oIVA0XSfxMlLWSB2Dk/LDuikGKrVa5y8kClgegxCBpo=','2025-05-27 01:21:48.562233',0,'diego','diego@gmail.com','Empleado','aprendiz','Papeleria',1,0,'Registros públicos','2025-05-26');
/*!40000 ALTER TABLE `libreria_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `libreria_customuser_groups`
--

DROP TABLE IF EXISTS `libreria_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `libreria_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `libreria_customuser_groups_customuser_id_group_id_00351eff_uniq` (`customuser_id`,`group_id`),
  KEY `libreria_customuser_groups_group_id_071f7f88_fk_auth_group_id` (`group_id`),
  CONSTRAINT `libreria_customuser__customuser_id_3af84ce6_fk_libreria_` FOREIGN KEY (`customuser_id`) REFERENCES `libreria_customuser` (`id`),
  CONSTRAINT `libreria_customuser_groups_group_id_071f7f88_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `libreria_customuser_groups`
--

LOCK TABLES `libreria_customuser_groups` WRITE;
/*!40000 ALTER TABLE `libreria_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `libreria_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `libreria_customuser_user_permissions`
--

DROP TABLE IF EXISTS `libreria_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `libreria_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `libreria_customuser_user_customuser_id_permission_e5838e6e_uniq` (`customuser_id`,`permission_id`),
  KEY `libreria_customuser__permission_id_1ff0bbce_fk_auth_perm` (`permission_id`),
  CONSTRAINT `libreria_customuser__customuser_id_4221e7cc_fk_libreria_` FOREIGN KEY (`customuser_id`) REFERENCES `libreria_customuser` (`id`),
  CONSTRAINT `libreria_customuser__permission_id_1ff0bbce_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `libreria_customuser_user_permissions`
--

LOCK TABLES `libreria_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `libreria_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `libreria_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `papeleria_articulo`
--

DROP TABLE IF EXISTS `papeleria_articulo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `papeleria_articulo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `marca` varchar(50) NOT NULL,
  `observacion` longtext,
  `tipo` varchar(50) DEFAULT NULL,
  `precio` bigint unsigned NOT NULL,
  `cantidad` int unsigned NOT NULL,
  `fecha_registro` date NOT NULL,
  `registrado_por_id` bigint DEFAULT NULL,
  `proveedor` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `papeleria_articulo_registrado_por_id_0c2be10e_fk_libreria_` (`registrado_por_id`),
  CONSTRAINT `papeleria_articulo_registrado_por_id_0c2be10e_fk_libreria_` FOREIGN KEY (`registrado_por_id`) REFERENCES `libreria_customuser` (`id`),
  CONSTRAINT `papeleria_articulo_chk_1` CHECK ((`precio` >= 0)),
  CONSTRAINT `papeleria_articulo_chk_2` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `papeleria_articulo`
--

LOCK TABLES `papeleria_articulo` WRITE;
/*!40000 ALTER TABLE `papeleria_articulo` DISABLE KEYS */;
INSERT INTO `papeleria_articulo` VALUES (1,'Tapas de carpetas','bic','no tiene','Recicables',1000,10,'2025-05-26',1,'javeriana'),(2,'resma','norma','dfgg','carta',4500,20,'2025-05-26',1,'dgg');
/*!40000 ALTER TABLE `papeleria_articulo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `papeleria_pedido`
--

DROP TABLE IF EXISTS `papeleria_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `papeleria_pedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_pedido` datetime(6) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `registrado_por_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `papeleria_pedido_registrado_por_id_b6a945d7_fk_libreria_` (`registrado_por_id`),
  CONSTRAINT `papeleria_pedido_registrado_por_id_b6a945d7_fk_libreria_` FOREIGN KEY (`registrado_por_id`) REFERENCES `libreria_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `papeleria_pedido`
--

LOCK TABLES `papeleria_pedido` WRITE;
/*!40000 ALTER TABLE `papeleria_pedido` DISABLE KEYS */;
INSERT INTO `papeleria_pedido` VALUES (1,'2025-05-27 00:59:17.774118','Confirmado',1),(2,'2025-05-27 01:07:55.380035','Confirmado',1),(3,'2025-05-27 01:09:49.552317','Confirmado',1),(4,'2025-05-27 01:17:25.692718','Confirmado',1),(5,'2025-05-27 01:21:59.794372','Pendiente',2),(6,'2025-05-27 01:22:12.458076','Cancelado',2);
/*!40000 ALTER TABLE `papeleria_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `papeleria_pedidoarticulo`
--

DROP TABLE IF EXISTS `papeleria_pedidoarticulo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `papeleria_pedidoarticulo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` int unsigned NOT NULL,
  `articulo_id` bigint NOT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `pedido_id` bigint DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `papeleria_pedido_art_articulo_id_e54f5ecb_fk_papeleria` (`articulo_id`),
  KEY `papeleria_pedidoarti_pedido_id_636b9164_fk_papeleria` (`pedido_id`),
  CONSTRAINT `papeleria_pedido_art_articulo_id_e54f5ecb_fk_papeleria` FOREIGN KEY (`articulo_id`) REFERENCES `papeleria_articulo` (`id`),
  CONSTRAINT `papeleria_pedidoarti_pedido_id_636b9164_fk_papeleria` FOREIGN KEY (`pedido_id`) REFERENCES `papeleria_pedido` (`id`),
  CONSTRAINT `papeleria_pedidoarticulo_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `papeleria_pedidoarticulo`
--

LOCK TABLES `papeleria_pedidoarticulo` WRITE;
/*!40000 ALTER TABLE `papeleria_pedidoarticulo` DISABLE KEYS */;
INSERT INTO `papeleria_pedidoarticulo` VALUES (1,1,1,'Recicables',1,'Administrativa'),(2,9,1,'Recicables',2,'Administrativa'),(3,1,1,'Recicables',3,'Administrativa'),(4,10,2,'carta',3,'Administrativa'),(5,10,2,'carta',4,'Administrativa'),(6,5,1,'Recicables',5,'Registros públicos'),(7,1,2,'carta',6,'Registros públicos');
/*!40000 ALTER TABLE `papeleria_pedidoarticulo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'ccd'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-26 20:24:06
