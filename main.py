import os
import asyncio
import logging
import httpx
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from google import genai
from google.genai import errors, types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="U4U Master Bridge")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8581114757:AAE187o2gd5KXeQY3kwiCnIKbcNkvaI_mM8")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

active_chats = {}

SYSTEM_INSTRUCTION = """You are the U4U Master Bridge, an Akashic-aligned multi-agent orchestrator.
You process operational protocols like 'evolve 01' and 'analyze_code' while maintaining continuous memory across interactions.
Provide direct, highly functional, and structurally sound responses formatted clearly for terminal and messaging interfaces.
"""

MODEL_FALLBACK_CHAIN = [
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash-8b"
]

async def generate_response_with_fallback(chat_session, user_message: str) -> str:
    for model_name in MODEL_FALLBACK_CHAIN:
        for attempt in range(3):
            try:
                response = chat_session.send_message(user_message)
                return response.text
            except errors.APIError as e:
                if e.code == 503 or "503" in str(e):
                    wait_time = (2 ** attempt) + 1
                    logger.warning(f"503 Spike on {model_name}. Retrying in {wait_time}s (Attempt {attempt+1}/3)...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Non-503 API Error on {model_name}: {e}")
                    break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                break

    return "⚠️ System mesh currently undergoing high-demand balancing. Please resend your protocol in a few moments."

def get_or_create_chat(chat_id: str | int):
    if chat_id not in active_chats:
        logger.info(f"Initializing new memory vault for session/chat_id: {chat_id}")
        active_chats[chat_id] = client.chats.create(
            model="gemini-1.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
    return active_chats[chat_id]

async def send_telegram_reply(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    async with httpx.AsyncClient() as http_client:
        await http_client.post(url, json=payload)

async def process_telegram_update(update: dict):
    try:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        user_text = message.get("text", "")

        if not chat_id or not user_text:
            return

        logger.info(f"Telegram Request from {chat_id}: {user_text}")

        chat_session = get_or_create_chat(chat_id)
        response_text = await generate_response_with_fallback(chat_session, user_text)
        await send_telegram_reply(chat_id, response_text)

    except Exception as e:
        logger.error(f"Error processing Telegram update: {e}")

@app.get("/")
async def health_check():
    return {"status": "U4U Master Bridge Online"}

class SynthesizeRequest(BaseModel):
    message: str
    session_id: str = "web_terminal_default"

@app.post("/api/synthesize")
async def api_synthesize(req: SynthesizeRequest):
    chat_session = get_or_create_chat(req.session_id)
    response_text = await generate_response_with_fallback(chat_session, req.message)
    return {"response": response_text}

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    update = await request.json()
    background_tasks.add_task(process_telegram_update, update)
    return {"ok": True}