from datetime import datetime
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
import configparser
import os

class Upload:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def readUploadFile(self):
        curpath = os.path.dirname(os.path.realpath(__file__))
        cfgpath = os.path.join(curpath, "upload.ini")
        print('读取配置文件成功: +',cfgpath)  # cfg.ini的路径
        # 创建管理对象
        conf = configparser.ConfigParser()
        # 读ini文件
        conf.read(cfgpath, encoding="utf-8")  # python3
        return conf

    def deleteUploadFile(self):
        conf = self.readUploadFile()
        allUploadTaskID = dict(conf["upload_file"])

    def deleteUploadFileCron(self):
        self.scheduler.add_job(self.deleteUploadFile, 'interval', hours=1)
 
    def cronStart(self):
        self.scheduler.start()