Quick and dirty script to monitor telegram channels, write chats to CSV and download files based on user parameters. Written using Python 3.7. Suggest using same to run.
Will only grab new messages/DLs when enable monitoring.
Settings inside script to change frequency of monitoring. Will send emails on completion of certain activities or if there is error. Look inside script for all the parameters you can change. Will eventually make more user friendly or maybe I won't, I dunno. 

You'll need to create Telegram application first to get keys. Edit telegramkws.py to specify channels usernames/ID you want to monitor for; what type of files you want to download and what keywords will trigger file download;
