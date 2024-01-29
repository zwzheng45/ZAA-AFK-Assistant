from log import *
import match
import adb
import os
import pygame
from time import sleep

path="./assets/infinite_pulls/"

skip_threshold=5



def re_pull():
    # 从pull.json中读取target_1和target_2
    with open("pull.json","r") as f:
        pull_json=f.read()
    pull_json=eval(pull_json)
    target_1_count=int(pull_json["target_1"])
    target_2_count=int(pull_json["target_2"])
    total_count=int(pull_json["total"])+1

    adb.capture_screen()
    re_pull_pos=match.match(os.path.join(path,"retry.png"))
    i=0
    while(re_pull_pos==None):
        if(i>=skip_threshold):
            log("跳过(%d/%d)"%(i,skip_threshold),1)
            break
        log("未能找到再次召唤按钮，重试(%d/%d)"%(i,skip_threshold),2)
        adb.capture_screen()
        re_pull_pos=match.match(os.path.join(path,"retry.png"))
        i+=1
    if(i<skip_threshold):
        adb.click(re_pull_pos[0],re_pull_pos[1])

    adb.capture_screen()
    re_pull_pos=match.match(os.path.join(path,"quick_show.png"))
    i=0
    while(re_pull_pos==None):
        if(i>=skip_threshold):
            log("跳过(%d/%d)"%(i,skip_threshold),1)
            break
        log("未能找到快速翻卡按钮，重试(%d/%d)"%(i,skip_threshold),2)
        adb.capture_screen()
        re_pull_pos=match.match(os.path.join(path,"quick_show.png"))
        i+=1
    if(i<skip_threshold):
        # 找到翻卡后点击两下才能跳过
        adb.click(re_pull_pos[0],re_pull_pos[1])
        sleep(0.5)
        adb.click(re_pull_pos[0],re_pull_pos[1])
        adb.click(re_pull_pos[0],re_pull_pos[1])

    # 等五秒跳过动画
    sleep(3)

    log("判断卡组",3)
    adb.capture_screen()
    target=os.path.join(path,"target_1.png")
    log("寻找%s"%target,3)
    x=match.match(target)
    if(x!=None):
        print("\033[7;36;40m第%d次抽到%s！正在判断紫色卡组\n\033[0m"%(target_1_count,target),end='')
        target_1_count+=1
        target=os.path.join(path,"target_2.png")
        log("寻找%s"%target,3)
        x=match.match(target)
        if(x!=None):
            target_2_count+=1
            print("\033[5;36;40m第%d次抽到%s！符合条件，保留卡组并停止抽取\n\033[0m"%(target_2_count,target))
            target=os.path.join(path,"record.png")
            record_pos=match.match(target)
            adb.click(record_pos[0],record_pos[1])
            sleep(0.1) #稳
            adb.capture_screen()
            target=os.path.join(path,"replace.png")
            replace_pos=match.match(target)
            adb.click(replace_pos[0],replace_pos[1])
            return 1
        else:
            print("不符合紫色条件，继续重新抽取")
    else:
        target=os.path.join(path,"target_2.png")
        log("寻找%s"%target,3)
        x=match.match(target)
        if(x!=None):
            target_2_count+=1
            print("\033[7;36;40m第%d次抽到%s\n\033[0m"%(target_2_count,target))



    #将抽取结果写入pull.json
    pull_json["target_1"]=target_1_count
    pull_json["target_2"]=target_2_count
    pull_json["total"]=total_count
    with open("pull.json","w") as f:
        f.write(str(pull_json))

    return 0