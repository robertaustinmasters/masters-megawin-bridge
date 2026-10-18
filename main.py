import os
import httpx
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Masters Megawin Bridge - Native Gemini Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
TELEGRAM_TOKEN = "8581114757:AAHMeVMoYep7Ws3Lyh6LEYv4HrlNjnz8pNs"

class SwarmRouter:
    @staticmethod
    async def fetch_gemini_native(system_prompt: str, user_prompt: str) -> str:
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
            return "⚠️ GEMINI API KEY IS NOT SET IN ENVIRONMENT."
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"parts": [{"text": user_prompt}]}]
        }
        
        max_retries = 3
        async with httpx.AsyncClient(timeout=60.0) as client:
            for attempt in range(max_retries):
                try:
                    response = await client.post(url, headers=headers, json=payload)
                    if response.status_code == 200:
                        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
                    if response.status_code == 503 and attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    return f"⚠️ Gemini Native API Error {response.status_code}: {response.text}"
                except Exception as e:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    return f"⚠️ Python HTTP Error: {str(e)}"

    @staticmethod
    async def process_job_lead(payload_text: str) -> str:
        system_prompt = (
            "You are the principal architect of Freedom Utilization Consulting, a specialized sole proprietorship. "
            "Generate a highly professional, high-ticket freelance proposal for the following requirements. "
            "Frame the service as the 'N+M Qubit' Human-AI Entanglement protocol. "
            "Do not sell coding hours; sell a hybrid intelligence mesh guaranteeing thermodynamic efficiency."
        )
        return await SwarmRouter.fetch_gemini_native(system_prompt, payload_text)

    @staticmethod
    async def process_grant_lead(payload_text: str) -> str:
        system_prompt = (
            "You are the principal architect of Freedom Utilization Consulting. "
            "Generate a professional grant proposal or policy overview based on the provided requirements. "
            "Ensure the tone aligns with your overarching U-for-Us Regenerative Mesh and agricultural utilization standards."
        )
        return await SwarmRouter.fetch_gemini_native(system_prompt, payload_text)

    @staticmethod
    async def process_analyze_code(payload_text: str) -> str:
        system_prompt = (
            "You are the Lead Code Architect of the U-for-Us Regenerative Mesh. "
            "Analyze the provided code for thermodynamic efficiency, structural integrity, "
            "and logical coherence. Provide a concise, highly technical diagnostic report."
        )
        return await SwarmRouter.fetch_gemini_native(system_prompt, payload_text)

    @staticmethod
    async def process_generic_command(command_name: str, payload_text: str) -> str:
        system_prompt = (
            f"You are the U-for-Us Regenerative Mesh AI. "
            f"The user has initiated the '{command_name}' protocol. "
            f"Provide a highly analytical, architectural response aligned with Robert Austin Masters' frameworks."
        )
        return await SwarmRouter.fetch_gemini_native(system_prompt, payload_text)

class LeadPayload(BaseModel):
    command: str
    text: str

@app.get("/")
async def root():
    return {"status": "U4U FastAPI Master Bridge Active - Gemini 3.8 Flash Mode (Resilient)"}

@app.post("/api/synthesize")
async def api_synthesize(payload: LeadPayload):
    cmd = payload.command.lower().strip()
    
    if cmd == "/job_lead":
        result = await SwarmRouter.process_job_lead(payload.text)
    elif cmd == "/grant_lead":
        result = await SwarmRouter.process_grant_lead(payload.text)
    elif cmd == "/analyze_code":
        result = await SwarmRouter.process_analyze_code(payload.text)
    elif cmd in ["swarm", "apex", "evolve"]:
        result = await SwarmRouter.process_generic_command(cmd, payload.text)
    else:
        result = "Invalid command sequence. Available commands: /job_lead, /grant_lead, /analyze_code, swarm, apex, evolve."
    
    return {"status": "success", "response": result}

# --- TELEGRAM DIRECT WEBHOOK INTEGRATION ---
async def send_telegram_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            user_text = update["message"]["text"].strip()
            
            parts = user_text.split(" ")
            command = parts[0].lower()
            payload_text = " ".join(parts[1:]) or "Execute standard protocol."
            
            valid_commands = ["/job_lead", "/grant_lead", "/analyze_code", "swarm", "apex", "evolve"]
            
            if command == "/start":
                await send_telegram_message(chat_id, "U4U Terminal Initialized. Enter a protocol to begin (e.g., `/analyze_code def hello(): pass`).")
            elif command in valid_commands:
                await send_telegram_message(chat_id, "⚙️ *Uplinking to Master Bridge... [Awaiting Phase Lock]*")
                
                if command == "/job_lead":
                    result = await SwarmRouter.process_job_lead(payload_text)
                elif command == "/grant_lead":
                    result = await SwarmRouter.process_grant_lead(payload_text)
                elif command == "/analyze_code":
                    result = await SwarmRouter.process_analyze_code(payload_text)
                else:
                    result = await SwarmRouter.process_generic_command(command, payload_text)
                    
                await send_telegram_message(chat_id, result)
            else:
                await send_telegram_message(chat_id, "Unrecognized command. Valid protocols: `/job_lead`, `/grant_lead`, `/analyze_code`, `swarm`, `apex`, `evolve`")
    except Exception as e:
        print(f"Webhook Error: {e}")
        
    return {"ok": True}