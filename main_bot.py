import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

# Загрузка переменных среды
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверка токена
if not BOT_TOKEN:
    print("❌ Токен не найден. Убедитесь, что он указан в .env")
    exit()

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📘 Каталог курсов",
                                 callback_data="catalog_courses"),
            InlineKeyboardButton(text="ℹ️ О проекте",
                                 callback_data="about_project"),
        ],
        [
            InlineKeyboardButton(text="📗 Каталог гайдов",
                                 callback_data="catalog_guides"),
            InlineKeyboardButton(text="❓ Задать вопрос",
                                 callback_data="ask_question"),
        ]
    ])

    await message.answer(
        "👋 Привет! Добро пожаловать в наш бот.\n\n"
        "Ты в проекте <b>«Знания для реальной жизни»</b> — здесь всё просто, понятно и по делу.\n"
        "Здесь ты найдёшь образовательные курсы, мини-гайды и пошаговые инструкции по самым актуальным темам.\n\n"
        "<b>Выбери, с чего хочешь начать:</b>",
        reply_markup=keyboard)


# 🟩 Блок 2 — Кнопка «📘 Каталог курсов» (основное сообщение + две кнопки)
@dp.callback_query(lambda c: c.data == "catalog_courses")
async def show_course_catalog(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🔥 Путь в криптомир — от первого шага до стратегии",
                callback_data="to_course_levels")
        ],
                         [
                             InlineKeyboardButton(
                                 text="🔙 Вернуться в начало",
                                 callback_data="back_to_start")
                         ]])
    await callback.message.edit_text(
        "🎓 *Каталог курсов*\n\n"
        "Здесь собраны все наши обучающие курсы.\n"
        "Сейчас доступен один, но очень мощный:\n\n"
        "🔥 *«Путь в криптомир — от первого шага до стратегии»*\n\n"
        "Курс разбит на 3 уровня: от базового к экспертному — чтобы вы могли двигаться в своём темпе.\n\n"
        "_Жми на курс, выбирай подходящий тебе уровень и будь в ногу со временем._",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# 🟩 Блок 3 — Кнопка «🔥 Путь в криптомир...» → открывает 3 уровня курса
@dp.callback_query(lambda c: c.data == "to_course_levels")
async def show_course_levels(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🟩 Базовый курс — Криптовалюта без паники",
                callback_data="course_basic")
        ],
        [
            InlineKeyboardButton(
                text="🟦 Продвинутый курс — Крипта на практике",
                callback_data="course_advanced")
        ],
        [
            InlineKeyboardButton(text="🟪 Экспертный курс — (в разработке)",
                                 callback_data="course_expert")
        ],
        [
            InlineKeyboardButton(text="⬅ 🎓 Вернуться в Каталог курсов",
                                 callback_data="catalog_courses")
        ]
    ])
    await callback.message.edit_text(
        "🔥 *Этот курс — ваш билет в мир криптовалюты.*\n\n"
        "Шаг за шагом, уровень за уровнем, мы проведём вас от полного нуля до уверенных действий и продвинутых стратегий.\n"
        "_Он состоит из трёх уровней, которые идут один за другим — как лестница вверх._\n\n"
        "— Сначала вы поймёте азы без перегрузки и стресса\n"
        "— Затем разберётесь в практике\n"
        "— А в финале — научитесь выстраивать свои стратегии и принимать решения с уверенностью\n\n"
        "*Курс поможет не просто разобраться — а начать применять и зарабатывать.*",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# 🟩 Блок 4 — Возврат в приветственное сообщение (по кнопке «🔙 Вернуться в начало»)
@dp.callback_query(lambda c: c.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="📘 Каталог курсов",
                                 callback_data="catalog_courses"),
            InlineKeyboardButton(text="ℹ️ О проекте",
                                 callback_data="about_project")
        ],
                         [
                             InlineKeyboardButton(
                                 text="📚 Каталог гайдов",
                                 callback_data="catalog_guides"),
                             InlineKeyboardButton(text="❓ Задать вопрос",
                                                  callback_data="ask_question")
                         ]])
    await callback.message.edit_text(
        "Привет! 👋\n"
        "Добро пожаловать в наш бот.\n"
        "Ты в проекте *\"Знания для реальной жизни\"* — здесь всё просто, понятно и по делу. "
        "Здесь ты найдёшь образовательные курсы, мини-гайды и пошаговые инструкции по самым актуальным темам.\n\n"
        "Выбери, с чего хочешь начать: 👇",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# 🟩 Блок 5 — Кнопка «🟩 Базовый курс — Криптовалюта без паники»
@dp.callback_query(lambda c: c.data == "course_basic")
async def show_basic_course(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="💳 Оплатить",
                                 url="https://yookassa.ru/my/i/aIoNsjvr2OgG/l")
        ],
                         [
                             InlineKeyboardButton(
                                 text="⬅ 🎓 Назад к уровням курса",
                                 callback_data="to_course_levels")
                         ]])
    await callback.message.edit_text(
        "📗 *Курс 1 — «Криптовалюта без паники»*\n"
        "_Пошагово • С нуля • Понятным языком_\n\n"
        "🎓 Это курс для тех, кто хочет разобраться в криптовалюте — но боится начинать.\n\n"
        "Мы объясняем всё простым и доступным языком:\n"
        "— что такое блокчейн и токены\n"
        "— как открыть кошелёк\n"
        "— как работать на бирже и P2P\n"
        "— как купить крипту и не потерять её\n"
        "— как не попасть на обман\n\n"
        "Без заумных терминов, без давления, без страха.\n"
        "С примерами и подсказками на каждом шаге.\n\n"
        "💬 *Представьте, что рядом друг, который всё уже прошёл — и теперь спокойно объясняет вам.*\n\n"
        "_Если вам всегда казалось, что «это не для меня, слишком сложно» — этот курс покажет, что это не так._",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# 🟦 Блок 6 — Кнопка «🟦 Продвинутый курс — Крипта на практике»
@dp.callback_query(lambda c: c.data == "course_advanced")
async def show_advanced_course(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="💳 Оплатить",
                                 url="https://yookassa.ru/my/i/aIpyCedjJcM7/l")
        ],
                         [
                             InlineKeyboardButton(
                                 text="⬅ 🎓 Назад к уровням курса",
                                 callback_data="to_course_levels")
                         ]])

    await callback.message.edit_text(
        "🟦 *Курс 2 — Крипта на практике*\n\n"
        "📅 _Старт 25 сентября_\n\n"
        "Этот курс — для тех, кто уже попробовал крипту, но хочет разобраться глубже.\n\n"
        "🔹 Вы уже открыли кошелёк, купили USDT — а дальше неуверенность.\n"
        "🔹 Что делать с этим дальше?\n"
        "🔹 Как избежать ошибок? Где не слить?\n\n"
        "Здесь всё разложено по полочкам. Без паники. На реальных примерах.",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# 🟪 Блок 7 — Кнопка «🟪 Экспертный курс — Крипта по-взрослому»
@dp.callback_query(lambda c: c.data == "course_expert")
async def show_expert_course(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="💳 Оплатить",
                                 url="https://yookassa.ru/my/i/aIpyXP8pfPH-/l")
        ],
                         [
                             InlineKeyboardButton(
                                 text="⬅ 🎓 Назад к уровням курса",
                                 callback_data="to_course_levels")
                         ]])

    await callback.message.edit_text(
        "🟪 *Курс 3 — Экспертный уровень*\n\n"
        "📅 _Старт 25 ноября_\n\n"
        "Этот курс скоро появится в доступе.\n\n"
        "Оставьте заявку, если хотите попасть в список ожидания 👇",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# 🟩 БЛОК 4 — КАТАЛОГ ГАЙДОВ
# Обработка кнопки "📚 Каталог гайдов" — показывает список доступных мини-гайдов


@dp.callback_query(lambda c: c.data == "catalog_guides")
async def catalog_guides(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📎 Гайд 1 — Учёт криптоактивов",
                                 callback_data="guide_1")
        ],
        [
            InlineKeyboardButton(text="📎 Гайд 2 — Частые ошибки при переводе",
                                 callback_data="guide_2")
        ],
        [
            InlineKeyboardButton(
                text="📎 Гайд 3 — Шпаргалка по сетям и комиссиям",
                callback_data="guide_3")
        ],
        [
            InlineKeyboardButton(text="📎 Гайд 4 — Криптовалюта и закон",
                                 callback_data="guide_4")
        ],
        [
            InlineKeyboardButton(text="⬅ Назад в начало",
                                 callback_data="back_to_start")
        ]
    ])
    await callback.message.edit_text(
        "📚 *Каталог гайдов*\n\n"
        "Здесь собраны полезные мини-гайды и шпаргалки: всё самое важное — коротко, чётко и по делу.\n\n"
        "Выбирай нужный — и получай готовое решение!",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# 🟩 БЛОК 5 — КАЖДЫЙ ГАЙД ПО ОТДЕЛЬНОСТИ


# 🟩 Обработка гайда 1 — Учёт криптоактивов
@dp.callback_query(lambda c: c.data == "guide_1")
async def show_guide_1(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="💳 Оплатить",
                                 url="https://yookassa.ru/my/i/aIoJFtd_ELsI/l")
        ],
                         [
                             InlineKeyboardButton(
                                 text="⬅ Назад к гайдам",
                                 callback_data="catalog_guides")
                         ]])
    await callback.message.edit_text(
        "📗 *Гайд 1 — Учёт криптоактивов*\n\n"
        "Этот гайд — для тех, кто не хочет потом разгребать хаос в кошельках, биржах, паролях и seed-фразах.\n\n"
        "💡 Где и в чём удобно вести учёт\n"
        "💡 Что важно для личной безопасности\n"
        "📎 Простой гайд с наглядными примерами таблиц.\n\n"
        "👉 Стоимость: 299 рублей\n"
        "🔒 Получишь гайд сразу после оплаты",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# 🟩 Обработка гайда 2 — Частые ошибки при переводе
@dp.callback_query(lambda c: c.data == "guide_2")
async def show_guide_2(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    payment_url = f"https://yookassa.ru/my/i/aIaTihMCqIE8/l?label=guide_2_{user_id}"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
        [
            InlineKeyboardButton(text="⬅ Назад к гайдам",
                                 callback_data="catalog_guides")
        ]
    ])

    await callback.message.edit_text(
        "📎 *Гайд 2 — Частые ошибки при переводе*\n\n"
        "💣 Самые распространённые ошибки новичков\n"
        "при переводах крипты — и как их избежать:\n"
        "— забыли выбрать нужную сеть\n"
        "— указали неправильный адрес\n"
        "— перевели USDT вместо USDC\n"
        "— оплатили, но не нажали «Подтвердить»\n\n"
        "Этот гайд — как страховка от глупых потерь.\n"
        "Покажем самые типичные ошибки —\n"
        "и дадим алгоритм, как действовать,\n"
        "чтобы не потерять деньги навсегда.\n"
        "Подойдёт даже тем, кто уже пару раз переводил —\n"
        "но каждый раз делает это с волнением.\n\n"
        "👉 Стоимость: 299 рублей\n"
        "🔒 Получишь гайд сразу после оплаты",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# Обработка гайда 3 — Шпаргалка по сетям и комиссиям
@dp.callback_query(lambda c: c.data == "guide_3")
async def show_guide_3(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="💳 Оплатить",
                                 url="https://yookassa.ru/my/i/aIoKoti5cRw7/l")
        ],
                         [
                             InlineKeyboardButton(
                                 text="⬅ Назад к гайдам",
                                 callback_data="catalog_guides")
                         ]])
    await callback.message.edit_text(
        "📎 *Гайд 3 — Шпаргалка по сетям и комиссиям*\n\n"
        "📗 Гайд «Шпаргалка — сети и комиссия»\n\n"
        "В этом вопросе происходит путаница у 9 из 10 новичков: сеть Ethereum, сеть BNB, TRC-20, а ещё комиссии, которые съедают всё удовольствие.\n\n"
        "😵 Что выбрать? Где дешевле? Почему не дошло? Почему списалось больше?\n\n"
        "💡 Как понять, в какой сети лежит ваша монета?\n"
        "И как не сжечь деньги на комиссии?\n\n"
        "Этот гайд — краткая, но наглядная шпаргалка:\n"
        "- какие монеты в каких сетях живут\n"
        "- что такое сеть\n"
        "- и чем они отличаются\n"
        "- в какой сети лучше переводить\n"
        "- как не ошибиться при выборе\n"
        "- и почему газ — это не про кухню 😊\n\n"
        "Если вы когда-то терялись между BNB Smart Chain и Ethereum,\n"
        "или не понимали, почему комиссии разные —\n"
        "этот гайд сэкономит вам и нервы, и деньги.\n\n"
        "👉 Стоимость: 299 рублей\n"
        "🔒 Получишь гайд сразу после оплаты",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# 🟦 Обработка гайда 4 — Криптовалюта и закон
@dp.callback_query(lambda c: c.data == "guide_4")
async def show_guide_4(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="💳 Оплатить",
                                url="https://yookassa.ru/my/i/aIYEiVg6P4R7/l?label=guide_law")
        ],
                         [
                             InlineKeyboardButton(
                                 text="⬅ Назад к гайдам",
                                 callback_data="catalog_guides")
                         ]])
    await callback.message.edit_text(
        "🛡️ *Криптовалюта и закон — просто и без паники*\n\n"
        "💬 Ты наверняка слышал, что криптовалюта — это \"вне закона\" или \"опасно\". На самом деле всё проще. Но надо разобраться и понимать.\n"
        "Ты не юрист — и не обязан им быть.\n"
        "Но ты точно должен понимать, что можно, а что нельзя, чтобы спать спокойно.\n\n"
        "📎 В этом гайде — коротко и по делу:\n"
        "— Что говорит закон в 2025 году\n"
        "— Как пользоваться криптой и не бояться проверок\n"
        "— Когда и как отчитываться\n"
        "— Где может быть риск и как его обойти\n\n"
        "⚖️ Если ты хочешь пользоваться криптой — а не бояться её, этот гайд тебе нужен.\n"
        "👉 Стоимость: 299 рублей\n"
        "🔒 Получишь гайд сразу после оплаты",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
