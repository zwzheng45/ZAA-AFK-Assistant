from log import *
import match
import adb
import os

path="./assets/"

skip_threshold=3

def main_mission():

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

    start_pos=match.match(os.path.join(path,"finish_fight.png"))
    while(start_pos==None):
        log("未检测到胜利，重试",2)
        adb.capture_screen()
        start_pos=match.match(os.path.join(path,"finish_fight.png"))
    adb.click(start_pos[0],start_pos[1])
    print("\033[0;32m战斗完成\033[0m")

    return main_mission()
