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

 Date: 02/02/2023 20:00:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_mask_video
-- ----------------------------
DROP TABLE IF EXISTS `tb_mask_video`;
CREATE TABLE `tb_mask_video`  (
  `video_id` int NOT NULL AUTO_INCREMENT,
  `video_src` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '视频存放地址',
  `video_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '视频保存时的名称',
  `video_account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '视频账号来源',
  `create_time` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`video_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_mask_video
-- ----------------------------
INSERT INTO `tb_mask_video` VALUES (1, NULL, 'tmp_vitamin_babe_video.mp4', NULL, '2023-02-02 17:53:29');

SET FOREIGN_KEY_CHECKS = 1;
