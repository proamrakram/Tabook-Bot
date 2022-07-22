from time import sleep
from telegram import Update
from telegram.ext import CallbackContext
from telethon import TelegramClient
from auth.GoogleDrive import GoogleDrive
from auth.sheets import GoogleSheet

sheet = GoogleSheet()
services = GoogleDrive.get_google_drive_services()

import logging

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    callbackqueryhandler,
)

token = "5564914229:AAEXcQ383pZZoUuf83a8PTsIoD_DHSbS3m8"
updater = Updater(token=token)
dispatcher = updater.dispatcher
    
NAME, PHONE = range(2)
NAME_GROUP, PEROID, CLOCK_START, CLOCK_END, URL_GROUP = range(5)



class Bot:
    def __init__(self):
        pass
    def controller(self):
        from tabook import views
        bot = views
        return bot
    def start(self,update: Update, context: CallbackContext):
        print("start")
        views = self.controller()
        return views.start(update, context)
    def test(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.test(update, context)
    def name(self,update: Update, context: CallbackContext):
        views = self.controller()
        if(update.message.text == "إلغاء"):
            return views.cancel(update, context)
        return views.name(update, context)
    def phone_number(self,update: Update, context: CallbackContext):
        views = self.controller()
        if(update.message.text == "إلغاء"):
            return views.cancel(update, context)
        return views.phone_number(update, context)
    def cancel(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.cancel(update, context)
    def panel(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.panel(update, context)
    def Options(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.Options(update, context)
    def addGroup(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.addGroup(update, context)
    def GroupName(self,update: Update, context: CallbackContext):
        views = self.controller()
        if(update.message.text == "إلغاء"):
            return views.cancel(update, context)
        return views.GroupName(update, context)
    def Period(self,update: Update, context: CallbackContext):
        views = self.controller()
        if(update.message.text == "إلغاء"):
            return views.cancel(update, context)
        return views.Period(update, context)  
    def GroupClockStart(self,update: Update, context: CallbackContext):
        views = self.controller()
        if(update.message.text == "إلغاء"):
            return views.cancel(update, context)
        return views.GroupClockStart(update, context)
    def GroupClockEnd(self,update: Update, context: CallbackContext):
        views = self.controller()
        if(update.message.text == "إلغاء"):
            return views.cancel(update, context)
        return views.GroupClockEnd(update, context)    
    def GroupUrl(self,update: Update, context: CallbackContext):
        views = self.controller()
        if(update.message.text == "إلغاء"):
            return views.cancel(update, context)
        return views.GroupUrl(update, context)
    def support(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.support(update, context)
    def statistics(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.statistics(update, context)
    def queries(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.queries(update, context)
    def rooms(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.rooms(update, context)
    def groups(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.groups(update, context)
    def new_user(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.new_user(update, context)
    def left_user(self,update: Update, context: CallbackContext):
        views = self.controller()
        return views.left_user(update, context)








def main():
    bot = Bot()


    start_conversation = ConversationHandler(

        entry_points=[CommandHandler('start', bot.start)],

        states={
            NAME: [MessageHandler(Filters.text & ~ Filters.command, bot.name)],
            PHONE: [MessageHandler(Filters.text & ~ Filters.command, bot.phone_number)],
        },

        fallbacks=[MessageHandler(Filters.regex('إلغاء'), bot.cancel)],
    )

    # adding_group_conversation = ConversationHandler(

    #     entry_points=[
    #         MessageHandler(Filters.regex('📌 إضافة مجموعة جديدة'), bot.addGroup),
    #         CommandHandler('addGroup', bot.addGroup)
    #         ],
    #     states={
    #         NAME_GROUP: [MessageHandler(Filters.text & ~ Filters.command, bot.GroupName)],
    #         PEROID: [MessageHandler(Filters.text & ~ Filters.command, bot.Period)],
    #         CLOCK_START: [MessageHandler(Filters.text & ~ Filters.command, bot.GroupClockStart)],
    #         CLOCK_END: [MessageHandler(Filters.text & ~ Filters.command, bot.GroupClockEnd)],
    #         URL_GROUP: [MessageHandler(Filters.text & ~ Filters.command, bot.GroupUrl)],
    #     },
    #     fallbacks=[MessageHandler(Filters.regex('إلغاء'), bot.cancel)],
    # )


    dispatcher.add_handler(start_conversation)
    # dispatcher.add_handler(adding_group_conversation)

    #Admin Panel
    dispatcher.add_handler(MessageHandler(Filters.regex('🎛 لوحة التحكم'), bot.panel))
    dispatcher.add_handler(MessageHandler(Filters.regex('رجوع'), bot.start))


    dispatcher.add_handler(MessageHandler(Filters.regex('📞 الدعم'), bot.support))
    dispatcher.add_handler(MessageHandler(Filters.regex('📊 التقارير والاحصائيات'), bot.statistics))

    dispatcher.add_handler(MessageHandler(Filters.regex('⁉️ الاستفسارات'), bot.queries))

    dispatcher.add_handler(MessageHandler(Filters.regex('🕌 حلقات التحفيظ'), bot.rooms))
    dispatcher.add_handler(MessageHandler(Filters.regex('📌 المجموعات'), bot.groups))
    dispatcher.add_handler(CommandHandler('addGroup', bot.addGroup))    

    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, bot.new_user))
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, bot.left_user))


    ################################################################################
    InlineKeyboard = callbackqueryhandler.CallbackQueryHandler(bot.Options)
    dispatcher.add_handler(InlineKeyboard)    
    ################################################################################
    print("Started The bot")
    updater.start_polling()
    
    updater.idle()

if __name__ == '__main__':
    main()
