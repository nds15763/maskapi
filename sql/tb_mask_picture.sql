/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80032
 Source Host           : localhost:3306
 Source Schema         : mask_db

 Target Server Type    : MySQL
 Target Server Version : 80032
 File Encoding         : 65001

 Date: 03/02/2023 16:59:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_mask_picture
-- ----------------------------
DROP TABLE IF EXISTS `tb_mask_picture`;
CREATE TABLE `tb_mask_picture`  (
  `pic_id` int NOT NULL AUTO_INCREMENT,
  `pic_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`pic_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_mask_picture
-- ----------------------------
INSERT INTO `tb_mask_picture` VALUES (1, 'kimilo_shoper.jpg');

SET FOREIGN_KEY_CHECKS = 1;
