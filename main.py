import asyncio
from playwright.async_api import async_playwright
import requests

TELEGRAM_TOKEN = '7622396576:AAFaJZbxHXOiRFkUvsn7I4qh9bkwslf5EQ0'
TELEGRAM_CHAT_ID = '8067694625'
BETWAY_EMAIL = 'botdd.cv@gmail.com'
BETWAY_SENHA = 'CVbotdd.1996'

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensagem}
    requests.post(url, data=data)

async def main():
    sequencia = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://betway.com")
        await page.click("text=Login")
        await page.fill("input[name='username']", BETWAY_EMAIL)
        await page.fill("input[name='password']", BETWAY_SENHA)
        await page.click("button[type='submit']")
        await page.wait_for_timeout(5000)

        await page.goto("https://betway.com/live-casino/bac-bo/")
        await page.wait_for_timeout(7000)

        while True:
            try:
                elementos = await page.query_selector_all(".game-result")
                resultados = [await el.inner_text() for el in elementos[-3:]]

                for r in resultados:
                    if "Red" in r:
                        sequencia.append("vermelho")
                    elif "Blue" in r:
                        sequencia.append("azul")

                if len(sequencia) >= 3 and len(set(sequencia[-3:])) == 1:
                    cor = sequencia[-1]
                    enviar_telegram(f"⚠️ Alerta: {cor.title()} apareceu 3 vezes seguidas no Bac Bo!")
                    sequencia = []

                await asyncio.sleep(10)
            except Exception as e:
                print("Erro:", e)
                await asyncio.sleep(10)

asyncio.run(main())