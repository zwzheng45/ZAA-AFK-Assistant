from log import *
import match
import adb
import os
import notification

from time import sleep

path="./assets/mainpage/"

skip_threshold=3

# 读取json中的silence
with open('config.json','r') as f:
    config=json.load(f)
    if config['silence']=='1':
        silence=True
    else:
        silence=False

def main_mission():
    adb.capture_screen()
    start_pos=match.match(os.path.join(path,"start.png"))
    i=0
    while(start_pos==None):
        if(i>=skip_threshold):
            #检查是否升级
            log("未能找到开始按钮，检查是否被升级窗口挡住",2)
            start_pos=match.match(os.path.join(path,"level_up.png"))
            j=0
            while (start_pos==None):
                if (j>=skip_threshold):
                    log("跳过",2)
                    break
                log("未能找到升级，重试",2)
                adb.capture_screen()
                start_pos=match.match(os.path.join(path,"level_up.png"))
                j+=1
            if (j<skip_threshold):
                adb.click(start_pos[0],start_pos[1])
                return main_mission()

            log("跳过",2)
            break
        log("未能找到开始按钮，重试",2)
        adb.capture_screen()
        start_pos=match.match(os.path.join(path,"start.png"))
        i+=1
    if(i<skip_threshold):
        adb.click(start_pos[0],start_pos[1])

    start_pos=match.match(os.path.join(path,"start_confirm.png"))
    i=0
    while(start_pos==None):
        if(i>=skip_threshold):
            log("跳过",2)
            break
        log("未能找到确认开始战斗按钮，重试",2)
        adb.capture_screen()
        start_pos=match.match(os.path.join(path,"start_confirm.png"))
        i+=1
    if(i<skip_threshold):
        adb.click(start_pos[0],start_pos[1])

    start_pos=match.match(os.path.join(path,"start_combact.png"))
    i=0
    while(start_pos==None):
        if(i>=skip_threshold):
            log("跳过",2)
            break
        log("未能找到开始战斗按钮，重试",2)
        adb.capture_screen()
        start_pos=match.match(os.path.join(path,"start_combact.png"))
        i+=1
    if(i<skip_threshold):
        adb.click(start_pos[0],start_pos[1])

    sleep(2) # 至少两秒才会结束战斗吧？
    start_pos=match.match(os.path.join(path,"finish_fight.png"))
    while(start_pos==None):


        log("检测是否卡在主页面的某个地方",3)
        start_pos=match.match(os.path.join(path,"start.png"))
        if(start_pos!=None):
            return main_mission()

        start_pos=match.match(os.path.join(path,"start_confirm.png"))
        if (start_pos!=None):
            return main_mission()

        log("检测是否失败",3)
        start_pos=match.match(os.path.join(path,"fail.png"))
        if(start_pos!=None):
            log("练度过低，打不过...调整队伍后回车返回...",1)
            notification.failure_warning()
            input()
            return -1
        start_pos=match.match(os.path.join(path,"new_map.png"))
        log("检测是否需要手动开启地图新区域",3)
        if(start_pos!=None):
            log("需手动开启地图新区域，请确认后回车继续...",1)
            notification.push_notification("需手动开启地图新区域","","请确认后回车继续...")
            notification.play_warning_sound()
            input()
            return main_mission()

        log("未检测到胜利，重试",2)
        adb.capture_screen()
        start_pos=match.match(os.path.join(path,"finish_fight.png"))
    adb.click(start_pos[0],start_pos[1])
    print("\033[0;32m战斗完成\033[0m")


    return main_mission()
