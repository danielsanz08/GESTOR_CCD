-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
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
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add custom user',6,'add_customuser'),(22,'Can change custom user',6,'change_customuser'),(23,'Can delete custom user',6,'delete_customuser'),(24,'Can view custom user',6,'view_customuser'),(25,'Can add articulo',7,'add_articulo'),(26,'Can change articulo',7,'change_articulo'),(27,'Can delete articulo',7,'delete_articulo'),(28,'Can view articulo',7,'view_articulo'),(29,'Can add pedido',8,'add_pedido'),(30,'Can change pedido',8,'change_pedido'),(31,'Can delete pedido',8,'delete_pedido'),(32,'Can view pedido',8,'view_pedido'),(33,'Can add pedido articulo',9,'add_pedidoarticulo'),(34,'Can change pedido articulo',9,'change_pedidoarticulo'),(35,'Can delete pedido articulo',9,'delete_pedidoarticulo'),(36,'Can view pedido articulo',9,'view_pedidoarticulo'),(37,'Can add productos',10,'add_productos'),(38,'Can change productos',10,'change_productos'),(39,'Can delete productos',10,'delete_productos'),(40,'Can view productos',10,'view_productos'),(41,'Can add pedido',11,'add_pedido'),(42,'Can change pedido',11,'change_pedido'),(43,'Can delete pedido',11,'delete_pedido'),(44,'Can view pedido',11,'view_pedido'),(45,'Can add pedido producto',12,'add_pedidoproducto'),(46,'Can change pedido producto',12,'change_pedidoproducto'),(47,'Can delete pedido producto',12,'delete_pedidoproducto'),(48,'Can view pedido producto',12,'view_pedidoproducto'),(49,'Can add pedido cde',13,'add_pedidocde'),(50,'Can change pedido cde',13,'change_pedidocde'),(51,'Can delete pedido cde',13,'delete_pedidocde'),(52,'Can view pedido cde',13,'view_pedidocde'),(53,'Can add pedido producto cde',14,'add_pedidoproductocde'),(54,'Can change pedido producto cde',14,'change_pedidoproductocde'),(55,'Can delete pedido producto cde',14,'delete_pedidoproductocde'),(56,'Can view pedido producto cde',14,'view_pedidoproductocde'),(57,'Can add backup',15,'add_backup'),(58,'Can change backup',15,'change_backup'),(59,'Can delete backup',15,'delete_backup'),(60,'Can view backup',15,'view_backup');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_backup`
--

LOCK TABLES `backup_backup` WRITE;
/*!40000 ALTER TABLE `backup_backup` DISABLE KEYS */;
INSERT INTO `backup_backup` VALUES (1,'Fgfg','backups/backup_db_20250716_090506.json','2025-07-16 14:05:06.477000','0.01 MB','libreria.CustomUser, papeleria.Articulo, papeleria.Pedido, papeleria.PedidoArticulo, cafeteria.Productos, cafeteria.Pedido, cafeteria.PedidoProducto, cde.PedidoCde, cde.PedidoProductoCde (con relaciones)',1),(2,'Ccd1 Backup','backups/backup_db_20250717_112801.json','2025-07-17 16:28:02.385224','0.03 MB','libreria.CustomUser, papeleria.Articulo, papeleria.Pedido, papeleria.PedidoArticulo, cafeteria.Productos, cafeteria.Pedido, cafeteria.PedidoProducto, cde.PedidoCde, cde.PedidoProductoCde (con relaciones)',1),(3,'export_20250717_112816','backups/backup_db_20250717_112816.json','2025-07-17 16:28:16.321411','0.03 MB','Todos (exportación completa con relaciones)',1);
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
  `registrado_por_id` bigint NOT NULL,
  `fecha_estado` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cafeteria_pedido_registrado_por_id_e4db4d2b_fk_libreria_` (`registrado_por_id`),
  CONSTRAINT `cafeteria_pedido_registrado_por_id_e4db4d2b_fk_libreria_` FOREIGN KEY (`registrado_por_id`) REFERENCES `libreria_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cafeteria_pedido`
--

LOCK TABLES `cafeteria_pedido` WRITE;
/*!40000 ALTER TABLE `cafeteria_pedido` DISABLE KEYS */;
INSERT INTO `cafeteria_pedido` VALUES (1,'2025-07-17 12:59:08.155658','Confirmado',2,'2025-07-17 12:59:08.155301'),(2,'2025-07-17 13:00:55.467400','Confirmado',2,'2025-07-17 13:00:55.467225'),(3,'2025-07-17 13:01:43.983519','Confirmado',2,'2025-07-17 13:01:43.983385'),(4,'2025-07-17 13:02:20.447335','Confirmado',2,'2025-07-17 13:02:20.447117'),(5,'2025-07-17 13:02:52.576823','Confirmado',2,'2025-07-17 13:02:52.576524'),(6,'2025-07-17 13:05:37.180827','Pendiente',3,NULL),(7,'2025-07-17 13:06:17.328775','Pendiente',3,NULL),(8,'2025-07-17 13:07:09.715500','Pendiente',3,NULL),(9,'2025-07-17 13:07:46.674194','Pendiente',3,NULL),(10,'2025-07-17 13:08:17.966013','Pendiente',3,NULL),(11,'2025-07-17 13:23:45.776372','Cancelado',3,'2025-07-17 13:42:50.105444'),(12,'2025-07-17 13:25:53.323972','Confirmado',3,'2025-07-17 13:42:25.183140');
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
  `area` varchar(50) NOT NULL,
  `producto_id` bigint NOT NULL,
  `lugar` varchar(100) NOT NULL,
  `pedido_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cafeteria_pedidoprod_producto_id_53398573_fk_cafeteria` (`producto_id`),
  KEY `cafeteria_pedidoprod_pedido_id_cf5da2ef_fk_cafeteria` (`pedido_id`),
  CONSTRAINT `cafeteria_pedidoprod_pedido_id_cf5da2ef_fk_cafeteria` FOREIGN KEY (`pedido_id`) REFERENCES `cafeteria_pedido` (`id`),
  CONSTRAINT `cafeteria_pedidoprod_producto_id_53398573_fk_cafeteria` FOREIGN KEY (`producto_id`) REFERENCES `cafeteria_productos` (`id`),
  CONSTRAINT `cafeteria_pedidoproducto_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cafeteria_pedidoproducto`
--

LOCK TABLES `cafeteria_pedidoproducto` WRITE;
/*!40000 ALTER TABLE `cafeteria_pedidoproducto` DISABLE KEYS */;
INSERT INTO `cafeteria_pedidoproducto` VALUES (3,1,'Administrativa',2,'cde',2),(4,1,'Administrativa',3,'cde',2),(5,1,'Administrativa',4,'cde',2),(6,1,'Administrativa',3,'cde',3),(7,16,'Administrativa',5,'cafeteria',4),(8,1,'Administrativa',5,'sdsd',5),(11,1,'Administrativa',2,'cde',7),(13,1,'Administrativa',2,'cde',8),(14,1,'Administrativa',3,'cde',8),(15,1,'Administrativa',4,'cde',8),(16,1,'Administrativa',5,'cde',9),(17,1,'Administrativa',5,'cde',10),(19,1,'Administrativa',5,'feliz maria',11),(21,1,'Administrativa',2,'cde',12);
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
  `registrado_por_id` bigint NOT NULL,
  `presentacion` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cafeteria_productos_registrado_por_id_26864eb8_fk_libreria_` (`registrado_por_id`),
  CONSTRAINT `cafeteria_productos_registrado_por_id_26864eb8_fk_libreria_` FOREIGN KEY (`registrado_por_id`) REFERENCES `libreria_customuser` (`id`),
  CONSTRAINT `cafeteria_productos_chk_1` CHECK ((`precio` >= 0)),
  CONSTRAINT `cafeteria_productos_chk_2` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cafeteria_productos`
--

LOCK TABLES `cafeteria_productos` WRITE;
/*!40000 ALTER TABLE `cafeteria_productos` DISABLE KEYS */;
INSERT INTO `cafeteria_productos` VALUES (2,'Palitos Mezcladores','Bond Ltda',5000,22,'Javeriana','2025-07-17','Unidad',2,'Paquete'),(3,'Toallas','Toallas Ltda',50000,34,'Javeriana','2025-07-17','Unidad',2,'Unidad'),(4,'Papel Higienico','Papel Scott',5500,1,'Scott','2025-07-17','Unidad',2,'Paquete Por Doce'),(5,'Café','Tostao',5000,0,'Tostao','2025-07-17','Kilogramos',2,'Paquete');
/*!40000 ALTER TABLE `cafeteria_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cde_pedidocde`
--

DROP TABLE IF EXISTS `cde_pedidocde`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cde_pedidocde` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_pedido` datetime(6) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `registrado_por_id` bigint NOT NULL,
  `fecha_estado` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cde_pedidocde_registrado_por_id_dba5a62f_fk_libreria_` (`registrado_por_id`),
  CONSTRAINT `cde_pedidocde_registrado_por_id_dba5a62f_fk_libreria_` FOREIGN KEY (`registrado_por_id`) REFERENCES `libreria_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cde_pedidocde`
--

LOCK TABLES `cde_pedidocde` WRITE;
/*!40000 ALTER TABLE `cde_pedidocde` DISABLE KEYS */;
INSERT INTO `cde_pedidocde` VALUES (1,'2025-07-17 14:44:49.542931','Confirmado',2,'2025-07-17 14:44:49.542681'),(2,'2025-07-17 14:45:49.522621','Pendiente',3,NULL),(3,'2025-07-17 14:46:29.511712','Pendiente',3,NULL),(4,'2025-07-17 14:47:22.602505','Pendiente',3,NULL),(5,'2025-07-17 14:48:48.706301','Cancelado',3,'2025-07-17 15:16:45.942460'),(6,'2025-07-17 14:49:22.671515','Confirmado',3,'2025-07-17 15:15:14.790567'),(7,'2025-07-17 15:16:02.016904','Confirmado',2,'2025-07-17 15:16:02.016740');
/*!40000 ALTER TABLE `cde_pedidocde` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cde_pedidoproductocde`
--

DROP TABLE IF EXISTS `cde_pedidoproductocde`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cde_pedidoproductocde` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` int unsigned NOT NULL,
  `area` varchar(50) NOT NULL,
  `evento` varchar(100) NOT NULL,
  `pedido_id` bigint NOT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cde_pedidoproductocd_producto_id_650e0030_fk_cafeteria` (`producto_id`),
  KEY `cde_pedidoproductocde_pedido_id_edac6f17_fk_cde_pedidocde_id` (`pedido_id`),
  CONSTRAINT `cde_pedidoproductocd_producto_id_650e0030_fk_cafeteria` FOREIGN KEY (`producto_id`) REFERENCES `cafeteria_productos` (`id`),
  CONSTRAINT `cde_pedidoproductocde_pedido_id_edac6f17_fk_cde_pedidocde_id` FOREIGN KEY (`pedido_id`) REFERENCES `cde_pedidocde` (`id`),
  CONSTRAINT `cde_pedidoproductocde_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cde_pedidoproductocde`
--

LOCK TABLES `cde_pedidoproductocde` WRITE;
/*!40000 ALTER TABLE `cde_pedidoproductocde` DISABLE KEYS */;
INSERT INTO `cde_pedidoproductocde` VALUES (1,49,'Administrativa','noticamara',1,5),(4,1,'Administrativa','ccd',3,2),(5,1,'Administrativa','exposicion',4,3),(7,1,'Administrativa','ccd',4,2),(9,1,'Administrativa','dfdfgdfg',5,4),(10,1,'Administrativa','fdgfdg',5,2),(11,1,'Administrativa','fgfdg',5,3),(12,1,'Administrativa','cvbvb',6,2),(13,1,'Administrativa','vbvb',6,4),(15,1,'Administrativa','cde',7,2);
/*!40000 ALTER TABLE `cde_pedidoproductocde` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(15,'backup','backup'),(11,'cafeteria','pedido'),(12,'cafeteria','pedidoproducto'),(10,'cafeteria','productos'),(13,'cde','pedidocde'),(14,'cde','pedidoproductocde'),(4,'contenttypes','contenttype'),(6,'libreria','customuser'),(7,'papeleria','articulo'),(8,'papeleria','pedido'),(9,'papeleria','pedidoarticulo'),(5,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-07-16 13:29:35.362176'),(2,'contenttypes','0002_remove_content_type_name','2025-07-16 13:29:36.629138'),(3,'auth','0001_initial','2025-07-16 13:29:46.613508'),(4,'auth','0002_alter_permission_name_max_length','2025-07-16 13:29:48.116416'),(5,'auth','0003_alter_user_email_max_length','2025-07-16 13:29:48.227645'),(6,'auth','0004_alter_user_username_opts','2025-07-16 13:29:48.337205'),(7,'auth','0005_alter_user_last_login_null','2025-07-16 13:29:48.482810'),(8,'auth','0006_require_contenttypes_0002','2025-07-16 13:29:48.610165'),(9,'auth','0007_alter_validators_add_error_messages','2025-07-16 13:29:48.733242'),(10,'auth','0008_alter_user_username_max_length','2025-07-16 13:29:48.819926'),(11,'auth','0009_alter_user_last_name_max_length','2025-07-16 13:29:48.973428'),(12,'auth','0010_alter_group_name_max_length','2025-07-16 13:29:49.273174'),(13,'auth','0011_update_proxy_permissions','2025-07-16 13:29:49.385810'),(14,'auth','0012_alter_user_first_name_max_length','2025-07-16 13:29:49.528884'),(15,'libreria','0001_initial','2025-07-16 13:29:57.434845'),(16,'admin','0001_initial','2025-07-16 13:30:00.956128'),(17,'admin','0002_logentry_remove_auto_add','2025-07-16 13:30:01.037092'),(18,'admin','0003_logentry_add_action_flag_choices','2025-07-16 13:30:01.126397'),(19,'backup','0001_initial','2025-07-16 13:30:01.690795'),(20,'backup','0002_backup_creado_por_alter_backup_modelos_incluidos_and_more','2025-07-16 13:30:04.116662'),(21,'cafeteria','0001_initial','2025-07-16 13:30:06.198918'),(22,'cafeteria','0002_remove_productos_observacion_productos_presentacion','2025-07-16 13:30:07.078819'),(23,'cafeteria','0003_alter_productos_unidad_medida_pedido_pedidoproducto','2025-07-16 13:30:11.219881'),(24,'cafeteria','0004_pedidoproducto_lugar','2025-07-16 13:30:11.805785'),(25,'cafeteria','0005_remove_pedidoproducto_tipo_pedidoproducto_pedido','2025-07-16 13:30:13.521553'),(26,'cafeteria','0006_alter_productos_nombre','2025-07-16 13:30:14.155334'),(27,'cafeteria','0007_alter_pedido_registrado_por_and_more','2025-07-16 13:30:23.826274'),(28,'cafeteria','0008_pedido_fecha_estado','2025-07-16 13:30:24.233934'),(29,'cafeteria','0009_alter_pedidoproducto_producto','2025-07-16 13:30:24.308624'),(30,'cde','0001_initial','2025-07-16 13:30:32.811854'),(31,'cde','0002_alter_pedidocde_registrado_por_and_more','2025-07-16 13:30:40.372278'),(32,'cde','0003_pedidocde_fecha_estado','2025-07-16 13:30:40.762933'),(33,'cde','0004_alter_pedidoproductocde_producto','2025-07-16 13:30:40.861951'),(34,'libreria','0002_alter_customuser_cargo','2025-07-16 13:30:41.154511'),(35,'libreria','0003_customuser_area','2025-07-16 13:30:41.965605'),(36,'libreria','0004_customuser_fecha_registro','2025-07-16 13:30:42.674607'),(37,'libreria','0005_remove_customuser_module_customuser_acceso_caf_and_more','2025-07-16 13:30:45.083223'),(38,'libreria','0006_alter_customuser_area','2025-07-16 13:30:45.152003'),(39,'libreria','0007_alter_customuser_username','2025-07-16 13:30:46.704470'),(40,'libreria','0008_alter_customuser_fecha_registro','2025-07-16 13:30:46.812776'),(41,'papeleria','0001_initial','2025-07-16 13:30:49.270513'),(42,'papeleria','0002_alter_articulo_tipo','2025-07-16 13:30:50.365241'),(43,'papeleria','0003_pedido_articulo','2025-07-16 13:30:55.926278'),(44,'papeleria','0004_rename_pedido_articulo_pedidoarticulo','2025-07-16 13:30:56.662957'),(45,'papeleria','0005_alter_pedidoarticulo_tipo','2025-07-16 13:31:02.627083'),(46,'papeleria','0006_alter_pedidoarticulo_articulo_and_more','2025-07-16 13:31:06.820726'),(47,'papeleria','0007_alter_pedidoarticulo_tipo','2025-07-16 13:31:09.152218'),(48,'papeleria','0008_remove_pedidoarticulo_cliente_and_more','2025-07-16 13:31:16.417317'),(49,'papeleria','0009_alter_articulo_observacion','2025-07-16 13:31:16.496844'),(50,'papeleria','0010_articulo_proveedor_pedidoarticulo_area','2025-07-16 13:31:18.036572'),(51,'papeleria','0011_alter_pedido_estado','2025-07-16 13:31:18.221698'),(52,'papeleria','0012_alter_pedidoarticulo_tipo','2025-07-16 13:31:24.688582'),(53,'papeleria','0013_alter_pedidoarticulo_tipo','2025-07-16 13:31:27.010725'),(54,'papeleria','0014_alter_articulo_nombre','2025-07-16 13:31:27.524548'),(55,'papeleria','0015_alter_articulo_marca_alter_articulo_nombre_and_more','2025-07-16 13:31:33.500956'),(56,'papeleria','0016_alter_articulo_marca_alter_articulo_nombre_and_more','2025-07-16 13:31:35.884066'),(57,'papeleria','0017_alter_articulo_cantidad','2025-07-16 13:31:35.990114'),(58,'papeleria','0018_alter_articulo_cantidad','2025-07-16 13:31:36.116612'),(59,'papeleria','0019_alter_articulo_cantidad_alter_articulo_observacion','2025-07-16 13:31:36.531472'),(60,'papeleria','0020_pedido_fecha_estado','2025-07-16 13:31:36.919333'),(61,'sessions','0001_initial','2025-07-16 13:31:37.773374');
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
INSERT INTO `django_session` VALUES ('dz3zx644fkqt1xz33yyq7u27rlm4c172','.eJxVjMEOgyAQBf-FszFsCwgem_Q7yAKrElETwFPTf69tPbTXN2_mwSzudbJ7oWxjYD0D1vxuDv1M6xuk6DLliO05lfa-YEy38_BnTVimQ5HKycCFJgJlpBlA6YsZ_OAcgeCBOoHOC92B5op7LzUdgIwDQJD-qo7oJ5e2caRg48r6mndqGCbKFW2pm5_tspWaMeAXPl94O0ck:1uc5V1:EXqjkntBopPoHPwAHcTWtooS0i2sgUrXcYhXC8ck0Bc','2025-07-16 17:10:55.942106'),('epjw52nk9s7xhq3pbaf17y78agewxf5s','.eJxVjMEOgyAQBf-FszFsCwgem_Q7yAKrElETwFPTf69tPbTXN2_mwSzudbJ7oWxjYD0D1vxuDv1M6xuk6DLliO05lfa-YEy38_BnTVimQ5HKycCFJgJlpBlA6YsZ_OAcgeCBOoHOC92B5op7LzUdgIwDQJD-qo7oJ5e2caRg48r6mndqGCbKFW2pm5_tspWaMeAXPl94O0ck:1uc93H:TgVSSrsWk7h_am2zg1V7rdbVkeq22504dPeQUAj-oCw','2025-07-16 20:58:31.315795'),('jj82h7a9yfix5544445zzcxvmwvisfpd','.eJxVjMEOgyAQBf-FszFsCwgem_Q7yAKrElETwFPTf69tPbTXN2_mwSzudbJ7oWxjYD0D1vxuDv1M6xuk6DLliO05lfa-YEy38_BnTVimQ5HKycCFJgJlpBlA6YsZ_OAcgeCBOoHOC92B5op7LzUdgIwDQJD-qo7oJ5e2caRg48r6mndqGCbKFW2pm5_tspWaMeAXPl94O0ck:1ucRT1:131LePIdrupoeaXSFTFHtSmSByC6CaxB4j5vRIy8BEs','2025-07-17 16:38:19.793138'),('qis3crdmt1a3yothlo48ilwcnace848p','.eJxtjMsOwiAQRf-FdWNAgUKXJn4HGYahJX0lQFfGf7eaLtS4Pefce2cOtjq4rVB2KbCOCdZ8Mg840vISU_KZcoLTgcrpNkOarkfwtRqgDPtEaa8Cl4ZIaKtsFNqcbcToPQnJA7USPErTCsM1R1SGdkHWCwFC4UXvp--7ae17Ci4trKt5o4bBRLmCK3XF0c1rqRkC_JUI8Sd4PAF0OFPN:1ucQfH:eGiEYznu9S4o5EI_1rCdbnMK8bOq7mINQZX0uRLcCks','2025-07-17 15:46:55.989828');
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
  `username` varchar(50) NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `libreria_customuser`
--

LOCK TABLES `libreria_customuser` WRITE;
/*!40000 ALTER TABLE `libreria_customuser` DISABLE KEYS */;
INSERT INTO `libreria_customuser` VALUES (1,'pbkdf2_sha256$1000000$ftXenUpxymjELJ27tApvUH$sgZGBv/twhYBCAgbBnNyTAcHday/NGWMJpOAdG4i9s0=','2025-07-17 16:19:59.452789',0,'Daniel Sanchez','jonnathansz73@gmail.com','Administrador','Aprendiz sena',1,0,'Administrativa','2025-07-16',1,1,1),(2,'pbkdf2_sha256$1000000$v8yZB3DvMHKkWJRbBIbh5B$3Rq0lXL5nmxNy8du5aPYi8cA6aO3W7dFKeRgot0issI=','2025-07-17 15:01:56.956376',0,'Viviana Rodriguez','viviana@gmail.com','Administrador','Asistente en gestion documental',1,0,'Administrativa','2025-07-16',1,1,1),(3,'pbkdf2_sha256$1000000$A9JNXj2slazLciMjzUkvaw$EMKgUv3GvK729H20FS8URlsIOP3MAIn5Gc7mSQFqYSA=','2025-07-17 15:32:56.163238',0,'Carlos Andres Orozco','carlos@gmail.com','Empleado','Auxiliar en gestion documental',1,0,'Administrativa','2025-07-16',1,1,1),(4,'pbkdf2_sha256$1000000$Nzx3vHs02JsaQZjg8Tcjr9$Ls9xhfEE0gw5+mrOgRZ6QMNogFr2Qv3UaDzt3qpBXDs=',NULL,0,'Diego Higuera','diego@gmail.com','Empleado','Auxiliar rues',1,0,'Registros públicos','2025-07-16',1,1,1),(5,'pbkdf2_sha256$1000000$sJt9K8MBj8ILQAWborKymk$pVV4vGLeR3eAeXEGPn06pTqsHSB6TfGwVWOg/is1uE8=',NULL,0,'Carolina Rua','carolina@gmail.com','Empleado','Auxiliar rues',1,0,'Registros públicos','2025-07-16',0,0,0),(6,'pbkdf2_sha256$1000000$3uNPsC5LopOnmU0Hm4HYsn$RFfz2oarPKw3I3lyAq8Ky8S9UooQfubDSYBPdl58dLI=','2025-07-16 16:26:17.294824',0,'Camila Ortega','camila@gmail.com','Empleado','Asistente de comunicaciones',1,0,'Presidencia','2025-07-16',0,0,1),(7,'pbkdf2_sha256$1000000$f8oegzGiHuPHkGiapAm60c$ymbegzbzQh4zp7FsSqVdSEaNgRYlpAqEeGP8j1pGpz4=',NULL,0,'Daniel Vargas','daniel@gmail.com','Empleado','Auxiliar de comunicaciones',1,0,'Presidencia','2025-07-16',0,0,0),(8,'pbkdf2_sha256$1000000$GXhW15jIWbG8V5c9Y5sMjT$a7QV6tymBvViDB15vfQDuswJKYuWC3REUFIbkd/mAQA=',NULL,0,'Diana C. Gomez','diana@gmail.com','Empleado','Asistente en gestion empresarial',1,0,'Gestión empresarial','2025-07-16',0,0,0),(9,'pbkdf2_sha256$1000000$v8Nxg4httKepKVyYn37qPt$wNB91lRKbkF/WNqAn3QXlk0ofNCO/at3i9QMVm6o6Gw=','2025-07-16 16:31:13.007055',0,'Freddy Monsalve','freddy@gmail.com','Empleado','Auxiliar en gestion empresarial',1,0,'Gestión empresarial','2025-07-16',0,0,1),(10,'pbkdf2_sha256$1000000$twCNVwSCIolNQsu25zjoJc$5HWzQVgoETArhlto5O5JvTCBqYvl2hQFC0T7MSHlAwg=',NULL,0,'Beatriz Sanabria','beatriz@gmail.com','Empleado','Tesorera',0,0,'Financiera','2025-07-16',0,0,1),(11,'pbkdf2_sha256$1000000$HBI1SGvYLFMuxJlcaN5Bt5$Ecir4kPpDRCLhcKFVwZdVsdo0vWWGWh+if9+mR8roxw=','2025-07-16 16:32:47.578333',0,'Freddy Camargo','freddyc@gmail.com','Empleado','Auxiliar contable',1,0,'Financiera','2025-07-16',0,0,1),(12,'pbkdf2_sha256$1000000$KPGMlPSN4yCwfwSPfytdvp$nOYApJJqM4xF16webpOfbaHRJpJTQNZxZlJ63xSl318=','2025-07-16 16:34:19.915423',0,'Hector Garcia','hector@gmail.com','Empleado','Asistente en competitividad',1,0,'Competitividad','2025-07-16',0,0,1),(13,'pbkdf2_sha256$1000000$HZOLk84uITBdy1Bsxrxzhh$KB6Wm3UoXTY14gDsnX5lfgeOfjoNphWUKMBXp04a1P8=',NULL,0,'Brayan Ceron','brayan@gmail.com','Empleado','Supernumerario en competividad',1,0,'Competitividad','2025-07-16',0,0,0);
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
  `nombre` varchar(40) NOT NULL,
  `marca` varchar(30) NOT NULL,
  `observacion` varchar(50) DEFAULT NULL,
  `tipo` varchar(30) DEFAULT NULL,
  `precio` bigint unsigned NOT NULL,
  `cantidad` int unsigned NOT NULL,
  `fecha_registro` date NOT NULL,
  `registrado_por_id` bigint DEFAULT NULL,
  `proveedor` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `papeleria_articulo_registrado_por_id_0c2be10e_fk_libreria_` (`registrado_por_id`),
  CONSTRAINT `papeleria_articulo_registrado_por_id_0c2be10e_fk_libreria_` FOREIGN KEY (`registrado_por_id`) REFERENCES `libreria_customuser` (`id`),
  CONSTRAINT `papeleria_articulo_chk_1` CHECK ((`precio` >= 0)),
  CONSTRAINT `papeleria_articulo_chk_2` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `papeleria_articulo`
--

LOCK TABLES `papeleria_articulo` WRITE;
/*!40000 ALTER TABLE `papeleria_articulo` DISABLE KEYS */;
INSERT INTO `papeleria_articulo` VALUES (3,'Resma de papel membreteada','Norma','N/a','Carta',5630,35,'2025-07-16',1,'Javeriana'),(4,'Sobres de manila','Bic','No hay','Oficio',16666,16,'2025-07-16',1,'Javeriana'),(5,'Sobres de manila','No tiene','No hay','Carta',5555,5,'2025-07-16',1,'Javeriana'),(6,'Lapiz','Bic','Ninguna','Rojo',2000,44,'2025-07-16',1,'Javeriana'),(7,'Tijeras','Norma','No hay','Punta roma',3000,22,'2025-07-16',1,'Roma ltda.');
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
  `fecha_estado` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `papeleria_pedido_registrado_por_id_b6a945d7_fk_libreria_` (`registrado_por_id`),
  CONSTRAINT `papeleria_pedido_registrado_por_id_b6a945d7_fk_libreria_` FOREIGN KEY (`registrado_por_id`) REFERENCES `libreria_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `papeleria_pedido`
--

LOCK TABLES `papeleria_pedido` WRITE;
/*!40000 ALTER TABLE `papeleria_pedido` DISABLE KEYS */;
INSERT INTO `papeleria_pedido` VALUES (1,'2025-07-16 13:58:21.229000','Confirmado',1,'2025-07-16 13:58:21.229000'),(2,'2025-07-16 15:38:03.366000','Confirmado',1,'2025-07-16 15:38:03.366000'),(3,'2025-07-16 16:26:30.716282','Confirmado',6,NULL),(4,'2025-07-16 16:28:11.431447','Confirmado',9,NULL),(5,'2025-07-16 16:31:39.149643','Confirmado',9,NULL),(6,'2025-07-16 16:32:54.462733','Confirmado',11,NULL),(7,'2025-07-16 16:34:29.713992','Confirmado',12,NULL),(8,'2025-07-16 16:53:54.720367','Confirmado',1,'2025-07-16 16:53:54.720186');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `papeleria_pedidoarticulo`
--

LOCK TABLES `papeleria_pedidoarticulo` WRITE;
/*!40000 ALTER TABLE `papeleria_pedidoarticulo` DISABLE KEYS */;
INSERT INTO `papeleria_pedidoarticulo` VALUES (1,1,3,'Carta',3,'Presidencia'),(3,10,4,'Oficio',4,'Gestión empresarial'),(4,1,3,'Carta',4,'Gestión empresarial'),(7,1,3,'Carta',5,'Gestión empresarial'),(10,1,3,'Carta',8,'Administrativa');
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

-- Dump completed on 2025-07-17 11:29:14
