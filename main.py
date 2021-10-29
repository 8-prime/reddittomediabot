from telegram.ext import Updater, CommandHandler
import logging
import urllib.request, json
import io




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

#Help for those who need it, not. LMAO
def help(update, context):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="Lappen")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def media(update, context):
    input_str = str(context.args[0]).lower()
    ijson = input_str + '.json'
    with urllib.request.urlopen(ijson) as response:
        data = json.loads(response.read().decode())
        img_url = data[0]['data']['children'][0]['data']['url']
        split = img_url.split('.')
        if split[-1] == 'png' or split[-1] == 'jpg':
            context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=img_url)
        elif split[-1] == 'mp4' or split[-1] == 'gif':
            context.bot.sendVideo(chat_id=update.effective_chat.id, video=img_url)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Was n das für n Dateityp bitte?!")
    # Delete message by using chat id: update.effective_chat.id and
    # message id: update.effective_message.id
    context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.effective_message.message_id)



def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=config['TOKEN']['Token'], use_context=True)
    dispatcher = updater.dispatcher
    
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler('media', media))
     #Start the Bot
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()
