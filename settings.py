import json

def toggle_silence():
    with open('config.json','r') as f:
        config=json.load(f)
        if config['silence']=='1':
            config['silence']='0'
            silence=False
        else:
            config['silence']='1'
            silence=True
    with open('config.json','w') as f:
        json.dump(config,f)
    return silence

def toggle_notification():
    with open('config.json','r') as f:
        config=json.load(f)
        if config['push_notification']=='1':
            config['push_notification']='0'
            push_noti=False
        else:
            config['push_notification']='1'
            push_noti=True
    with open('config.json','w') as f:
        json.dump(config,f)
    return push_noti

def set_logging_level(new_level):
    with open('config.json','r') as f:
        config=json.load(f)
    config['logging_level']=new_level
    with open('config.json','w') as f:
        json.dump(config,f)
