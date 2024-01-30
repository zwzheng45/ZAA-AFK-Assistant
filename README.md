# ZAA-AFK-Assistant
一个适用于剑与远征的小脚本，由我自用的星铁脚本改写而来。   
边玩边写的一个练手项目，会随着我的游戏理解更新（   
## 功能
- adb操作，支持物理设备及模拟器
- 使用opencv模版匹配，不限制屏幕分辨率和长宽比
- 自动主线
- 自动爬塔
- 自动无限抽卡
- 战斗失败重试以及自动镜像站队
## 开始使用
克隆此仓库至本地   
```
git clone https://github.com/zwzheng45/ZAA-AFK-Assistant
cd ZAA-AFK-Assistant
```  
安装依赖（推荐使用conda或虚拟环境安装）
```
conda create -n zaa python=3.12
conda activate zaa
pip3 install -r requirements.txt
```
此外还需安装[Android 调试桥 (ADB)](https://source.android.google.cn/docs/setup/build/adb)   

启动脚本  
```
python3 main.py
```
