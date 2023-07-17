/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100428
 Source Host           : localhost:3306
 Source Schema         : uso_dev

 Target Server Type    : MySQL
 Target Server Version : 100428
 File Encoding         : 65001

 Date: 17/07/2023 17:01:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for uso_product
-- ----------------------------
DROP TABLE IF EXISTS `uso_product`;
CREATE TABLE `uso_product`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '产品id',
  `product_name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL COMMENT '产品名称',
  `product_dir` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL COMMENT '产品路径',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of uso_product
-- ----------------------------
INSERT INTO `uso_product` VALUES (1, 'plouise bad bitch', 'D:\\uso_ftp\\sucai\\plouise_bad_bitch');

-- ----------------------------
-- Table structure for uso_video
-- ----------------------------
DROP TABLE IF EXISTS `uso_video`;
CREATE TABLE `uso_video`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '视频id',
  `video_name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL COMMENT '视频文件名称',
  `video_fullpath` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL COMMENT '视频全路径',
  `video_length` double NULL DEFAULT NULL COMMENT '视频长度（2.5，5，7.5）',
  `product_id` int NOT NULL COMMENT '对应产品id',
  `update_time` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `video_type` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL COMMENT '视频标签',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of uso_video
-- ----------------------------
INSERT INTO `uso_video` VALUES (1, 'c1025.mp4', 'D:\\uso_ftp\\sucai\\plouise_bad_bitch\\2.5\\c1025.mp4', 2.5, 1, '2023-07-17 13:12:41', NULL);
INSERT INTO `uso_video` VALUES (2, 'c2025.mp4', 'D:\\uso_ftp\\sucai\\plouise_bad_bitch\\2.5\\c2025.mp4', 2.5, 1, '2023-07-17 13:12:41', NULL);
INSERT INTO `uso_video` VALUES (3, 'b1050.mp4', 'D:\\uso_ftp\\sucai\\plouise_bad_bitch\\5\\b1050.mp4', 5, 1, '2023-07-17 13:19:18', NULL);
INSERT INTO `uso_video` VALUES (4, 'b2050.mp4', 'D:\\uso_ftp\\sucai\\plouise_bad_bitch\\5\\b2050.mp4', 5, 1, '2023-07-17 13:40:51', NULL);
INSERT INTO `uso_video` VALUES (5, 'a1075.mp4', 'D:\\uso_ftp\\sucai\\plouise_bad_bitch\\7.5\\a1075.mp4', 7.5, 1, '2023-07-17 13:41:41', NULL);
INSERT INTO `uso_video` VALUES (6, 'a2075.mp4', 'D:\\uso_ftp\\sucai\\plouise_bad_bitch\\7.5\\a2075mp4', 7.5, 1, '2023-07-17 13:42:39', NULL);

SET FOREIGN_KEY_CHECKS = 1;
