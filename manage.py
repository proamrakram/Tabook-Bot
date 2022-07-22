#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
# from controllerTabook import Bot

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


def main():
    # bot = Bot()

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TelegramBot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


    # start_conversation = ConversationHandler(

    #     entry_points=[CommandHandler('start', bot.start)],

    #     states={
    #         NAME: [MessageHandler(Filters.text & ~ Filters.command, bot.name)],
    #         PHONE: [MessageHandler(Filters.text & ~ Filters.command, bot.phone_number)],
    #     },

    #     fallbacks=[MessageHandler(Filters.regex('إلغاء'), bot.cancel)],
    # )

    # # adding_group_conversation = ConversationHandler(

    # #     entry_points=[
    # #         MessageHandler(Filters.regex('📌 إضافة مجموعة جديدة'), bot.addGroup),
    # #         CommandHandler('addGroup', bot.addGroup)
    # #         ],
    # #     states={
    # #         NAME_GROUP: [MessageHandler(Filters.text & ~ Filters.command, bot.GroupName)],
    # #         PEROID: [MessageHandler(Filters.text & ~ Filters.command, bot.Period)],
    # #         CLOCK_START: [MessageHandler(Filters.text & ~ Filters.command, bot.GroupClockStart)],
    # #         CLOCK_END: [MessageHandler(Filters.text & ~ Filters.command, bot.GroupClockEnd)],
    # #         URL_GROUP: [MessageHandler(Filters.text & ~ Filters.command, bot.GroupUrl)],
    # #     },
    # #     fallbacks=[MessageHandler(Filters.regex('إلغاء'), bot.cancel)],
    # # )

    # dispatcher.add_handler(start_conversation)
    # # dispatcher.add_handler(adding_group_conversation)

    # #Admin Panel
    # dispatcher.add_handler(MessageHandler(Filters.regex('🎛 لوحة التحكم'), bot.panel))
    # dispatcher.add_handler(MessageHandler(Filters.regex('رجوع'), bot.start))


    # dispatcher.add_handler(MessageHandler(Filters.regex('📞 الدعم'), bot.support))
    # dispatcher.add_handler(MessageHandler(Filters.regex('📊 التقارير والاحصائيات'), bot.statistics))

    # dispatcher.add_handler(MessageHandler(Filters.regex('⁉️ الاستفسارات'), bot.queries))

    # dispatcher.add_handler(MessageHandler(Filters.regex('🕌 حلقات التحفيظ'), bot.rooms))
    # dispatcher.add_handler(MessageHandler(Filters.regex('📌 المجموعات'), bot.groups))
    # dispatcher.add_handler(CommandHandler('addGroup', bot.addGroup))    

    # dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, bot.new_user))
    # dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, bot.left_user))


    # ################################################################################
    # InlineKeyboard = callbackqueryhandler.CallbackQueryHandler(bot.Options)
    # dispatcher.add_handler(InlineKeyboard)    
    # ################################################################################
    # print("Started The bot")
    # updater.start_polling()
    
    # updater.idle()


if __name__ == '__main__':
    main()
