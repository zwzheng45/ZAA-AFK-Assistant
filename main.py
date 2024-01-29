from automators.navigate import *
import automators
from log import *
import settings

print("\n------------------ZSA Starrail Assistant 0.1------------------\n")
# 初始化
if adb.get_stored_device_id() is None:
    input("初次见面！\n请确保adb已添加至环境变量（简单来说现在打开此电脑上的命令行输入`adb version`要能看到对应的adb版本号）\n请连接设备后并在安卓端允许USB调试以及模拟触控（部分手机）后按回车键继续...")
    adb.setup_new_device()
else:
    while(True):
        if not adb.check_device_connected(adb.device_id):
            c=input("检测不到上次使用的设备，请解锁设备并确保USB调试已开启并按回车重试；或输入r连接新设备：")
            if(c=='r' or c=='R'):
                adb.setup_new_device()
                break
            else:
                continue
        else:
            break
if not adb.start():
    print("请等待应用启动...")
    adb.capture_screen()
    if(match.cur_location(-5,True)==None):
        log("执行冷启动步骤",3)
        adb.capture_screen()
        x=None
        while(x==None):
            # 检查是否断线重连
            y=match.cur_location(4,True)
            if (y!=None and y!="loading"):
                break
            adb.capture_screen()
            # 检查是否加载到了开始界面
            x=match.match("./assets/login_page/server_page_start.png")
        adb.click(x[0],x[1])
        x=None
        while(x==None):
            adb.capture_screen()
            x=match.match("./assets/login_page/actual_start.png")
        adb.click(x[0],x[1])
        log("等待加载中...",2)
        x=None
        while(x==None):
            adb.capture_screen()
            y=match.cur_location(4,True)
            if (y!=None and y!="loading"):
                break
with open('config.json','r') as f:
    config=json.load(f)
    if config['print_logo']!='0':
        print("""                                     __,,,___
        ███████████████████▀    ▄█████████████            ╓███████
       ████▄▄▄▄▄▄▄▄▄Z╓████▀   ▄████▀▀S▄▄▄▄████           ,███▀A▀███
      ▀▀▀▀▀▀▀▀█████"▄████     ████▌╓██████████          ┌███Γ▄█ ████
             ████▀ ████▀      █████ ▀████▄,            ┌███▀▐███ ███▌
           ╓████"╓████"        ▀█████▄╙▀█████▄         ███▀╓█████ ███▌
          ▄████ █████            ╙▀█████▄"▀████▄      ███▌╒███▀███ ███▌
         ████▀,████▀                `╙█████`█████    ███by███ZZW███ ███▌
       ╓████"▄████▄,,,,,,,,,  ██▄▄▄▄▄▄█████▌▐████⌐  ███▌╒███████████ ███▌
      ████▀  ▀▀▀▀▀▀▀▀▀█████   ████▀▀▀▀▀▀▀▀"▄█████  ███▌┌▄▄▄▄▄▄▄▄▄▄▄▄▄ ███▄
    ,█████████████████████    █████████████████▀  ████████▀▀▀▀▀▀▀▀████████▄\t，启动！ 
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀     ╙▀▀▀▀▀▀▀▀▀▀▀▀""    '▀▀▀▀▀▀▀          ▀▀▀▀▀▀▀▀   \n""")
    else:
        print("\tZSA，启动！\n")

adb.capture_screen()


def menu():
    print("\n\033[1m功能选择：\033[0m\n\t1. 刷主线\n\t2. 刷塔\n\t3. 抽卡\n\t4. 设置\n\t\033[4me. 退出\033[0m")
    c=input("\t: ")
    if(c=='1'):
        try:
            automators.mainpage.navigate.main_mission()
        except KeyboardInterrupt:
            log("停止自动操作（用户中断）",1)
        return menu()
    elif(c=='2'):
        try:
            x=automators.tower.navigate.climb_tower()
            while(x!=-1):
                automators.tower.navigate.climb_tower()
        except KeyboardInterrupt:
            log("停止自动操作（用户中断）",1)
        return menu()
    elif(c=='3'):
        try:
            x=automators.infinite_pulls.navigate.re_pull()
            while(x==0):
                x=automators.infinite_pulls.navigate.re_pull()
        except KeyboardInterrupt:
            log("停止自动操作（用户中断）",1)
        return menu()
    elif(c=='4'):
        with open('config.json','r') as f:
            config=json.load(f)
            silence="关闭" if config['silence']=='1' else "启用"
            allow_push="启用" if config['push_notification']=='1' else "关闭"
            log_level="最低（仅错误）" if int(config['logging_level'])==1 else "中等（错误+警告）" if int(config['logging_level'])==2 else "最高（错误+警告+信息）"
        c=input("\033[1m设置\033[0m\n\t1. 提示音：\033[1m%s\033[0m\n\t2. 推送通知：\033[1m%s\033[0m\n\t3. 日志等级：\033[1m%s\033[0m\n\t\033[4mb. 返回\033[0m\n\t: "%(silence,allow_push,log_level))
        if(c=='1'):
            if(settings.toggle_silence()):
                print("设置变更：已\033[1m禁用\033[0m提示音")
            else:
                print("设置变更：已\033[1m启用\033[0m提示音")
        elif(c=='2'):
            if not (settings.toggle_notification()):
                print("设置变更：已\033[1m禁用\033[0m推送通知")
            else:
                print("设置变更：已\033[1m启用\033[0m推送通知")
        elif(c=='3'):
            new_level=input("日志等级：1. 最低（仅错误） 2. 中等（错误+警告） 3. 最高（错误+警告+信息），请输入新的日志打印等级: ")
            settings.set_logging_level(new_level)
    elif(c=='e' or c=='E'):
        print("拜拜～")
        log("用户退出",3)
        exit()
    else:
        print("没有这个选项，请重试...")
    return menu()



menu()
