import json 
import requests
import time
import urllib
import random
from difflib import get_close_matches

TOKEN = "1301731488:AAG2ggR8juPW1i25c7Rhfg1vFYaxV-toOBM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
CHAT_IDS=[]
Jdata = json.load(open('data.json'))
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
def dictionary(word,chat):
    if word in Jdata:
        return(Jdata[word])
    elif word.title() in Jdata:
        return (Jdata(word.title()))
    elif word.upper() in Jdata:
        return (Jdata[word.upper()])
    elif len(get_close_matches(word,Jdata.keys())) > 0:
        word1=get_close_matches(word,Jdata.keys())[0]
        res="Do you mean "+word1+"??"
        send_message(res,chat)
        pass
    else:
        return None


pass
def call_dict(chat,texts):
    del texts[0]
    g_word=' '.join(texts)
    
    output=dictionary(g_word,chat)
    if(output == None):
        message="Sorry we couldn't find out your word in dictionary."
        send_message(message,chat)
    else:
        if type(output)== list:
            sent=""
            for item in output:
                sent=sent+item
            send_message(sent,chat)
        else:
            return(output,chat)

    	    

def get_chat_id(chat):
    if(chat not in CHAT_IDS):
        CHAT_IDS.append(chat)
def check_math(chat):
    if(chat not in CHAT_IDS):
        ask_math(chat)
        get_chat_id(chat)
def ask_math(chat):
    ask="C'mon i'm here to join hands with you:)"
    send_message(ask,chat)
    ask="type math<space>expression for your calculations"
    send_message(ask,chat)
    ask="type mean<space>word to find out Meaning!"
    send_message(ask,chat)
def do_maths(chat,key):
    try:
        content=key.encode()
        ans=content
        ans=str(eval(bytes(ans)))
        send_message(ans,chat)
    except Exception as e:
        reply="Please type\nMath<space>expression"
        send_message(reply,chat)
    
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    name = updates["result"][last_update]["message"]["chat"]["first_name"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
def send_this_message(text ,chat, name):
    try:
        hello=["hello","hi","hii","namaste","hiii","hloo","hlo","hey","heyy","helloo"]
        fine=["how are you?","hw r uh?"]
        mat=["math","maths","Math","Maths","math.","Math."]
        mean=["mean","meaning","means","defination"]
        texts=text.split(" ")
        if(text.lower() in hello):
            name='dear'
            reply=(random.choice(hello)).capitalize()+" "+name+"!!"
            send_message(reply, chat)
        elif(text.lower() in fine):
            reply="I'm doing well.How about you?"
            send_message(reply, chat)
        elif(texts[0] in mat):
            do_maths(chat,texts[1])
        elif(texts[0].lower() in mean):
            call_dict(chat,texts)
    except Exception as e:
        send_message("Please try again",chat)
    #else:
     #   reply="Sorry,I didn't get what you are looking for.. "
      #  send_message(reply,chat)
    check_math(chat) 
    
def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            #name = update["message"]["chat"]["first_name"]
            name='dear'
            send_message(text,1225086699)
            send_this_message(text, chat, name)
        except Exception as e:
            print(e)
            
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)
        
if __name__ == '__main__':
    main()
            
   