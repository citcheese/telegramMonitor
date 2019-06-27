from telethon import TelegramClient,sync #need to keep sync in otherwise get await errors
import os
import pandas as pd
from datetime import datetime, timedelta
import time


"""
NOTES:
1. if get database locked error, that means havent closed session properly. Use client.log_out()
2. Go create app in Telegram to get below values
"""
api_hash = ""
api_id= ""
phonenumber = ""


client = TelegramClient(phonenumber, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phonenumber)
    client.sign_in(phonenumber, input('Enter the code: '))


def chatstocsv(channel_username,filestodl=[]):
    if os.path.isfile(os.path.join("Telegramchats",F"{channel_username}_chats.csv")):
        df1 = pd.read_csv(os.path.join("Telegramchats",F"{channel_username}_chats.csv"))
        minID = df1.message_id.max() #get ID of last message scraped
        fileexists = True
    else:
        fileexists=False
        minID = 0
    chats = client.get_messages(channel_username, min_id=minID, max_id=0)

    message_id = []
    message = []
    sender = []
    reply_to = []
    time = []
    mediatype =[]
    medianame =[]
    filestodl=[]
    mediaids=[]
    if len(chats):
        print(F"    {str(len(chats))} new messages found!")
        for chat in chats:
            message_id.append(chat.id)
            message.append(chat.message)
            sender.append(chat.from_id)
            reply_to.append(chat.reply_to_msg_id)
            time.append(chat.date)
            if chat.message:#check if any text in message
                if any(x in chat.message for x in filestodl):
                    filestodl.append(chat)
            if chat.media:
                MEDIATYPE = next(iter(chat.media.__dict__))
                item = getattr(chat.media,MEDIATYPE)
                if MEDIATYPE == "document":
                    #item = ast.literal_eval(item)
                    name = [x for x in item.attributes if hasattr(x, "file_name")] #check attribs for one that has filename in it
                    filename = name[0].file_name #then pull that one and get name
                else:
                    filename = ""
                medianame.append(filename)
                mediaids.append(str(item.id))
                mediatype.append(MEDIATYPE)
    else:
        print ("    No new messages found")

    data = {'message_id': message_id, 'message': message, 'sender_ID': sender, "media_type":mediatype,"media_name":medianame,"media_id":mediaids,'reply_to_msg_id': reply_to,
            'time': time}
    df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.items() ])) #lists are uneven lengths because not all items have media so do this
    df = df.sort_values("message_id")
    if fileexists:
        df.to_csv(os.path.join("Telegramchats",F"{channel_username}_chats.csv"),mode="a",header=False,index=False)

    else:
        df.to_csv(os.path.join("Telegramchats",F"{channel_username}_chats.csv"),index=False)

    return filestodl

def dltelegrammedia(chat):
    chat.download_media("TelegramFiles")

def monitorTelegram(channels=[],downloadfiles=False,kwstofindinmessagestodownload=[]):
    if not os.path.exists("Telegramchats"):
        os.makedirs("Telegramchats")
    if not os.path.exists("Telegramfiles"):
        os.makedirs("Telegramfiles")

    for channel in channels:
        if downloadfiles:
            if not os.path.exists(os.path.join("TelegramFiles", channel)):
                os.makedirs(os.path.join("TelegramFiles", channel))
        print(F"Starting scrape of {channel}")
        try:
           filestodl = chatstocsv(channel,filestodl=kwstofindinmessagestodownload)
           if downloadfiles:
               for y in filestodl:
                   print(F"Downloading file from message: {str(y.id)}")
                   dltelegrammedia(y)
        except Exception as e:
           print(e)

def getkws():
    import telegramkws
    import importlib
    importlib.reload(telegramkws) #reload moduel so can add new groups/kws to kw file without having to stop script
    channels = telegramkws.channels
    filestodl = telegramkws.kwstofindinmessagestodownload
    return channels,filestodl



def main():
    count = 0
    while 1:
        count += 1
        channels,filestodl = getkws()
        monitorTelegram(channels=channels,downloadfiles=False,kwstofindinmessagestodownload=filestodl) #if you don't want to DL files set to false

        print(F"Completed run number {str(count)} at {str(datetime.now()).split('.', 1)[0]}")
        # below code runs script every hour
        dt = datetime.now() + timedelta(hours=1)
        # dt = dt.replace(minute=10)
        while datetime.now() < dt:
            time.sleep(1)

if __name__ == '__main__':
    main()
