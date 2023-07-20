from . import models, database
from fastapi import FastAPI, File, UploadFile,Request
import pymysql
import time

def open():
    return pymysql.connect(host='localhost',
                        user='root',
                        password='root',
                        database='uso_dev', charset='utf8', use_unicode=True)
#服务器密码1qaz!QAZ

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
    except Exception as e: 
        print(e.args[0], e.args[1])
        # 发生错误时回滚
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()


def GetProduct(product_id:int):
    dbModel = models.UsoProduct
    sql = "SELECT * FROM uso_product \
        WHERE id = %d" % product_id
    re = dbModel.toModelFirstLine(dbModel,fetch(sql))
    return re

def GetProductList():
    dbModel = models.UsoProduct
    sql = "SELECT id,product_name FROM uso_product"
    re = dbModel.toModelList(dbModel,fetch(sql))
    return re

def CreateVideo(video_name:str,video_fullpath:str,video_length:float,product_id:int,video_type:str):
    video_fullpath = video_fullpath.replace('\\', '\\\\')
    # SQL 插入语句
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    sql = "INSERT INTO uso_video ( `video_name`, `video_fullpath`, `video_length`, `product_id`, `update_time`, `video_type`) VALUES ('{video_name}', '{video_fullpath}', {video_length}, {product_id}, '{update_time}', '{video_type}');".format(
    video_name=video_name, 
    video_fullpath=video_fullpath,
    video_length = video_length,
    product_id = product_id,
    update_time = now,
    video_type = video_type
    )
    re = exec(sql)
    return re

def UpdateTask(status:int,task_id:str,video_src:str):
    # SQL 插入语句
    sql ="""UPDATE tb_mask_task SET status = %d, out_video_src= '%s' WHERE task_uuid = '%s';""" %(status,video_src,task_id)
    re = exec(sql)
    return re

def GetVideoIDList(product_id:int,video_length:float):
    dbModel = models.UsoVideo
    sql = "select id from uso_video where product_id = %d and video_length =" % product_id + str(video_length)
    re = dbModel.toIDList(dbModel,fetch(sql))
    return re

def GetVideoList(product_ids:str):
    dbModel = models.UsoVideo
    sql = "select * from uso_video where id in (%s) " % product_ids
    re = dbModel.toModelList(dbModel,fetch(sql))
    return re

def CreateVideoLog(status:int,task_id:str,video_src:str):
    # SQL 插入语句
    sql ="""UPDATE tb_mask_task SET status = %d, out_video_src= '%s' WHERE task_uuid = '%s';""" %(status,video_src,task_id)
    re = exec(sql)
    return re


def CreateVideoToken(token:str,status:int,create_time:str):
    # SQL 插入语句
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    sql ="INSERT INTO `uso_dev`.`uso_download_token` (`token`, `status`, `create_time`) VALUES ('%s', %d, '%s');" %(token,0,now)
    re = exec(sql)
    return re

def CreateProdut(product_name:str,product_path:str):
    # SQL 插入语句
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    sql ="INSERT INTO `uso_dev`.`uso_product` ( `product_name`, `product_dir`) VALUES \
    ('%s', '%s');"%(product_name,product_path)
    re = exec(sql)
    return re