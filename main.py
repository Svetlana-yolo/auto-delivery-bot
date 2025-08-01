import os
import json
from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.types import FSInputFile
from dotenv import load_dotenv
import uvicorn

# === 🟦 БЛОК 1: НАСТРОЙКА ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
app = FastAPI()


# === 🟦 БЛОК 2: ОБРАБОТКА ВЕБХУКА ОТ ЮКАССА ===
@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    print(json.dumps(data, indent=2))  # Добавим лог


    # Проверка на успешную оплату
    if data.get("event") == "payment.succeeded":
        label = data.get("object", {}).get("metadata", {}).get("label")
        telegram_id = data.get("object", {}).get("metadata", {}).get("telegram_id")

        # Подтверждаем, что всё нужное получено
        if label and telegram_id:
            await send_file_by_label(telegram_id, label)

    return {"status": "ok"}


# === 🟦 БЛОК 3: ВЫДАЧА ФАЙЛА ПО МЕТКЕ ===
async def send_file_by_label(telegram_id, label):
    if label == "guide_law":
        file = FSInputFile("files/guide_law.pdf")
        caption = "📗 *Гайд — Криптовалюта и закон*\n\nВот твой гайд! Спасибо за оплату 🙌"
    elif label == "guide_1":
        file = FSInputFile("files/guide_1.pdf")
        caption = "📗 *Гайд 1 — Учёт криптоактивов*\n\nСпасибо за оплату! Вот твой гайд 💼"
    elif label == "guide_2":
        file = FSInputFile("files/guide_2.pdf")
        caption = "📎 *Гайд 2 — Частые ошибки при переводе*\n\nСпасибо за оплату! Надеемся, он поможет тебе избежать потерь 🔍"
    elif label == "guide_3":
        file = FSInputFile("files/guide_3.pdf")
        caption = "📎 *Гайд 3 — Шпаргалка по сетям и комиссиям*\n\nВот шпаргалка! Спасибо за оплату 🧾"
    else:
        return  # Неизвестная метка

    await bot.send_document(chat_id=telegram_id, document=file, caption=caption, parse_mode="Markdown")


# === 🟦 БЛОК 4: ЗАПУСК FASTAPI ===
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
