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


def xstr(s):
    if s is None:
        return ''
    return str(s)

def chatstocsv(channel_username,filestodl=[]):
    if ":::?:::" in channel_username:
        channel_IDusername,channel_username = channel_username.split(":::?:::")
        channel_IDusername = int(channel_IDusername)
    else:
        channel_IDusername = channel_username
    if os.path.isfile(os.path.join("Telegramchats",F"{channel_username}_chats.csv")):
        df1 = pd.read_csv(os.path.join("Telegramchats",F"{channel_username}_chats.csv"))
        minID = df1.message_id.max() #get ID of last message scraped
        fileexists = True
    else:
        fileexists=False
        minID = 0
    chats = client.get_messages(channel_IDusername, min_id=minID, max_id=0)
    sender_username=[]
    sender_name=[]
    sender_phone=[]
    isbot =[]
    message_id = []
    message = []
    sender = []
    reply_to = []
    time = []
    channelid=[]
    channelname =[]
    mediatype =[]
    medianame =[]
    filestodownload=[]
    mediaids=[]
    if len(chats):
        print(F"    {str(len(chats))} new messages found!")
        for chat in chats:
            message_id.append(chat.id)
            message.append(str(chat.message))
            sender.append(chat.from_id)
            reply_to.append(chat.reply_to_msg_id)
            time.append(chat.date)
            try:
                sender_username.append(str(chat.sender.username))
                sendername = F"{xstr(chat.sender.first_name)} {xstr(chat.sender.last_name)}" #convert 'none' to empty string
                sender_name.append(sendername)
                sender_phone.append(xstr(chat.sender.phone))
                isbot.append(str(chat.sender.bot))
            except Exception as e: #placeholder til figure out how to check if thing is chnnael or chat
                pass
            channelid.append(str(chat.to_id.channel_id))
            channelname.append(str(chat._chat.title))
            if chat.media:
                MEDIATYPE = next(iter(chat.media.__dict__))
                item = getattr(chat.media,MEDIATYPE)
                if MEDIATYPE == "document":
                    #item = ast.literal_eval(item)
                    name = [x for x in item.attributes if hasattr(x, "file_name")] #check attribs for one that has filename in it
                    if name:
                        filename = name[0].file_name #then pull that one and get name
                    else:
                        filename = ""
                else:
                    filename = ""
                medianame.append(filename)
                mediaids.append(str(item.id))
                mediatype.append(MEDIATYPE)
            if chat.message:#check if any text in message on per channel basis
                if channel_username in filestodl:
                    if any(x.lower() in chat.message.lower() for x in filestodl[channel_username]):
                        filestodownload.append((chat,filename))

        data = {"channel_name": channelname, "channel_ID": channelid, 'message_id': message_id, 'message': message,
                'sender_ID': sender, "sender_username": sender_username, "sender_name": sender_name,
                "sender_phone": sender_phone, "media_type": mediatype, "media_name": medianame, "media_id": mediaids,
                'reply_to_msg_id': reply_to,
                'time': time}
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in
                                data.items()]))  # lists are uneven lengths because not all items have media so do this
        df = df.sort_values("message_id")
        if fileexists:
            df.to_csv(os.path.join("Telegramchats", F"{channel_username}_chats.csv"), mode="a", header=False,
                      index=False)
            print ("    Updated CSV")
        else:
            df.to_csv(os.path.join("Telegramchats", F"{channel_username}_chats.csv"), index=False)
            print("    Created CSV")
    else:
        print ("    No new messages found")

    return filestodownload


def monitorTelegram(channels=[],downloadfiles=False,kwstofindinmessagestodownload=[]):
    if not os.path.exists("Telegramchats"):
        os.makedirs("Telegramchats")
    if not os.path.exists("TelegramFiles"):
        os.makedirs("TelegramFiles")

    for channel in channels:
        if downloadfiles:
            if not os.path.exists(os.path.join("TelegramFiles", channel)):
                os.makedirs(os.path.join("TelegramFiles", channel))
        print(F"Starting scrape of {channel}")
        try:
           filestodl = chatstocsv(channel,filestodl=kwstofindinmessagestodownload)
           if downloadfiles:
               for y in filestodl:
                   chat,filename =y
                   if filename:
                       filename1 = filename
                   else:
                       filename1 = str(chat.id)
                   print(F"Downloading file from message: {str(filename1)}")
                   chat.download_media(os.path.join("TelegramFiles",channel))
        except Exception as e:
           print(e)

def getkws():
    import telegramkws
    import importlib
    importlib.reload(telegramkws) #reload moduel so can add new groups/kws to kw file without having to stop script
    channels = telegramkws.channels
    filestodl = telegramkws.kwstofindinmessagestodownload
    return channels,filestodl



def main(alertonerror=False):
    count = 0
    while 1:
        count += 1
        channels,filestodl = getkws()
        try:
            monitorTelegram(channels=channels,downloadfiles=True,kwstofindinmessagestodownload=filestodl) #if you don't want to DL files set to false
            print(F"Completed run number {str(count)} at {str(datetime.now()).split('.', 1)[0]}")

        except Exception as e:
            fullError = traceback.format_exc()
            if alertonerror:
                  EmailAlert.Py3send_email(F"Telegram: {str(e)}",str(fullError),str(fullError))
            else:
                  print(str(fullerror)
        # below code runs script every hour
        dt = datetime.now() + timedelta(hours=1)
        # dt = dt.replace(minute=10)
        while datetime.now() < dt:
            time.sleep(1)

if __name__ == '__main__':
    main(alertonerror=True)
