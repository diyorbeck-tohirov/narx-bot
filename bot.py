import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# ====== Shu yerdan o'zgartirsangiz bo'ladi ======
SIZES = {"men": "40-44", "women": "36-40"}
GENDER_TEXT = {"men": "Мужские носки", "women": "Женские носки"}
CONTACTS = (
    "📲 Заказ и оформление:\n"
    "☎️ +998 93 481 11 81\n"
    "👤 @Rifattillo\n\n"
    "☎️ +998 93 778 82 87\n"
    "👤 @Tohirv_Diyor"
)
# ================================================


class Form(StatesGroup):
    photo = State()
    name = State()
    price = State()
    gender = State()


dp = Dispatcher()


def build_caption(name: str, price: int, gender: str) -> str:
    price_text = f"{price:,}".replace(",", " ")
    return (
        f"{name} ✨\n"
        f"🧦 {GENDER_TEXT[gender]}\n"
        f"🔥 Цена: {price_text} сум\n\n"
        f"📏 Размер: {SIZES[gender]}\n\n"
        f"📦 Количество — сколько хотите\n\n"
        f"🚚 Доставка по всему Узбекистану 🇺🇿\n\n"
        f"{CONTACTS}"
    )


@dp.message(CommandStart())
@dp.message(Command("cancel"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Form.photo)
    await message.answer("Paypoq rasmini yuboring 📷")


@dp.message(Form.photo, F.photo)
async def got_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(Form.name)
    await message.answer("Nomini yozing (masalan: Jindina Cashmere):")


@dp.message(Form.photo)
async def photo_expected(message: Message):
    await message.answer("Iltimos, rasm yuboring 📷")


@dp.message(Form.name, F.text)
async def got_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(Form.price)
    await message.answer("Narxini yozing (faqat raqam, masalan: 15000):")


@dp.message(Form.price, F.text)
async def got_price(message: Message, state: FSMContext):
    digits = "".join(ch for ch in message.text if ch.isdigit())
    if not digits:
        await message.answer("Narxni raqam bilan yozing, masalan: 15000")
        return
    await state.update_data(price=int(digits))
    await state.set_state(Form.gender)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👨 Erkaklar", callback_data="men"),
                InlineKeyboardButton(text="👩 Ayollar", callback_data="women"),
            ]
        ]
    )
    await message.answer("Jinsini tanlang:", reply_markup=kb)


@dp.callback_query(Form.gender, F.data.in_({"men", "women"}))
async def got_gender(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    caption = build_caption(data["name"], data["price"], call.data)
    await call.message.answer_photo(photo=data["photo"], caption=caption)
    await call.answer()
    await state.set_state(Form.photo)
    await call.message.answer("Tayyor ✅ Yangi post uchun keyingi rasmni yuboring.")


# ---------- Bepul hosting uchun "uyg'oq turish" mini-serveri ----------
# Render shu portga so'rov kutadi, UptimeRobot esa har 5 daqiqada ping yuborib turadi.
async def health(request: web.Request) -> web.Response:
    return web.Response(text="Paypoq post-bot ishlamoqda ✅")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "10000"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Keep-alive server {port}-portda ishlamoqda")


async def main():
    if not TOKEN:
        raise SystemExit("BOT_TOKEN topilmadi. .env faylini yoki Render'dagi Environment Variables'ni tekshiring.")
    await start_web_server()
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
