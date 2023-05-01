from websockets.sync.client import connect
import json
import time
# import sys
# sys.stdout.write("Hello")
# sys.stdout.flush()
# while True:
    # print("Hello")
    # sys.stdin.flush()
    # lines = sys.stdin.readlines()
    # if (lines == None or len(lines) < 1):
        # time.sleep(1)
        # print(len(lines))
    #     continue
    # line = lines[0]
    # line = input()
    # print(line)
    # try:
        # data = json.loads(line)
    #     if (data['msg'] == "Ping!"):
    #         sys.stdout.write(json.dumps({
    #             'msg': "Pong!"
    #         }))
    #         sys.stdout.flush()
    # except SystemExit:
    #     raise
    # except:
    #     pass

with connect("ws://localhost:9910/ws/") as websocket:
    while True:
        try:
            data = json.loads(websocket.recv())
            if data["msg"] == "ping":
                print("Ping Recieved")
                websocket.send(json.dumps({
                    'msg': "Pong!"
                }))
            elif data["msg"] == "quit":
                exit(0)
            else:
                print(data)
        except SystemExit:
            raise
        except:
            pass
