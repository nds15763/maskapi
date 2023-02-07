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

 Date: 06/02/2023 18:33:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_mask_product
-- ----------------------------
DROP TABLE IF EXISTS `tb_mask_product`;
CREATE TABLE `tb_mask_product`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL COMMENT '产品ID',
  `product_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `product_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_mask_product
-- ----------------------------
INSERT INTO `tb_mask_product` VALUES (1, 1, 'vitamin babe setting');
INSERT INTO `tb_mask_product` VALUES (2, 2, 'Rosemary Oil For Hair');
INSERT INTO `tb_mask_product` VALUES (3, 3, 'PLouise The Cheek Of It Liquid Blush');
INSERT INTO `tb_mask_product` VALUES (4, 4, 'BFF BRONZING FACE FROSTING');

SET FOREIGN_KEY_CHECKS = 1;
