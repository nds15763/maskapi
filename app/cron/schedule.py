import cron.schedule as schedule
import time

# 定义你要周期运行的函数
def job():
    print("I'm working...")

schedule.every().hour.do(job)                    # 每隔 1 小时运行一次 job 函数

while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(1)