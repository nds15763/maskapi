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

 Date: 03/02/2023 16:59:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_mask_creative
-- ----------------------------
DROP TABLE IF EXISTS `tb_mask_creative`;
CREATE TABLE `tb_mask_creative`  (
  `creative_id` int NOT NULL AUTO_INCREMENT,
  `video_id` int NULL DEFAULT NULL,
  `pic_id` int NULL DEFAULT NULL,
  `content_id` int NULL DEFAULT NULL,
  `product_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`creative_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_mask_creative
-- ----------------------------
INSERT INTO `tb_mask_creative` VALUES (1, 1, 1, 1, 1);
INSERT INTO `tb_mask_creative` VALUES (2, 2, 1, 2, 1);
INSERT INTO `tb_mask_creative` VALUES (3, 3, 1, 3, 1);
INSERT INTO `tb_mask_creative` VALUES (4, 4, 1, 4, 1);
INSERT INTO `tb_mask_creative` VALUES (5, 5, 1, 5, 1);
INSERT INTO `tb_mask_creative` VALUES (6, 6, 1, 6, 1);

SET FOREIGN_KEY_CHECKS = 1;
