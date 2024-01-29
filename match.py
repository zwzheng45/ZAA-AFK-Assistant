import cv2
import os
import numpy as numby # (ゝ∀･)

import adb
from log import *

trust_threshold=0.87


def cur_location(trials=0,silent=False):
    log("开始识别所在界面...",3)
    log("读取截图... ",3,False)
    screenshot=cv2.imread("./tmp.png",cv2.IMREAD_GRAYSCALE)
    for root,dirs,files in os.walk("./assets"):
        for target in files:
            if target.startswith("isin_"):
                template=cv2.imread(os.path.join(root,target),cv2.IMREAD_GRAYSCALE)
                res=cv2.matchTemplate(screenshot,template,cv2.TM_CCOEFF_NORMED)
                min_val,max_val,_,_=cv2.minMaxLoc(res)
                log("对比%s，可信度：%f；"%(target,max_val),3,False,False)
                if max_val>trust_threshold:
                    log("",3,True,False)
                    cur_scene_name=target.replace("isin_","").replace(".png","")
                    log("匹配成功，目前处于%s"%cur_scene_name,3,True)
                    if (cur_scene_name=="item_received"):
                        log("关闭获得新物品界面",3)
                        x=match("./assets/global/close_item_received.png")
                        adb.click(x[0],x[1])
                        adb.capture_screen()
                        return cur_location()
                    return cur_scene_name
    else:
        if trials<5:
            if not silent:
                log("",2,True,False)
                log("未能识别当前界面，重试(%d/5)"%trials,2)
            log("",3,True,False)
            adb.capture_screen()
            return cur_location(trials+1,silent)
        else:
            if not silent:
                log("",1,True,False)
                log("无法识别所在界面(%d/5)"%trials,1)
            log("",3,True,False)
            return None


def match(path):
    log("读取截图... ",3,False)
    screenshot=cv2.imread("./tmp.png",cv2.IMREAD_GRAYSCALE)
    template=cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    res=cv2.matchTemplate(screenshot,template,cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)
    if max_val>trust_threshold:
        log("匹配%s成功，可信度：%f"%(path,max_val),3,True,False)
        match_x=max_loc[0]+template.shape[1]/2
        match_y=max_loc[1]+template.shape[0]/2
        return match_x,match_y
    else:
        log("匹配%s失败，可信度：%f"%(path,max_val),2,True,False)
        return None


def match_multi(path):
    log("读取截图... ",3,False)
    screenshot=cv2.imread("./tmp.png",cv2.IMREAD_GRAYSCALE)
    template=cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    res=cv2.matchTemplate(screenshot,template,cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)

    matches=[]

    while max_val>trust_threshold:
        log("匹配成功，在(%d,%d)，可信度：%f；"%(max_loc[0],max_loc[1],max_val),3,False,False)
        match_x=max_loc[0]
        match_y=max_loc[1]
        matches.append((match_x,match_y))

        # 在原始图像中标记找到的匹配区域
        w,h=template.shape[::-1]
        cv2.rectangle(screenshot,max_loc,(max_loc[0]+w,max_loc[1]+h),(0,255,255),2)

        # 将已经找到的区域置为0，避免重复匹配
        mask=numby.zeros_like(res)
        mask[max_loc[1]:max_loc[1]+h,max_loc[0]:max_loc[0]+w]=1
        res*=(1-mask)

        # 继续寻找下一个匹配
        min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)
    log("",3,True,False)
    if matches:
        return matches
    else:
        log("未匹配到目标",2)
        return None


def test_match(filename):
    global trust_threshold
    log("测试：匹配%s.png"%filename,3)
    screenshot=cv2.imread("./tmp.png",cv2.IMREAD_GRAYSCALE)
    for root,dirs,files in os.walk("./assets"):
        for target in files:
            if target.startswith(filename):
                template=cv2.imread(os.path.join(root,target),cv2.IMREAD_GRAYSCALE)
                res=cv2.matchTemplate(screenshot,template,cv2.TM_CCOEFF_NORMED)
                min_val,max_val,_,_=cv2.minMaxLoc(res)
                log("对比%s，可信度：%f"%(target,max_val),3)
                if max_val>trust_threshold:
                    log("匹配成功",3)
                    return True
                else:
                    log("匹配失败",3)
                    return False
    log("什么嘛，根本没有%s.png这张图！"%filename,1)
