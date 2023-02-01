import configparser
import os

class Conf:
    uploadImgPath = ""
    uploadVideoPath = ""
    outputVideoPath = ""
    httpcode = {}
    def __init__(self):
        self.curpath = os.path.dirname(os.path.realpath(__file__))
        self.cfgpath = os.path.join(self.curpath, "web.ini")
        print('读取配置文件成功: +',self.cfgpath)  # cfg.ini的路径
        # 创建管理对象
        self.conf = configparser.ConfigParser()
        # 读ini文件
        self.conf.read(self.cfgpath, encoding="utf-8")  # python3
        # 获取所有的section
        sections = self.conf.sections()
        
        print(sections)  # 返回list
        self.uploadImgPath = self.conf["upload_path"]["upload_img_path"]
        self.uploadVideoPath = self.conf["upload_path"]["upload_video_path"]
        self.outputVideoPath = self.conf["upload_path"]["output_video_path"]
        self.httpcode = dict(self.conf["http_code"])
        