import asyncio
import requests
from telethon import TelegramClient, events
from keep_alive import keep_alive

# ====== بيانات Telethon ======
api_id = 23744337
api_hash = 'a2f8a95102ca063ba2f9c822897d2b18'
session = 'forward_multi_session2'

# قنوات المصدر
source_channels = ['ajanews', 'iraninarabic']

# قناتك الهدف
target_channel = 'newsorbitt'

# بيانات البوت للإشعار
bot_token = '7375573205:AAHPbl7tu5tH1eJJdIzw9fbZlqOrzXoTMW4'
notify_chat_id = 6462833025

# إنشاء الكلاينت
client = TelegramClient(session, api_id, api_hash)

# إرسال إشعار
def send_bot_notification(text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": notify_chat_id, "text": text}
    try:
        requests.post(url, data=data)
        print("📢 تم إرسال إشعار عبر البوت.")
    except Exception as e:
        print(f"❌ فشل إرسال الإشعار: {e}")

# استقبال الرسائل
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    msg = event.message
    source = f"@{event.chat.username}" if event.chat and event.chat.username else event.chat.title
    try:
        if msg.text and not msg.media:
            await client.send_message(target_channel, msg.text)
        elif msg.media:
            await client.send_file(target_channel, msg.media, caption=msg.text)
        else:
            print("⚠️ تم تجاهل رسالة غير مدعومة.")
            return
        print(f"✅ نُشرت رسالة من {source}")
        send_bot_notification(f"📰 تم نشر خبر جديد من {source} على @{target_channel}")
    except Exception as e:
        err = f"❌ خطأ أثناء النشر من {source}: {e}"
        print(err)
        send_bot_notification(err)

# بدء التشغيل
async def main():
    await client.start()
    print("🚀 جاري مراقبة القنوات: ajanews + iraninarabic")
    await client.run_until_disconnected()

# تشغيل فعلي
if __name__ == '__main__':
    keep_alive()
    asyncio.run(main())
