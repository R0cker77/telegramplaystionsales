import telegram.ext
import logging
import pymongo
from telegram.ext import Updater
import datetime
import util

# logging, database initialization
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
client = pymongo.MongoClient("DATABASE URL")
db = client['Telegrambotps']
gamesales = db['psSales']

# puts every game in data into text , then sends it to a certain chat_id
def callback_minute(context: telegram.ext.CallbackContext):
    big_boy = ""
    for game in gamesales.find()[:65]:
        big_boy += f"[{game['name'].capitalize()} : from {game['OGprice']} to {game['AfterCut']}]({game['url']})\n\n"

    util.putting_list_to_xlxs(util.cleaning(gamesales.find()))
    context.bot.send_message(chat_id='-1001415795520', text=big_boy + "\n Full Games On sale down below\n", parse_mode='MarkdownV2')
    context.bot.send_document(chat_id='-1001415795520',document=open('gamesales.xlsx', 'rb'))

def main():
    updater = Updater("<BOT TOKEN>", use_context=True)
    dp = updater.dispatcher
    j = updater.job_queue
    job_minute = j.run_daily(callback_minute, time= datetime.time(hour =3, minute = 01))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
