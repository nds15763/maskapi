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

 Date: 02/02/2023 19:12:32
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_mask_product
-- ----------------------------
DROP TABLE IF EXISTS `tb_mask_product`;
CREATE TABLE `tb_mask_product`  (
  `product_id` int NOT NULL AUTO_INCREMENT COMMENT '产品ID',
  `video_id` int NULL DEFAULT NULL COMMENT '视频素材ID',
  `content_id` int NULL DEFAULT NULL COMMENT '文案素材ID',
  PRIMARY KEY (`product_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
