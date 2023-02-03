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

 Date: 03/02/2023 16:58:56
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_mask_content
-- ----------------------------
DROP TABLE IF EXISTS `tb_mask_content`;
CREATE TABLE `tb_mask_content`  (
  `content_id` int NOT NULL AUTO_INCREMENT,
  `video_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `post_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`content_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_mask_content
-- ----------------------------
INSERT INTO `tb_mask_content` VALUES (1, "I think my fave affordable loose powder\\n\r\nwhich like blurs your under eyes makes\r\nthem look flawless makes you not crease\\n\r\nnow comes in a pink shade this is the \r\nbest affordasble loose power lown.", "A NEW affordable Pink Setting Powder, what do we think? #testingnewmakeup #pinksettingpowder #flawlessundereye");
INSERT INTO `tb_mask_content` VALUES (2, "This stopped my hair loss and scalp is much thicker than before.rosemary oil is a miracle 😊", "Rosemary Water Hair Routine✨ If you oiling Your Scalp is too much work for you, Rosemary water is for you. #rosemarywater #rosemarywaterforhairgrowth #rosemarywaterforhair #rosemarywaterbenefits #rosemarywaterspray #rosemarywaterresults#GoforLoveGiftforYou");
INSERT INTO `tb_mask_content` VALUES (3, "Rosemary oil for hair growth😍", "I\'ll keep y\'all posted but def seeing a\ndifference #hairthinning #rosemarywater\n#haircare #thinhairproblems#GoforLoveGiftforYou");
INSERT INTO `tb_mask_content` VALUES (4, "I\'m Sooo annoye! !\ni got these for £29 and\nNow\nthey are half price😍", "gotta be joking 😭 #pickle tviralpicke tviralpicklesnack#hotpickle #garlicpickles##GoforLoveGiftforYou");
INSERT INTO `tb_mask_content` VALUES (5, "12 shades of BFF Bronzing\nFace Frosting😍\nWorth than ￡50\nOnly ￡16.5", "The most gorgeous shades!#fyp#pinkhoney #bronzer #creambronze#GoforLoveGiftforYou");

SET FOREIGN_KEY_CHECKS = 1;
