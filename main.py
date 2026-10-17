import httpx
import asyncio
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for direct browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,  # <-- THIS MUST BE FALSE
    allow_methods=["*"],
    allow_headers=["*"],
)

GROK_API_KEY = os.environ.get("GROK_API_KEY", "YOUR_GROK_API_KEY_HERE")

class SwarmRouter:
    @staticmethod
    async def fetch_grok_completion(system_prompt: str, user_prompt: str) -> str:
        if GROK_API_KEY == "YOUR_GROK_API_KEY_HERE":
            return "⚠️ GROK API KEY MISSING."
            
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "grok-beta",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        async with httpx.AsyncClient(timeout=45.0) as client:
            try:
                response = await client.post(
                    "https://api.x.ai/v1/chat/completions", 
                    headers=headers, 
                    json=payload
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                return f"⚠️ Swarm API Error: {str(e)}"

    @staticmethod
    async def process_job_lead(payload_text: str) -> str:
        system_prompt = (
            "You are the principal architect of Freedom Utilization Consulting, a specialized sole proprietorship. "
            "Generate a highly professional, high-ticket freelance proposal for the following requirements. "
            "Frame the service as the 'N+M Qubit' Human-AI Entanglement protocol. "
            "Do not sell coding hours; sell a hybrid intelligence mesh guaranteeing thermodynamic efficiency."
        )
        return await SwarmRouter.fetch_grok_completion(system_prompt, payload_text)

# Data model for incoming browser requests
class LeadPayload(BaseModel):
    command: str
    text: str

# Direct API endpoint for the web frontend
@app.post("/api/synthesize")
async def api_synthesize(payload: LeadPayload):
    if payload.command == "/job_lead":
        result = await SwarmRouter.process_job_lead(payload.text)
    elif payload.command == "/grant_lead":
        result = await SwarmRouter.process_grant_lead(payload.text)
    else:
        result = "Invalid command sequence."
    
    return {"status": "success", "response": result}

@app.get("/")
async def root():
    return {"status": "U4U FastAPI Master Bridge Active - REST API Mode"}