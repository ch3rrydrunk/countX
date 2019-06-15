#!/usr/bin/env
# By ch3rrydrunk <@ch3rrydrunk>
# Built with grace on python-telegram-bot
import logging as log
import os

from telegram import *
from telegram.ext import *
from telegram.ext import CommandHandler as CMH 
from telegram.ext import MessageHandler as MSH

from imageai.Detection import ObjectDetection
import os
import os.path

"""for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
    """

####### SETTINGS #######
#~~~~~~~ Logging ~~~~~~#
log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=log.INFO)
logger = log.getLogger(__name__)

#~~~~~~~ ImageAI ~~~~~~#
execution_path = os.getcwd()
"""
execution_path = "/Users/davidamb/telegram_bots/hackaton_vlabs"
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
"""

#~~~~~~~ Proxyfy ~~~~~~#
'''
# Be sure to add "request_kwargs=REQUEST_KWARGS" as Updater parameter if you wanna use proxy
REQUEST_KWARGS={
    'proxy_url': 'http://PROXY_HOST:PROXY_PORT/',
    # Optional, if you need authentication:
    'username': 'PROXY_USER',
    'password': 'PROXY_PASS',
}'''

######### LOGICS ########
#~~~~~~~ Commands ~~~~~~#
def start(update, context):
	update.message.reply_text("Начнем?\n"
								"Просто сфотографируй группу,"
								"чтобы быстро посчитать количество человек!\n"
								"Или выбери тип предметов, чтобы посчитать что-то другое!",
								reply_markup=markup)
	return MAIN


def help(update, context):
	update.message.reply_text("Серьезно? :)\n"
								"Просто присылай фото "
								"или набери '/start' для перезагрузки!",
								reply_markup=markup)
	return MAIN


#~~~~~~~~ Functions ~~~~~~~#
def rewind(update, context):
	return MAIN


def count_x(update, context):
	image_id = update.message.photo[-1]
	image = bot_core.bot.get_file(image_id)
	image.download('img.jpg')
	while True:
		if os.path.isfile("img.jpg") == True:
			break
	detector = ObjectDetection()
	detector.setModelTypeAsRetinaNet()
	detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
	detector.loadModel()
	detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "img.jpg"), output_image_path=os.path.join(execution_path , "imgnew.jpg"))
	file = open('imgnew.jpg', 'rb')
	i = 0
	for each in detections:
		if (each["name"] == "person"):
			i += 1
	update.message.reply_text("На фото - {} объектов\n".format(i),
								reply_markup=markup)
	update.message.reply_photo(file)
#	close(file)
	return MAIN


def to_contact(update, context):
	update.message.reply_text("Сделано с любовью командой RAW OCV\n"
								"Исходный код проекта доступен по ссылке:\n"
								"https://github.com/ch3rrydrunk/countX.git\n"
								"Спасибо, что вы с нами!",
								reply_markup=markup)
	return MAIN


def cancel(update, context):
	logger.info(str(update))
	user = update.message.from_user
	logger.info("User %s canceled the conversation.", user.first_name)
	update.message.reply_text('До свидания!',
								reply_markup=ReplyKeyboardRemove())

	return ConversationHandler.END



def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)


####### IGNITION #######
# To set API token set env variable (do "export BOT_API_TOKEN=your_token")
TOKEN = os.getenv("BOT_API_TOKEN")
bot_core = Updater("766731952:AAH6Xarc4gOOfWKI0kVYB8bVZs46_PdGVvE", use_context=True)
bot = bot_core.dispatcher

#======= LOGICS =======#

#˜˜˜˜˜˜  KEYMAP  ˜˜˜˜˜˜#
reply_keyboard = [['📲 Свяжись с нами! 📲']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

#˜˜˜˜˜˜  MANAGER ˜˜˜˜˜˜#
MAIN = range(1)

conv_handler = ConversationHandler(
	entry_points=[CMH('start', start)],

	states={
		MAIN:	[MSH(Filters.regex('^📲 Свяжись с нами! 📲$'), to_contact),
					MSH(Filters.photo, count_x)]
	},
	fallbacks=[CMH('cancel', cancel)]
	)
bot.add_handler(conv_handler)
#Extra Commands

#Errors
bot.add_error_handler(error)

#˜˜˜˜˜˜ Gogogo ˜˜˜˜˜˜#
bot_core.start_polling()
bot_core.idle()
