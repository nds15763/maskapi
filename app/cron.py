from datetime import datetime
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
import configparser
import os

class Upload:
    def readUploadFile(self):
        curpath = os.path.dirname(os.path.realpath(__file__))
        cfgpath = os.path.join(curpath, "upload.ini")
        print('读取配置文件成功: +',cfgpath)  # cfg.ini的路径
        # 创建管理对象
        conf = configparser.ConfigParser()
        # 读ini文件
        conf.read(cfgpath, encoding="utf-8")  # python3
        return conf

    def cron_job(self):
        conf = self.readUploadFile()
        allUploadTaskID = dict(conf["upload_file"])

 
# scheduler = BackgroundScheduler()
# #每小时一次
# scheduler.add_job(cron_job, 'interval', hours=1)
 
# scheduler.start()