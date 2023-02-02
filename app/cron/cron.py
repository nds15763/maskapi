from conf.conf import Conf
import os
import datetime

class CronJob:
    def CronDeleteUploadedFile():
        #每天夜里2点，删除上传过的照片和视频
        if datetime.datetime.now().hour == 4:
            conf = Conf()

            img_list = []
            for root, dirs, files in os.walk(conf.uploadImgPath):
                img_list.append(root)
                print("执行定时任务:删除上传照片文件")
                print("共清理:"+files.count()+"个")
            for name in files:
                if name.casefold().endswith(".png" ) or name.casefold().endswith(".jpg") or name.casefold().endswith(".webp") or name.casefold().endswith(".jpeg"):
                    os.remove(os.path.join(root, name))


            video_list = []
            for root, dirs, files in os.walk(conf.uploadVideoPath):
                video_list.append(root)
                print("执行定时任务:删除上传视频文件")
                print("共清理:"+files.count()+"个")
            for name in files:
                if name.casefold().endswith(".mp4"):
                    os.remove(os.path.join(root, name))

            out_video_list = []
            for root, dirs, files in os.walk(conf.outputVideoPath):
                out_video_list.append(root)
                print("执行定时任务:删除生成视频文件")
                print("共清理:"+files.count()+"个")
            for name in files:
                if name.casefold().endswith(".mp4"):
                    os.remove(os.path.join(root, name))