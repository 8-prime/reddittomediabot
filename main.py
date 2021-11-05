from telegram.ext import Updater, CommandHandler
import configparser
import traceback
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


def check_share(url):
    split = url.split('/')
    if 'share' in split[-1]:
        split = split[:len(split)-1]
        new_url = ""
        for s in split:
            new_url += s + '/'
        return new_url
    else:
        return url

def media(update, context):
    input_str = str(context.args[0]).lower()
    input_str = check_share(input_str)
    ijson = input_str + '.json'
    req = urllib.request.Request(ijson, headers = {
                'User-agent': 'reddittomedia'
                })

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data[0]['data']['children'][0]['data']['is_video']:
                img_url = data[0]['data']['children'][0]['data']['media']['reddit_video']['fallback_url']
                context.bot.sendVideo(chat_id=update.effective_chat.id, video=img_url)
            else:
                img_url = data[0]['data']['children'][0]['data']['url']

                split = img_url.split('.') # splits url to find filetype

                if split[-1] == 'png' or split[-1] == 'jpg':
                    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=img_url)
                    print("image\n" + img_url)
                else:        
                    context.bot.sendVideo(chat_id=update.effective_chat.id, video=img_url)              
                    print("video\n"+img_url)
    except Exception:
        print(traceback.print_exc())
        print("server overlaod")



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
