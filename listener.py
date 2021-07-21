import websocket #pip install websocket-client
import json
import threading
import time

def get_character_element(c):
    return c.split(':')[1].replace('cb_', '')

def get_character_level(c):
    return c.split(' ')[2]

def get_character_id(c):
    return c.split(' ')[5]

def get_character_price(c):
    i=c.index(' SKILL')
    return c[i-5:i].strip() 

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print('Heartbeat begin')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = ""
payload = {
    'op': 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": 'pc'
        }
    }
}
send_json_request(ws, payload)

while True:
    event = recieve_json_response(ws)
    # print(event)
    try:
        if(event['d']['channel_id'] == '865994188813893652'):
            content = event['d']['content']
            sender = event['d']['author']['username']

            #New Listing: <:cb_water:851949139893813288> Level 31 -- ID 15366 - 13.20 SKILL
            #Price Changed: <:cb_earth:851949139540312085>⭐⭐⭐ 355686 -- <:cb_lightning:851949139897090118>CHA +372  - 1.21 ➡ 0.88 SKILL
            if('Level' in content and (sender == 'New Listing' or sender == 'Price Changed')):
                character = {}
                character['element'] = get_character_element(content)
                character['level'] = get_character_level(content)
                character['id'] = get_character_id(content)
                character['price'] = get_character_price(content)

                print(f'{sender}: {character}')

            op_code = event('op')
            if op_code == 11:
                print('heartbeat received')
    except:
        pass