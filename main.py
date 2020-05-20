import requests

#import time

request_type = ("sendMessage", "sendPoll", "sendDice",
                "sendContact", "sendVenue", "getUpdates", "forwardMessage")
# BOT_TOKEN = "1100044193:AAHVCn9H2lPOPPPRw0wcKMHb3sLc-gezoGo"+"/"
BOT_TOKEN = "YourTelegramBotToken"+"/"
THE_URL = "https://api.telegram.org/bot"

currentUpdateID = None
latest_msgID_forComputer = None

channel_id_list = [
    -1001439227003,
    -1001297789349
]


def test():

    # class test:

    #     def testtesttest(self):

    # print(time.time())

    # print(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(time.time())))

    REQUEST_METHOD_NAME = request_type[6]

    found_url = [
        "http://www.fyk.edu.my/read.php?id=1006",

    ]

    text_tobe_sent = "<b>Hello 你好</b>"

    PARAMETER = {
        # "chat_id": "@nkzlxs",
        # "chat_id": -1001293231152,

        # "phone_number": "0125215620",
        # "first_name": "何",
        # "last_name": "家珍校长",

        # "reply_to_message_id":119

        # "question": "1 + 1 = ?",
        # "options": [
        #     "2", "22", "222", "0"
        # ],
        # "is_anonymous": False,
        # "type": "regular",
        # "correct_option_id": 0

        # "latitude": 4.549099,
        # "longitude": 101.112350,
        # "title": "Shen Jai High School",
        # "address": "Shen Jai High School, 31350 Ipoh, Perak"

        # "voice":"AwACAgUAAx0CWLyKsgADS16VwHq9eeLGIf4SkNrDgFWju9RZAAIxAQAChE2xVBTNeqkiH-3dGAQ"
        # "parse_mode": "HTML",
        # "parse_mode": "MarkdownV2",
        # "text": text_tobe_sent
    }

    PARAMETER_FORWARD = {
        "chat_id": "@yejizhongxue",
        "from_chat_id": "-1001439227003",
        "message_id": 3
    }

    the_header = {"CONTENT-TYPE": "APPLICATION/JSON"}

    print(THE_URL+BOT_TOKEN+REQUEST_METHOD_NAME)

    # r = requests.post(url=THE_URL+BOT_TOKEN+REQUEST_METHOD_NAME)

    # print(r.json())

    b = requests.post(url=THE_URL+BOT_TOKEN+REQUEST_METHOD_NAME,
                      json=PARAMETER_FORWARD, headers=the_header)

    print(b.json())


def getUpdates(input_chat_id):
    response = requests.get(url=THE_URL+BOT_TOKEN + request_type[5])
    response_array = response.json()['result']
    global currentUpdateID
    if(response_array[len(response_array)-1]['channel_post']['chat']['id'] == input_chat_id):
        currentUpdateID = response_array[len(response_array)-1]['update_id']
    else:
        currentUpdateID = None


def getLatestMessageID(currentUpdateID=None):
    if(currentUpdateID == None):
        return None
    response = requests.get(url=THE_URL+BOT_TOKEN +
                            request_type[5]+"?offset="+str(currentUpdateID))
    # response_msg_ID = response.json()['result']['channel_post']['message_id']
    response_msg_ID = response.json()['result'][0]['channel_post']["message_id"]
    print(response_msg_ID)
    global latest_msgID_forComputer
    if(latest_msgID_forComputer is None):
        latest_msgID_forComputer = response_msg_ID
        return response_msg_ID
    elif(latest_msgID_forComputer == response_msg_ID):
        return None
    else:
        latest_msgID_forComputer = response_msg_ID
        return response_msg_ID


def forwardMessage(chat_id=None):
    the_message_id = getLatestMessageID(currentUpdateID)
    if (the_message_id is None):
        return None

    method_headers = {"CONTENT-TYPE": "APPLICATION/JSON"}
    method_parameters = {
        "chat_id": "@yejizhongxue",
        "from_chat_id": chat_id,
        "message_id": the_message_id
    }
    response = requests.post(url=THE_URL+BOT_TOKEN+request_type[6],
                             json=method_parameters, headers=method_headers)
    print(response.json())


if __name__ == "__main__":
    timer = 0
    choice = 0
    while True:
        if choice == len(channel_id_list):
            choice = 0
        if timer > 1000:
            getUpdates(channel_id_list[choice])
            forwardMessage(channel_id_list[choice])
            timer = 0
        timer += 1
        choice += 1
