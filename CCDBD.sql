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
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add custom user',6,'add_customuser'),(22,'Can change custom user',6,'change_customuser'),(23,'Can delete custom user',6,'delete_customuser'),(24,'Can view custom user',6,'view_customuser'),(25,'Can add articulo',7,'add_articulo'),(26,'Can change articulo',7,'change_articulo'),(27,'Can delete articulo',7,'delete_articulo'),(28,'Can view articulo',7,'view_articulo'),(29,'Can add pedido articulo',8,'add_pedidoarticulo'),(30,'Can change pedido articulo',8,'change_pedidoarticulo'),(31,'Can delete pedido articulo',8,'delete_pedidoarticulo'),(32,'Can view pedido articulo',8,'view_pedidoarticulo'),(33,'Can add pedido',9,'add_pedido'),(34,'Can change pedido',9,'change_pedido'),(35,'Can delete pedido',9,'delete_pedido'),(36,'Can view pedido',9,'view_pedido'),(37,'Can add productos',10,'add_productos'),(38,'Can change productos',10,'change_productos'),(39,'Can delete productos',10,'delete_productos'),(40,'Can view productos',10,'view_productos'),(41,'Can add pedido',11,'add_pedido'),(42,'Can change pedido',11,'change_pedido'),(43,'Can delete pedido',11,'delete_pedido'),(44,'Can view pedido',11,'view_pedido'),(45,'Can add pedido producto',12,'add_pedidoproducto'),(46,'Can change pedido producto',12,'change_pedidoproducto'),(47,'Can delete pedido producto',12,'delete_pedidoproducto'),(48,'Can view pedido producto',12,'view_pedidoproducto'),(49,'Can add backup',13,'add_backup'),(50,'Can change backup',13,'change_backup'),(51,'Can delete backup',13,'delete_backup'),(52,'Can view backup',13,'view_backup');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup_backup`
--

DROP TABLE IF EXISTS `backup_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backup_backup` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `archivo` varchar(100) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `tamano` varchar(100) NOT NULL,
  `modelos_incluidos` longtext NOT NULL,
  `creado_por_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `backup_backup_creado_por_id_217c3075_fk_libreria_customuser_id` (`creado_por_id`),
  CONSTRAINT `backup_backup_creado_por_id_217c3075_fk_libreria_customuser_id` FOREIGN KEY (`creado_por_id`) REFERENCES `libreria_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_backup`
--

LOCK TABLES `backup_backup` WRITE;
/*!40000 ALTER TABLE `backup_backup` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup_backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cafeteria_pedido`
--

DROP TABLE IF EXISTS `cafeteria_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cafeteria_pedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_pedido` datetime(6) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `registrado_por_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cafeteria_pedido_registrado_por_id_e4db4d2b_fk_libreria_` (`registrado_por_id`),
  CONSTRAINT `cafeteria_pedido_registrado_por_id_e4db4d2b_fk_libreria_` FOREIGN KEY (`registrado_por_id`) REFERENCES `libreria_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cafeteria_pedido`
--

LOCK TABLES `cafeteria_pedido` WRITE;
/*!40000 ALTER TABLE `cafeteria_pedido` DISABLE KEYS */;
INSERT INTO `cafeteria_pedido` VALUES (1,'2025-06-11 02:47:54.759239','Confirmado',1),(2,'2025-06-11 02:55:56.729033','Confirmado',1),(3,'2025-06-11 03:00:13.695758','Confirmado',1),(4,'2025-06-11 03:06:50.071129','Confirmado',2),(5,'2025-06-12 01:43:12.806595','Confirmado',1),(6,'2025-06-12 01:44:35.772526','Pendiente',2),(7,'2025-06-12 01:50:55.355009','Confirmado',3),(8,'2025-06-12 01:59:04.922381','Pendiente',3);
/*!40000 ALTER TABLE `cafeteria_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cafeteria_pedidoproducto`
--

DROP TABLE IF EXISTS `cafeteria_pedidoproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cafeteria_pedidoproducto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` int unsigned NOT NULL,
  `area` varchar(50) DEFAULT NULL,
  `producto_id` bigint NOT NULL,
  `lugar` varchar(100) NOT NULL,
  `pedido_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cafeteria_pedidoprod_producto_id_53398573_fk_cafeteria` (`producto_id`),
  KEY `cafeteria_pedidoprod_pedido_id_cf5da2ef_fk_cafeteria` (`pedido_id`),
  CONSTRAINT `cafeteria_pedidoprod_pedido_id_cf5da2ef_fk_cafeteria` FOREIGN KEY (`pedido_id`) REFERENCES `cafeteria_pedido` (`id`),
  CONSTRAINT `cafeteria_pedidoprod_producto_id_53398573_fk_cafeteria` FOREIGN KEY (`producto_id`) REFERENCES `cafeteria_productos` (`id`),
  CONSTRAINT `cafeteria_pedidoproducto_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cafeteria_pedidoproducto`
--

LOCK TABLES `cafeteria_pedidoproducto` WRITE;
/*!40000 ALTER TABLE `cafeteria_pedidoproducto` DISABLE KEYS */;
INSERT INTO `cafeteria_pedidoproducto` VALUES (1,1,'Administrativa',1,'vcvvc',2),(2,1,'Administrativa',1,'sdfsd',3),(3,1,'Administrativa',1,'dfsd',4),(4,1,'Administrativa',1,'dfgdf',5),(5,1,'Administrativa',2,'fdgfdg',5),(6,1,'Administrativa',2,'ffgfg',6),(7,1,'Administrativa',1,'fghgfh',6),(8,1,'Administrativa',1,'rtrtret',7),(9,1,'Administrativa',2,'dfgdfg',7),(10,1,'Administrativa',1,'fgfdgdf',8),(11,14,'Administrativa',2,'sdfdsf',8);
/*!40000 ALTER TABLE `cafeteria_pedidoproducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cafeteria_productos`
--

DROP TABLE IF EXISTS `cafeteria_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cafeteria_productos` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `marca` varchar(50) NOT NULL,
  `precio` bigint unsigned NOT NULL,
  `cantidad` int unsigned NOT NULL,
  `proveedor` varchar(100) NOT NULL,
  `fecha_registro` date NOT NULL,
  `unidad_medida` varchar(15) NOT NULL,
  `registrado_por_id` bigint DEFAULT NULL,
  `presentacion` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `cafeteria_productos_registrado_por_id_26864eb8_fk_libreria_` (`registrado_por_id`),
  CONSTRAINT `cafeteria_productos_registrado_por_id_26864eb8_fk_libreria_` FOREIGN KEY (`registrado_por_id`) REFERENCES `libreria_customuser` (`id`),
  CONSTRAINT `cafeteria_productos_chk_1` CHECK ((`precio` >= 0)),
  CONSTRAINT `cafeteria_productos_chk_2` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cafeteria_productos`
--

LOCK TABLES `cafeteria_productos` WRITE;
/*!40000 ALTER TABLE `cafeteria_productos` DISABLE KEYS */;
INSERT INTO `cafeteria_productos` VALUES (1,'dfdg','dfsf',43344,31,'sdfsdf','2025-06-11','Kilogramos',1,'sdf'),(2,'fgfgh','dfgdf',4444,443,'dfgdfg','2025-06-11','Kilogramos',1,'ertger');
/*!40000 ALTER TABLE `cafeteria_productos` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(13,'backup','backup'),(11,'cafeteria','pedido'),(12,'cafeteria','pedidoproducto'),(10,'cafeteria','productos'),(4,'contenttypes','contenttype'),(6,'libreria','customuser'),(7,'papeleria','articulo'),(9,'papeleria','pedido'),(8,'papeleria','pedidoarticulo'),(5,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-06-11 02:44:42.577229'),(2,'contenttypes','0002_remove_content_type_name','2025-06-11 02:44:42.729626'),(3,'auth','0001_initial','2025-06-11 02:44:43.577773'),(4,'auth','0002_alter_permission_name_max_length','2025-06-11 02:44:43.713397'),(5,'auth','0003_alter_user_email_max_length','2025-06-11 02:44:43.725249'),(6,'auth','0004_alter_user_username_opts','2025-06-11 02:44:43.739494'),(7,'auth','0005_alter_user_last_login_null','2025-06-11 02:44:43.750469'),(8,'auth','0006_require_contenttypes_0002','2025-06-11 02:44:43.756454'),(9,'auth','0007_alter_validators_add_error_messages','2025-06-11 02:44:43.768440'),(10,'auth','0008_alter_user_username_max_length','2025-06-11 02:44:43.789589'),(11,'auth','0009_alter_user_last_name_max_length','2025-06-11 02:44:43.803432'),(12,'auth','0010_alter_group_name_max_length','2025-06-11 02:44:43.847996'),(13,'auth','0011_update_proxy_permissions','2025-06-11 02:44:43.861278'),(14,'auth','0012_alter_user_first_name_max_length','2025-06-11 02:44:43.874515'),(15,'libreria','0001_initial','2025-06-11 02:44:44.930857'),(16,'admin','0001_initial','2025-06-11 02:44:45.440973'),(17,'admin','0002_logentry_remove_auto_add','2025-06-11 02:44:45.455763'),(18,'admin','0003_logentry_add_action_flag_choices','2025-06-11 02:44:45.468754'),(19,'backup','0001_initial','2025-06-11 02:44:45.545385'),(20,'backup','0002_backup_creado_por_alter_backup_modelos_incluidos_and_more','2025-06-11 02:44:46.043253'),(21,'cafeteria','0001_initial','2025-06-11 02:44:46.363099'),(22,'cafeteria','0002_remove_productos_observacion_productos_presentacion','2025-06-11 02:44:46.501459'),(23,'cafeteria','0003_alter_productos_unidad_medida_pedido_pedidoproducto','2025-06-11 02:44:47.063481'),(24,'cafeteria','0004_pedidoproducto_lugar','2025-06-11 02:44:47.152815'),(25,'cafeteria','0005_remove_pedidoproducto_tipo_pedidoproducto_pedido','2025-06-11 02:44:47.445840'),(26,'libreria','0002_alter_customuser_cargo','2025-06-11 02:44:47.512867'),(27,'libreria','0003_customuser_area','2025-06-11 02:44:47.635503'),(28,'libreria','0004_customuser_fecha_registro','2025-06-11 02:44:47.757058'),(29,'libreria','0005_remove_customuser_module_customuser_acceso_caf_and_more','2025-06-11 02:44:48.471705'),(30,'libreria','0006_alter_customuser_area','2025-06-11 02:44:48.488620'),(31,'papeleria','0001_initial','2025-06-11 02:44:48.798700'),(32,'papeleria','0002_alter_articulo_tipo','2025-06-11 02:44:49.000238'),(33,'papeleria','0003_pedido_articulo','2025-06-11 02:44:49.814700'),(34,'papeleria','0004_rename_pedido_articulo_pedidoarticulo','2025-06-11 02:44:49.964630'),(35,'papeleria','0005_alter_pedidoarticulo_tipo','2025-06-11 02:44:50.606834'),(36,'papeleria','0006_alter_pedidoarticulo_articulo_and_more','2025-06-11 02:44:51.176675'),(37,'papeleria','0007_alter_pedidoarticulo_tipo','2025-06-11 02:44:51.517454'),(38,'papeleria','0008_remove_pedidoarticulo_cliente_and_more','2025-06-11 02:44:53.163396'),(39,'papeleria','0009_alter_articulo_observacion','2025-06-11 02:44:53.193055'),(40,'papeleria','0010_articulo_proveedor_pedidoarticulo_area','2025-06-11 02:44:53.447445'),(41,'papeleria','0011_alter_pedido_estado','2025-06-11 02:44:53.463245'),(42,'papeleria','0012_alter_pedidoarticulo_tipo','2025-06-11 02:44:54.021122'),(43,'papeleria','0013_alter_pedidoarticulo_tipo','2025-06-11 02:44:54.443678'),(44,'sessions','0001_initial','2025-06-11 02:44:54.563351');
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
INSERT INTO `django_session` VALUES ('ngb150j4pl7cc42mmc2lxsf514yk3xjg','.eJxVjMsOgjAQRf-la0Po9M3ShO9opu0UGhGTFlbGfxcNC92ee895Mo_7Nvu9UfUlsYEBu_yygPFG62dYSqhUC3Ynat14x7Jcz8OfNWObD0Vy5bIktJEbcgmEBQegshS2V6AV9tEEMMKgzgJ6p6yUmecsXdAGEz-i39zymCZKvqxs2OpOrzfAjjrC:1uPBr2:8jf5jb42vwK32vccICTsNsOLzuym91orIfJBHkq9dqM','2025-06-11 03:20:20.837590');
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
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `area` varchar(30) NOT NULL,
  `fecha_registro` date NOT NULL,
  `acceso_caf` tinyint(1) NOT NULL,
  `acceso_cde` tinyint(1) NOT NULL,
  `acceso_pap` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `libreria_customuser`
--

LOCK TABLES `libreria_customuser` WRITE;
/*!40000 ALTER TABLE `libreria_customuser` DISABLE KEYS */;
INSERT INTO `libreria_customuser` VALUES (1,'pbkdf2_sha256$870000$j5QXjBtNWIt6LDN5i4i3uD$kYK50CUUIbkPHJ8UK6PcIt9F9ICZNM2FqFYfVR4ZCNQ=','2025-06-12 01:55:06.906864',0,'Daniel Sanchez','jonnathansz73@gmail.com','Administrador','Director ccd',1,0,'Administrativa','2025-06-10',1,1,1),(2,'pbkdf2_sha256$870000$J3YXDMVgWeLBkUXMq5fCa6$yk1qTGxjEeXHrhCErhxUmTfbI8kHyWhvLPlMZUV4ThY=','2025-06-12 01:43:57.662268',0,'Diego','diego@gmail.com','Empleado','Aprendiz',1,0,'Administrativa','2025-06-11',0,0,0),(3,'pbkdf2_sha256$870000$ZtY9eftU12EnA9brWd1uz2$JHvKGgKkAL6YIWgEQW5Sal0X6jt39ujAMo7J7YDrdHw=','2025-06-12 01:58:40.892928',0,'Viviana','viviana@gmail.com','Empleado','Asistente en gestion documental',1,0,'Administrativa','2025-06-11',1,0,0);
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
INSERT INTO `papeleria_articulo` VALUES (1,'Resma','sdfdsf','sdfsdf','dfdfsd',4444,443,'2025-06-11',1,'sdfsdf'),(2,'sdffs','asdyt','fdgdg','dfd',3333,32,'2025-06-11',1,'rthtgrf');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `papeleria_pedido`
--

LOCK TABLES `papeleria_pedido` WRITE;
/*!40000 ALTER TABLE `papeleria_pedido` DISABLE KEYS */;
INSERT INTO `papeleria_pedido` VALUES (1,'2025-06-12 01:40:36.461152','Confirmado',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `papeleria_pedidoarticulo`
--

LOCK TABLES `papeleria_pedidoarticulo` WRITE;
/*!40000 ALTER TABLE `papeleria_pedidoarticulo` DISABLE KEYS */;
INSERT INTO `papeleria_pedidoarticulo` VALUES (1,1,1,'dfdfsd',1,'Administrativa'),(2,1,2,'dfd',1,'Administrativa');
/*!40000 ALTER TABLE `papeleria_pedidoarticulo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-11 21:50:23
