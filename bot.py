import requests
import logging
import yaml

from bs4 import BeautifulSoup

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load config
with open("config.yaml", "r") as yamlfile:
    cfg = yaml.safe_load(yamlfile)

    token = cfg['botToken']
    wait = cfg['refreshTime']
    items = cfg['products']


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update, context):
    text = """I am a bot you have to run on your computer that checks regularly if items you're interested in are available.
My ultimate goal is do defeat scalpers.

You can control me using these commands:

/subscribe - Subscribe to user-defined items that are available
/subscribe_all - Subscribe to user-defined items regardless of availability
/unsubscribe - Unsubscribe from every subscriptions"""

    context.bot.send_message(chat_id = update.effective_chat.id, text = text)

def alertAvailableOnly(context):
    for item in items:
        name = item['name']
        url = item['url']

        job = context.job
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        price = soup.select('html body div#__next div div div main#pageContent div div div div div.productDetail div strong')[0].text.strip()
        availability = soup.select('html body div div div div main#pageContent div div div div div.productDetail div span span span.availabilityText div div')[0].text

        text = 'Name: %s\nPrice: %s\nStatus: %s\nUrl: %s' % (name, price, availability, url)

        if "Livré" in availability:
            context.bot.send_message(job.context, text = text)
        elif("Entre") in availability:
            context.bot.send_message(job.context, text = text)

def alert(context):
    for item in items:
        name = item['name']
        url = item['url']

        job = context.job
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        price = soup.select('html body div#__next div div div main#pageContent div div div div div.productDetail div strong')[0].text.strip()
        availability = soup.select('html body div div div div main#pageContent div div div div div.productDetail div span span span.availabilityText div div')[0].text

        text = 'Name: %s\nPrice: %s\nStatus: %s\nUrl: %s' % (name, price, availability, url)
        context.bot.send_message(job.context, text = text)

        

def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def subscribe(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_repeating(alertAvailableOnly, first = 0, interval = wait, context = chat_id, name = str(chat_id))

    text = 'Successfully subscribed to available items! I will check these every %s seconds' % wait if not job_removed else 'You were already subscribed to something. Your subscription was updated'
    update.message.reply_text(text)

def subscribeAll(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_repeating(alert, first = 0, interval = wait, context = chat_id, name = str(chat_id))

    text = 'Successfully subscribed to all items availability! I will check these every %s seconds' % wait if not job_removed else 'You were already subscribed to something. Your subscription was updated'
    update.message.reply_text(text)


def unsubscribe(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Successfully unsubscribed!' if job_removed else 'You are not subscribed. Type /subscribe or /subscribeAll to subscribe'
    update.message.reply_text(text)


def main():
    updater = Updater(token = token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    subscribe_handler = CommandHandler('subscribe', subscribe)
    subscribe_all_handler = CommandHandler('subscribe_all', subscribeAll)
    unsubscribe_handler = CommandHandler('unsubscribe', unsubscribe)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(subscribe_handler)
    dispatcher.add_handler(subscribe_all_handler)
    dispatcher.add_handler(unsubscribe_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()