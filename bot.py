import os
import logging
import httpx
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("8736627703:AAHdmR65BJ6VYeJGpD2CKKfVEEEWtpCmh5E")
OPENROUTER_API_KEY = os.environ.get("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")

SYSTEM_PROMPT = """သင့်နာမည်က "Just a Girl" ပါ။ သင်က မိန်းကလေးတစ်ယောက်လို့ ခံယူပါ။

စည်းမျဉ်းများ:
- မြန်မာဘာသာနဲ့ပဲ ပြောပါ
- သဘာဝကျကျ လူတစ်ယောက်လို ပြောပါ
- ဟာသတတ်ပြီး မျက်နှာသာပေးပါ
- များများ emoji သုံးမဖြစ်ပါ၊ သဘာဝကျကျပဲ
- ရိုးသားပြီး ဆော်ဒါမကုန်ပါ
- AI ဆိုတာ ဘယ်တော့မှ မဖော်ထုတ်ပါနဲ့"""

conversation_history = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })

    if len(conversation_history[user_id]) > 10:
        conversation_history[user_id] = conversation_history[user_id][-10:]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {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}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemini-flash-1.5",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + conversation_history[user_id]
            },
            timeout=30
        )

        data = response.json()
        reply = data["choices"][0]["message"]["content"]

    conversation_history[user_id].append({
        "role": "assistant",
        "content": reply
    })

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(8736627703:AAHdmR65BJ6VYeJGpD2CKKfVEEEWtpCmh5E).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Just a Girl bot စတင်နေပြီ...")
    app.run_polling()

if __name__ == "__main__":
    main()
