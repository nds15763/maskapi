# Import everything needed to edit video clips
from moviepy.editor import *
import cv2
import numpy as np



def picToImgMask(video):
    mask = (ImageClip("t1.png")
    .set_duration(video.duration) 
    .resize(video.size))
    CompositeVideoClip([video, mask]).write_videofile("out1.mp4")

def openVideo(vPath):
    clip = VideoFileClip(vPath)
    return clip

def greenScrean():
    # todo 读取并转换图片格式
    opencv = cv2.imread("677d5c21c813411ea09183c292644322q.jpg")
    hsv = cv2.cvtColor(opencv, cv2.COLOR_RGB2HSV)

    # todo 指定绿色范围,60表示绿色，我取的范围是-+10
    minGreen = np.array([40, 100, 100])
    maxGreen = np.array([80, 255, 255])

    # todo 确定绿色范围
    mask = cv2.inRange(hsv, minGreen, maxGreen)

    # todo 确定非绿色范围
    mask_not = cv2.bitwise_not(mask)

    # todo 通过掩码控制的按位与运算锁定绿色区域
    green = cv2.bitwise_and(opencv, opencv, mask=mask)

    # todo 通过掩码控制的按位与运算锁定非绿色区域
    green_not = cv2.bitwise_and(opencv, opencv, mask=mask_not)

    # todo 拆分为3通道
    b, g, r = cv2.split(green_not)

    # todo 合成四通道
    bgra = cv2.merge([b, g, r, mask_not])

    # todo 保存带有透明通道的png图片,有了这种素材之后，就可以给这张图片替换任意背景了
    cv2.imwrite("t1.png",bgra)


#图片扣色，或者扣好了传上去也行
greenScrean()
#打开视频
video = openVideo("2.mp4")
#制作遮罩层
picToImgMask(video)