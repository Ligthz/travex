import requests

class TelegramBot:
    def __init__(self,TOKEN):
        self.url = "https://api.telegram.org/bot"+TOKEN
        self.id = "-475752058"

    def read(self):
        msgs = requests.get(self.url+"/getUpdates")
        msgs = msgs.text
        print(msgs)

    def send(self,msg):
        send_buff = self.url+"/sendMessage"
        send_buff += "?text="+msg
        send_buff += "&chat_id="+str(self.id)
        msgs = requests.get(send_buff)
        msgs = msgs.text

