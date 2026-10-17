import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Masters Megawin Bridge - Native Gemini Engine")

# Secure open backend configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

class SwarmRouter:
    @staticmethod
    async def fetch_gemini_native(system_prompt: str, user_prompt: str) -> str:
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
            return "⚠️ GEMINI API KEY IS NOT SET IN ENVIRONMENT."
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Native Google Gemini payload structure (strict camelCase)
        payload = {
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "parts": [
                        {"text": user_prompt}
                    ]
                }
            ]
        }
        
        async with httpx.AsyncClient(timeout=45.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    return f"⚠️ Gemini Native API Error {response.status_code}: {response.text}"
                    
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
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
    async def process_generic_command(command_name: str, payload_text: str) -> str:
        system_prompt = (
            f"You are the U-for-Us Regenerative Mesh AI. "
            f"The user has initiated the '{command_name}' protocol. "
            f"Provide a highly analytical, architectural response aligned with Robert Austin Masters' frameworks."
        )
        return await SwarmRouter.fetch_gemini_native(system_prompt, payload_text)


# Data model for incoming browser requests
class LeadPayload(BaseModel):
    command: str
    text: str

# Health Check Endpoint
@app.get("/")
async def root():
    return {"status": "U4U FastAPI Master Bridge Active - Gemini 3.8 Flash Mode"}

# Direct API endpoint for the web frontend
@app.post("/api/synthesize")
async def api_synthesize(payload: LeadPayload):
    cmd = payload.command.lower().strip()
    
    if cmd == "/job_lead":
        result = await SwarmRouter.process_job_lead(payload.text)
    elif cmd == "/grant_lead":
        result = await SwarmRouter.process_grant_lead(payload.text)
    elif cmd in ["swarm", "apex", "evolve"]:
        result = await SwarmRouter.process_generic_command(cmd, payload.text)
    else:
        result = "Invalid command sequence. Available commands: /job_lead, /grant_lead, swarm, apex, evolve."
    
    return {"status": "success", "response": result}