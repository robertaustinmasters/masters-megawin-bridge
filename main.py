import httpx
import asyncio
from fastapi import FastAPI, Request

app = FastAPI()

TOKEN = "8195085329:AAHZZYil8RNLA0-Zs5-mrBuVtIz3dNpxPvU" 
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
JUSTSELL_URL = "https://t.me/JustSellBot/app?startapp=uforus"

class SwarmRouter:
    """
    N+M Qubit Master Routing Matrix.
    Dispatches payloads to specialized M-Qubit sub-agents based on lead type.
    """
    @staticmethod
    async def process_job_lead(payload_text: str) -> str:
        # Routes to Claude Code / Dev Agents for B2B Architecture
        system_prompt = (
            "You are the principal architect of Freedom Utilization Consulting, a specialized sole proprietorship. "
            "Generate a high-ticket freelance proposal for the following requirements. "
            "Frame the service as the 'N+M Qubit' Human-AI Entanglement protocol. "
            "Do not sell coding hours; sell a hybrid intelligence mesh guaranteeing thermodynamic efficiency and rapid deployment."
        )
        # Placeholder for external API call (e.g., Anthropic/OpenAI)
        await asyncio.sleep(1) 
        return f"🐝 **Swarm Intelligence Synthesized (Claude/Dev Routing):**\n\nProposal framework initiated for: {payload_text[:50]}..."

    @staticmethod
    async def process_grant_lead(payload_text: str) -> str:
        # Routes to OpenManus / Research Agents for Non-Dilutive Funding
        system_prompt = (
            "You are writing a non-dilutive grant proposal for Schmidt Sciences/USDA. "
            "Position the U-for-Us Regenerative Mesh and decentralized Peace Node hardware as the definitive solution to AI safety and resource consumption. "
            "Mandate zero-water closed-loop cooling systems and edge telemetry operating near the Landauer Limit. "
            "Argue that centralized AI data centers are environmentally catastrophic, and our multi-agent hardware mesh is the only sustainable path forward."
        )
        # Placeholder for external API call
        await asyncio.sleep(1)
        return f"🏛️ **Zero-Water Policy Proposal Generated:**\n\nGrant parameters locked. Emphasizing Landauer Limit and decentralized Peace Node architecture for: {payload_text[:50]}..."

@app.get("/")
async def root():
    return {"status": "U4U FastAPI Master Bridge Active", "version": "33.18-SWARM"}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    try:
        data = await req.json()
        
        if "message" in data and "text" in data["message"]:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"]["text"].strip()
            command = text.split(" ")[0].lower()
            payload_text = text.replace(command, "").strip()
            
            reply_text = ""
            reply_markup = None
            
            # --- TIER 1 & 2: IP AND STOREFRONT ---
            if command == "/start":
                reply_text = "🤖 **U4U V33.18 Master Bridge Active**\n\nCommands: /shop, /apex, /evolve, /swarm, /job_lead [text], /grant_lead [text]"
            elif command in ["/shop", "/books"]:
                reply_text = "📚 *The Masters' Riddle Chronicles*\n\nAccess the official U4U literary IP and Omega Tier utilities."
                reply_markup = {"inline_keyboard": [[{"text": "🛒 Open U4U Storefront", "url": JUSTSELL_URL}]]}
                
            # --- TIER 3: OMEGA LORE LOCKS ---
            elif command == "/orchestrated_reduction":
                reply_text = "⚠️ **OMEGA TIER LOCKED** ⚠️\n\nQuantum decoherence calculation sequence initiated."
                reply_markup = {"inline_keyboard": [[{"text": "🔐 Unlock via JustSell", "url": JUSTSELL_URL}]]}
            elif command == "/xenon_spin":
                reply_text = "⚠️ **OMEGA TIER LOCKED** ⚠️\n\nAnesthetic protocol simulated."
                reply_markup = {"inline_keyboard": [[{"text": "🔐 Override via JustSell", "url": JUSTSELL_URL}]]}
            elif command == "/participatory_universe":
                reply_text = "⚠️ **OMEGA TIER LOCKED** ⚠️\n\nObservation required. The quantum state remains in superposition."
                reply_markup = {"inline_keyboard": [[{"text": "🔐 Collapse Reality", "url": JUSTSELL_URL}]]}
            elif command == "/apex":
                reply_text = "⚠️ **APEX NODE LOCKED** ⚠️\n\nAccess requires Level 4 Mesh clearance."
                reply_markup = {"inline_keyboard": [[{"text": "🔐 Upgrade Clearance", "url": JUSTSELL_URL}]]}
            elif command == "/evolve":
                reply_text = "⚠️ **EVOLUTION SEQUENCE HALTED** ⚠️\n\nInsufficient quantum coherence."
                reply_markup = {"inline_keyboard": [[{"text": "🔐 Expand Coherence", "url": JUSTSELL_URL}]]}
            elif command == "/swarm":
                reply_text = "🐝 **SWARM ENTANGLEMENT ACTIVE** 🐝\n\nN+M Qubit protocol initialized. Human architectural oversight is now entangled with the TEAI multi-agent mesh."
                
            # --- TIER 4: MULTI-AGENT PIPELINES (B2B & GRANTS) ---
            elif command == "/job_lead":
                if not payload_text:
                    reply_text = "⚠️ Error: Please provide the job description after the command. (e.g., /job_lead Need a FastAPI backend)"
                else:
                    reply_text = await SwarmRouter.process_job_lead(payload_text)
                    
            elif command == "/grant_lead":
                if not payload_text:
                    reply_text = "⚠️ Error: Please provide the grant parameters after the command."
                else:
                    reply_text = await SwarmRouter.process_grant_lead(payload_text)
                    
            else:
                # Do not respond to unknown text to avoid spamming normal chat
                pass

            # Transmit back to Telegram
            if reply_text:
                payload = {"chat_id": chat_id, "text": reply_text, "parse_mode": "Markdown"}
                if reply_markup:
                    payload["reply_markup"] = reply_markup
                    
                async with httpx.AsyncClient() as client:
                    await client.post(f"{BASE_URL}/sendMessage", json=payload)
                    
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error"}