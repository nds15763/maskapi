from . import models, database
from fastapi import FastAPI, File, UploadFile,Request
import pymysql
import time

def open():
    return pymysql.connect(host='localhost',
                        user='root',
                        password='root',
                        database='mask_db')

def fetch(sql:str):
    # 打开数据库连接
    db = open()
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        return cursor.fetchall()
    except pymysql.Error as e:  
        print(e.args[0], e.args[1])
        # 如果发生错误则回滚
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()

def exec(sql:str):
    # 打开数据库连接
    db = open()
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except pymysql.Error as e:  
        print(e.args[0], e.args[1])
        # 发生错误时回滚
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()


def GetCreative(creative_id:int):
    dbModel = models.DBMaskCreative
    sql = "SELECT * FROM tb_mask_creative \
        WHERE creative_id = %d" % creative_id
    re = dbModel.toModelFirstLine(dbModel,fetch(sql))
    return re

def GetVideo(video_id:int):
    dbModel = models.DBMaskVideo
    # SQL 插入语句
    sql = "SELECT * FROM tb_mask_video \
        WHERE video_id = %d" % video_id
    re = dbModel.toModelFirstLine(dbModel,fetch(sql))
    return re

def GetPicture(pic_id:int):
    dbModel = models.DBMaskPicture
    # SQL 插入语句
    sql = "SELECT * FROM tb_mask_picture \
        WHERE pic_id = %d" % pic_id
    re = dbModel.toModelFirstLine(dbModel,fetch(sql))
    return re

def GetTask(task_id:int):
    dbModel = models.DBMaskTask
    # SQL 插入语句
    sql = "SELECT * FROM tb_mask_task \
        WHERE task_uuid = '%s'" % task_id
    re = dbModel.toModelFirstLine(dbModel,fetch(sql))
    return re

def CreateTask(task_id:str,creative_id:int):
    # SQL 插入语句
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    sql = "INSERT INTO tb_mask_task VALUES ('%s',%d,%d,'','%s');" % (task_id,creative_id,0,now)
    re = exec(sql)
    return re

def UpdateTask(status:int,task_id:str,video_src:str):
    # SQL 插入语句
    sql ="""UPDATE tb_mask_task SET status = %d, out_video_src= '%s' WHERE task_uuid = '%s';""" %(status,video_src,task_id)
    re = exec(sql)
    return re

def GetContent(content_id:int):
    dbModel = models.DBMaskContent
    sql = "SELECT * FROM tb_mask_content \
        WHERE content_id = %d" % content_id
    re = dbModel.toModelFirstLine(dbModel,fetch(sql))
    return re