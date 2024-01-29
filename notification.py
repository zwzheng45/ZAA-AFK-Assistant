import json
import pygame
import sys
import os
from time import sleep

with open('config.json','r') as f:
    config=json.load(f)
    silence=True if config['silence']=='1' else False
    allow_push=True if config['push_notification']=='1' else False


def failure_warning():
    global silence,allow_push
    if allow_push:
        if (sys.platform=="darwin"):
            os.system('osascript -e \'display notification "调整队伍后回车返回..." with title "练度过低，打不过..." subtitle ""\'')
    if not silence:
        pygame.mixer.init()
        sound=pygame.mixer.Sound("assets/sound/warning.wav")
        sound.play()
        sleep(2.3)

def push_notification(title='',subtitle='',content=''):
    global silence,allow_push
    if allow_push:
        if (sys.platform=="darwin"):
            os.system('osascript -e \'display notification "%s" with title "%s" subtitle "%s"\''%(content,title,subtitle))

def play_warning_sound():
    if not silence:
        pygame.mixer.init()
        sound=pygame.mixer.Sound("assets/sound/warning.wav")
        sound.play()
        sleep(2.3)