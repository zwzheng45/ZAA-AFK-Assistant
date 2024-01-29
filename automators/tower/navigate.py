from log import *
import match
import adb
import os
import notification

path="./assets/tower/"

skip_threshold=3

# 读取json中的silence
with open('config.json','r') as f:
    config=json.load(f)
    if config['silence']=='1':
        silence=True
    else:
        silence=False

def climb_tower(trial=0,mirror=False):
    adb.capture_screen()
    start_pos=match.match(os.path.join(path,"start_challenge.png"))
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
                return climb_tower()

            log("跳过",2)
            break
        log("未能找到开始按钮，重试",2)
        adb.capture_screen()
        start_pos=match.match(os.path.join(path,"start_challenge.png"))
        i+=1
    if(i<skip_threshold):
        adb.click(start_pos[0],start_pos[1])

    start_pos=match.match(os.path.join(path,"start_combact.png"))
    i=0
    if(mirror==True):
        mirror_line_up()
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
        start_pos=match.match(os.path.join(path,"fail.png"))
        if(start_pos!=None):
            if(trial<=6 and trial%2==0):
                log("战斗失败...尝试重试(%d/6)"%trial,1)
                adb.click(start_pos[0],start_pos[1])
                return climb_tower(trial+1)
            elif(trial<=6 and trial%2==1):
                log("战斗失败...尝试自动镜像站队后重试(%d/6)"%trial,1)
                adb.click(start_pos[0],start_pos[1])
                return climb_tower(trial+1,True)
            else:
                log("练度过低，打不过...调整队伍后回车返回...(7/6)",1)
                notification.failure_warning()
                input()
                return -1
        log("未检测到胜利，重试",2)
        adb.capture_screen()
        start_pos=match.match(os.path.join(path,"finish_fight.png"))
    adb.click(start_pos[0],start_pos[1])
    print("\033[0;32m战斗完成\033[0m")

    return 0

def mirror_line_up():
    log("镜像站队",3)
    first_pos=None
    second_pos=None
    while(first_pos==None or second_pos==None):
        adb.capture_screen()
        for root,dirs,files in os.walk(path):
            for target in files:
                if target.startswith("Rem") and first_pos==None:
                    x=match.match(os.path.join(path,target))
                    if(x!=None):
                        first_pos=x
                if target.startswith("zhujiao") and second_pos==None:
                    y=match.match(os.path.join(path,target))
                    if(y!=None):
                        second_pos=y
                if(first_pos!=None and second_pos!=None):
                    break
    adb.swipe(first_pos[0],first_pos[1],second_pos[0],second_pos[1],200)