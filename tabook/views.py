from time import sleep
from django.shortcuts import render
from telethon import TelegramClient

# Create your views here.
from .models import *
import logging
from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)

from auth.GoogleDrive import GoogleDrive
from auth.sheets import GoogleSheet

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


NAME, PHONE = range(2)
NAME_GROUP, PEROID, CLOCK_START, CLOCK_END, URL_GROUP = range(5)
token = "5564914229:AAEXcQ383pZZoUuf83a8PTsIoD_DHSbS3m8"
bot = Bot(token=token)


sheet = GoogleSheet()

services = GoogleDrive.get_google_drive_services()


reply_keyboards = {
    "reply_keyboard_user": [['🕌 حلقات التحفيظ', ], ['⁉️ الاستفسارات', '📞 الدعم']],
    "reply_keyboard_admin": [['🕌 حلقات التحفيظ', ], ['⁉️ الاستفسارات', '📞 الدعم'], ['🎛 لوحة التحكم']],
    "statistics": [['📌 المجموعات', ], ['رجوع']],
    "panel": [['📊 التقارير والاحصائيات', ], ['رجوع']],
    "cancel_process": [['إلغاء', ]],
    "back": [['رجوع']],

}

keyboards = {
    "users": ReplyKeyboardMarkup(reply_keyboards["reply_keyboard_user"], one_time_keyboard=False, resize_keyboard=True),
    "admins": ReplyKeyboardMarkup(reply_keyboards["reply_keyboard_admin"], one_time_keyboard=False, resize_keyboard=True),
    "cancel": ReplyKeyboardMarkup(reply_keyboards["cancel_process"], one_time_keyboard=False, resize_keyboard=True),
    "back": ReplyKeyboardMarkup(reply_keyboards["back"], one_time_keyboard=False, resize_keyboard=True),
    "panel": ReplyKeyboardMarkup(reply_keyboards["panel"], one_time_keyboard=False, resize_keyboard=True),

    "statistics": ReplyKeyboardMarkup(reply_keyboards["statistics"], one_time_keyboard=False, resize_keyboard=True),
}

texts = {
    "text_start": "🕌 تبوك لحلقات التحفيظ القراني 🕌",
    "text_start_paragraph": "<b>مرحبا بك صديقي في مبادرة تبوك لحلقات القران الكريم، للتسجيل في حلقات التحفيظ يرجى الإجابة على الأسئلة التالية: -</b>\n\n1- ما هو اسمك رباعي؟\n😊😊😊",
    "phone_text":  "يرجى إدخال رقم هاتفك مع بادئة الدولة كما يظهر في التنسيق التالي: -\n+96659843390\n\n😊😊😊",
    "thanks": "شكر لك",
    "text_session": "<b>اهلا وسهلا بك في حلقات التحفيظ، يمكنك اختيار حلقة التحفيظ المناسبة لك حسب وقتك، حيث تتوفر الأوقات التالية: -</b>\n\nيمكنك اقتراح وقت يناسبك صديقي عن طريق التواصل مع الدعم\n😊😊😊",
    "nothing_session": "لا يوجد حلقات تحفيظ في الوقت الحالي",
    "support_text": "للتواصل مع الدعم عبر الواتس اب من خلال  الرابط التالي: \nhttp://wa.me/966920024900",
    "statistics_text": "📊 التقارير والاحصائيات 📊",
    "add_group_text": "أدخل اسم المجموعة لو سمحت!",
    "group_name_text": "<b>ما هو موعد توقيت افتتاح الجلسة حسب الخيارات التالية: - </b>\nالفجر، الظهر، العصر، المغرب، العشاء\n\nأدخل الفترة المناسبة لك",
    "period_text": "تبدأ حلقة التحفيظ من الساعة كم؟",
    "group_clock_start_text":  "تنتهي حلقة التحفيظ الساعة كم؟",
    "group_clock_end_text": "أدخل رابط المجموعة لو سمحت: ",
    "group_url_text": "لقد تم حفظ المجموعة الجديدة بنجاح",
    "panel_text": "🧩 لوحة التحكم في البوت 🧩",
    "no_groups": "لا يوجد مجموعات حاليا",
    "queries_text": "📞 اذا كان لديك اي استفسارات يمكنك طرحها من خلال الرابط التالي: \n https://forms.gle/ABNyq3Yx61ceRYXi9",

}


photos = {
    "photo_start": 'https://iadsb.tmgrup.com.tr/861b7a/645/344/0/69/1026/616?u=https://idsb.tmgrup.com.tr/ar/2018/02/07/-20--1518012388088.jpg'
}


def dash(request):
    users = User.objects.all()
    return render(request, 'dashboard/dashboard.html', {'users': users})


def StoreUser(user, update, context):
    if user.telegram_user_name == None or user.telegram_first_name == None or user.telegram_last_name == None or user.telegram_is_bot == None:
        print('There is a None Value!?')
        if user.telegram_user_name == None:
            user.telegram_user_name = "None"
            print('UserName is a None value')
        elif user.telegram_first_name == None:
            user.telegram_first_name = "None"
            print('FirstName is a None value')
        elif user.telegram_last_name == None:
            user.telegram_last_name = "None"
            print('LastName is a None value')
        elif user.telegram_is_bot == None:
            user.telegram_is_bot = "None"
            print('LastName is a None value')
    else:
        print('There is no a None Value!')

    if not User.objects.select_for_update().filter(telegram_user_id=user.telegram_user_id).exists():
        User.objects.get_or_create(
            telegram_user_id=user.telegram_user_id,
            telegram_user_name=user.telegram_user_name,
            telegram_first_name=user.telegram_first_name,
            telegram_last_name=user.telegram_last_name,
            telegram_language=user.telegram_language,
            telegram_is_bot=user.telegram_is_bot)

        user = User.objects.get(telegram_user_id=user.telegram_user_id)

        return user


def getInformation(update: Update, context: CallbackContext):
    model = User(
        telegram_user_id=update.message.from_user.id,
        telegram_user_name=update.message.from_user.username,
        telegram_first_name=update.message.from_user.first_name,
        telegram_last_name=update.message.from_user.last_name,
        telegram_language=update.message.from_user.language_code,
        telegram_is_bot=update.message.from_user.is_bot,
    )

    return model

# User Scop


def user_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=texts["text_start"],
        parse_mode="HTML",
        reply_markup=keyboards["users"]
    )

# Admin Scop


def admin_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=texts["text_start"],
        parse_mode="HTML",
        reply_markup=keyboards["admins"]
    )

# Starting


def start(update: Update, context: CallbackContext):

    user = getting_user(update.message.from_user.id, update, context)

    if user:

        validate = is_registered(user, update, context)

        if validate:
            update.message.reply_photo(
                photo=photos["photo_start"],
                caption=texts["text_start_paragraph"],
                parse_mode="HTML",
            )
            return NAME
        else:
            if(user.is_admin):
                admin_start(update, context)
            else:
                user_start(update, context)


def is_registered(user, update, context):
    if(user.name == 'None' or user.phone_number == 'None'):
        return True
    else:
        return False


def getting_user(telegram_user_id, update, context):

    users = User.objects.all()

    print(users, User.objects.filter(telegram_user_id=telegram_user_id).exists())

    if users.count():
        if User.objects.filter(telegram_user_id=telegram_user_id).exists():
            user = User.objects.get(telegram_user_id=telegram_user_id)
            return user
        else:
            user_model = getInformation(update, context)
            user = StoreUser(user_model, update, context)
            return user
    else:
        user_model = getInformation(update, context)
        user = StoreUser(user_model, update, context)
        return user

# Save User Input Name
def name(update: Update, context: CallbackContext):
    user = getting_user(update.message.from_user.id, update, context)
    user.name = update.message.text
    user.save()
    bot.send_message(update.message.from_user.id, text=texts["phone_text"])
    return PHONE

def phone_number(update: Update, context: CallbackContext):
    user = getting_user(update.message.from_user.id, update, context)
    user.phone_number = update.message.text
    user.save()
    bot.send_message(update.message.from_user.id, text=texts["thanks"])
    if(user.is_admin):
        admin_start(update, context)
    else:
        user_start(update, context)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(text=texts["thanks"])
    start(update, context)
    return ConversationHandler.END

def panel(update: Update, context: CallbackContext):
    user = getting_user(update.message.from_user.id, update, context)

    if(user.is_admin):
        update.message.reply_text(
            text=texts["panel_text"], parse_mode="HTML", reply_markup=keyboards["panel"])
    else:
        update.message.reply_text(
            text="ليس لديك صلاحيات الادمن", parse_mode="HTML", reply_markup=keyboards["back"])


def addGroup(update: Update, context: CallbackContext):
    user = getting_user(update.message.from_user.id, update, context)

    validate = is_registered(user, update, context)

    if not validate:
        if(user.is_admin):
            Group.objects.get_or_create(
                telegram_group_title=update.message.chat.title)
            
            group = Group.objects.select_for_update().order_by('-id')[0]
            chat = bot.get_chat(update.message.chat.id)
            # group.period = update.message.text
            group.telegram_group_id = chat.id
            group.telegram_url = chat.invite_link
            group.telegram_chat_type = chat.type
            group.telegram_counts = chat.get_member_count()
            group.save()
            update.message.reply_text(text="لقد تم إضافة القروب في البوت بنجاح" )
            # return PEROID
        else:
            update.message.reply_text(text="هذا الأمر من صلاحيات الادمن")
    else:
        update.message.reply_text(
            text="يرجى تسجيل اسمك ورقمك في هذا البوت @bottabook_bot")


# def Period(update: Update, context: CallbackContext):
#     group = Group.objects.select_for_update().order_by('-id')[0]
#     chat = bot.get_chat(update.message.chat.id)
#     group.period = update.message.text
#     group.telegram_group_id = chat.id
#     group.telegram_url = chat.invite_link
#     group.telegram_chat_type = chat.type
#     group.telegram_counts = chat.get_member_count()
#     group.save()
#     update.message.reply_text(
#         text=texts["period_text"], parse_mode="HTML", reply_markup=keyboards["cancel"])
#     return CLOCK_START


# def GroupClockStart(update: Update, context: CallbackContext):
#     group = Group.objects.select_for_update().order_by('-id')[0]
#     group.start = update.message.text
#     group.save()
#     update.message.reply_text(
#         text=texts["group_clock_start_text"], reply_markup=keyboards["cancel"])
#     return CLOCK_END


# def GroupClockEnd(update: Update, context: CallbackContext):
#     group = Group.objects.select_for_update().order_by('-id')[0]
#     group.end = update.message.text
#     group.save()
#     update.message.reply_text(
#         text=texts["thanks"], parse_mode="HTML")
#     return ConversationHandler.END


def support(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=texts["support_text"], parse_mode="HTML", reply_markup=keyboards["back"])


def statistics(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=texts["statistics_text"], parse_mode="HTML", reply_markup=keyboards["statistics"])


def queries(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=texts["queries_text"], parse_mode="HTML", reply_markup=keyboards["back"])
   
def rooms(update: Update, context: CallbackContext):

    groups = Group.objects.all()

    if groups.count():
        keyboard = []
        x = 1
        for group in groups:

            if (group.telegram_url and group.telegram_group_title):
                # name = "حلقة " + str(group.period) + " " + \
                #     str(group.start) + " - " + str(group.end)
                keyboard.append(
                    [InlineKeyboardButton(str(group.telegram_group_title), url=str(group.telegram_url))])
                
                x = x + 1

        bot.send_message(update.message.from_user.id,
                         text="حلقات التحفيظ القراني", reply_markup=keyboards["back"])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            text=texts["text_session"], parse_mode="HTML", reply_markup=reply_markup)
    else:
        update.message.reply_text(
            text=texts["nothing_session"], parse_mode="HTML", reply_markup=keyboards["back"])


def groups(update: Update, context: CallbackContext):

    groups = Group.objects.all()

    x = 1

    if groups.count():
        for group in groups:
            if(group.telegram_url and group.telegram_group_title and group.telegram_counts):
                # text = "<b>🕌 المجموعة رقم </b>" + "<b>(" + str(x) + ")\n\n🔰 اسم المجموعة: </b>" + group.telegram_group_title + "\n\n🔰 <b>عدد الأعضاء: </b>" + str(group.telegram_counts) + "\n\n<b>🔰 الفترة: </b>" + group.period + \
                #     "\n\n<b>🔰 ساعة البداية: </b>" + str(group.start) + "\n\n<b>🔰 ساعة النهاية: </b>" + str(
                #     group.end) + "\n\n🔰 <b>رابط المجموعة: </b>\n" + group.telegram_url + "\n\n*******"

                text = "<b>🕌 المجموعة رقم </b>" + "<b>(" + str(x) + ")\n\n🔰 اسم المجموعة: </b>" + group.telegram_group_title + "\n\n🔰 <b>عدد الأعضاء: </b>" + str(group.telegram_counts) + "\n\n🔰 <b>رابط المجموعة: </b>\n" + group.telegram_url + "\n\n*******"

                x = x + 1
                update.message.reply_text(
                    text=text, parse_mode="HTML", reply_markup=keyboards["back"])
    else:
        update.message.reply_text(
            text=texts["no_groups"], parse_mode="HTML", reply_markup=keyboards["back"])


def new_user(update: Update, context: CallbackContext):
    print("Joined User")
    sheet = GoogleSheet()
    chat = update.message.chat
    telegram_user_id = update.message.from_user.id
    group = Group.objects.get(telegram_group_id=chat.id)
    user = User.objects.get(telegram_user_id=telegram_user_id)
    group.user_id = user
    group.status = True
    group.save()

    print(user, user.name, user.phone_number)

    Sheet.objects.get_or_create(telegram_user_id=telegram_user_id)

    sheet_object = Sheet.objects.get(telegram_user_id=telegram_user_id)

    sheet_object.telegram_user_id = telegram_user_id
    sheet_object.name = user.name
    sheet_object.phone_number = user.phone_number

    if chat.title == "رتل | حلقة الظهر من ١:٠٠م إلى ٢:٠٠م":
        sheet_object.group_one = "مشارك"

    if chat.title == "رتل | حلقة العصر من ٤:٣٠م إلى ٥:٣٠ م":
        sheet_object.group_two = "مشارك"

    if chat.title == "رتل | حلقة المساء من ٩:٣٠م إلى ١٠:٣٠م":
        sheet_object.group_three = "مشارك"

    sheet_object.save()

    sheet_object = Sheet.objects.all()

    #Saving in sheets
    sheet = sheet.get_sheet()

    last_col = sheet.col_values(1)[-1]

    last_col = 2

    for user in sheet_object:

        insertRow = [
            str(last_col),
            str(user.telegram_user_id),
            str(user.name),
            str(user.phone_number),
            str(user.group_one),
            str(user.group_two),
            str(user.group_three),
        ]

        range_row = 'A' + str(last_col) + ':G' + str(last_col)

        sheet.update(range_row,  [insertRow])

        last_col = int(last_col) + 1


def left_user(update: Update, context: CallbackContext):
    print("LeftUser User")
    sheet = GoogleSheet()
    chat = update.message.chat
    telegram_user_id = update.message.from_user.id
    group = Group.objects.get(telegram_group_id=chat.id)
    user = User.objects.get(telegram_user_id=telegram_user_id)
    group.status = False
    group.save()

    sheet_object = Sheet.objects.get(telegram_user_id=telegram_user_id)

    sheet_object.telegram_user_id = telegram_user_id
    sheet_object.name = user.name
    sheet_object.phone_number = user.phone_number

    if chat.title == "رتل | حلقة الظهر من ١:٠٠م إلى ٢:٠٠م":
        sheet_object.group_one = "مغادر"

    if chat.title == "رتل | حلقة العصر من ٤:٣٠م إلى ٥:٣٠ م":
        sheet_object.group_two = "مغادر"

    if chat.title == "رتل | حلقة المساء من ٩:٣٠م إلى ١٠:٣٠م":
        sheet_object.group_three = "مغادر"

    sheet_object.save()

    sheet_object = Sheet.objects.all()

    #Saving in sheets

    sheet = sheet.get_sheet()

    last_col = sheet.col_values(1)[-1]

    last_col = 2

    for user in sheet_object:

        insertRow = [
            str(last_col),
            str(user.telegram_user_id),
            str(user.name),
            str(user.phone_number),
            str(user.group_one),
            str(user.group_two),
            str(user.group_three),
        ]

        range_row = 'A' + str(last_col) + ':G' + str(last_col)

        sheet.update(range_row,  [insertRow])

        last_col = int(last_col) + 1
