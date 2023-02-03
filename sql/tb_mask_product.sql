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

 Date: 03/02/2023 16:59:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_mask_product
-- ----------------------------
DROP TABLE IF EXISTS `tb_mask_product`;
CREATE TABLE `tb_mask_product`  (
  `product_id` int NOT NULL AUTO_INCREMENT COMMENT '产品ID',
  `product_src` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`product_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_mask_product
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
