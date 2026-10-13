# Paypoq post-bot

Rasm yuborasiz, nom/narx/jinsni kiritasiz, bot rasmni tayyor caption bilan qaytaradi.

## Mahalliy ishga tushirish
1. `.env.example` faylidan nusxa olib `.env` nomi bilan saqlang, ichiga bot tokenini yozing.
2. `pip install -r requirements.txt`
3. `python bot.py`

## 24/7 bepul ishlatish (Render + UptimeRobot)
1. Fayllarni GitHub'ga yuklang. **`.env` faylini yuklamang** (u `.gitignore`da turibdi).
2. Render.com: New + > Web Service > repo'ni tanlang.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Instance Type: Free
   - Environment Variables: `BOT_TOKEN` = botingiz tokeni
3. Deploy tugagach Render bergan manzilni UptimeRobot'da HTTP(s) monitor sifatida qo'shing, interval 5 daqiqa.
