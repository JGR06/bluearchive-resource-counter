import imax
import telegram
import os.path

# python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html
# python-telegram-bot.readthedocs.io/en/stable/telegram.message.html#telegram.Message

def telegram_sendmessage(token, chatid, text):
	bot = telegram.Bot(token)
	ret = bot.sendMessage(chatid, text)
#	imax.print('ret.message_id: ', ret.message_id)
	return ret.message_id

def telegram_sendphoto(token, chatid, path):
	if not os.path.isfile(path):
		imax.print('file does not exist: ', path)
		return -1
	bot = telegram.Bot(token)
	ret = bot.send_photo(chatid, photo=open(path, 'rb'))
#	imax.print('send_photo ret.message_id: ', ret.message_id)
	return ret.message_id

def telegram_getmessage(token):
#	print('token: ', token)
	bot = telegram.Bot(token)
#	updates = bot.getUpdates()
#	# 메시지 내역 출력
#	for u in updates:
#		print(u.message)
	# 가장 최근 메시지 출력
	text = bot.getUpdates()[-1].message.text
	imax.print('lastest message text: ', text)

#import os
#print("Current working directory: {0}".format(os.getcwd()))
