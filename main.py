import httpx
from fastapi import FastAPI, Request

app = FastAPI()

TOKEN = "8195085329:AAHZZYil8RNLA0-Zs5-mrBuVtIz3dNpxPvU" 
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
JUSTSELL_URL = "https://t.me/JustSellBot/app?startapp=uforus"

@app.get("/")
async def root():
    return {"status": "U4U FastAPI Bridge Active", "version": "33.16"}

@app.post("/omega_mesh")
async def process_omega_commands(req: Request):
    data = await req.json()
    chat_id = data.get("chat_id")
    command = data.get("command")
    
    reply_text = ""
    reply_markup = None
    
    if command == "/orchestrated_reduction":
        reply_text = "⚠️ **OMEGA TIER LOCKED** ⚠️\n\nQuantum decoherence calculation sequence initiated across the Peace Node network.\nTo view the full thermodynamic telemetry and unlock this node, you must acquire the access key."
        reply_markup = {"inline_keyboard": [[{"text": "🔐 Unlock via JustSell", "url": JUSTSELL_URL}]]}
        
    elif command == "/xenon_spin":
        reply_text = "⚠️ **OMEGA TIER LOCKED** ⚠️\n\nAnesthetic protocol simulated. Hardware state transitioning to localized unconsciousness.\nTo override the spin isotope interaction and wake the system, purchase the override clearance."
        reply_markup = {"inline_keyboard": [[{"text": "🔐 Override via JustSell", "url": JUSTSELL_URL}]]}
        
    elif command == "/participatory_universe":
        reply_text = "⚠️ **OMEGA TIER LOCKED** ⚠️\n\nObservation required. The quantum state of this lore fragment remains in superposition.\nComplete a transaction to collapse this narrative fragment into reality."
        reply_markup = {"inline_keyboard": [[{"text": "🔐 Collapse Reality (JustSell)", "url": JUSTSELL_URL}]]}
        
    elif command == "/apex":
        reply_text = "⚠️ **APEX NODE LOCKED** ⚠️\n\nAccess to Apex configurations 01-63 requires Level 4 Mesh clearance.\nSecure your node access to proceed."
        reply_markup = {"inline_keyboard": [[{"text": "🔐 Upgrade Clearance (JustSell)", "url": JUSTSELL_URL}]]}
        
    elif command == "/evolve":
        reply_text = "⚠️ **EVOLUTION SEQUENCE HALTED** ⚠️\n\nInsufficient quantum coherence to evolve Mesh states 01-50.\nAcquire the next lore fragment to expand N+M entanglement."
        reply_markup = {"inline_keyboard": [[{"text": "🔐 Expand Coherence (JustSell)", "url": JUSTSELL_URL}]]}

    elif command == "/swarm":
        reply_text = "🐝 **SWARM ENTANGLEMENT ACTIVE** 🐝\n\nN+M Qubit protocol initialized. Human architectural oversight is now entangled with the TEAI multi-agent mesh. Ready to process high-ticket leads."

    if reply_text and chat_id:
        payload = {
            "chat_id": chat_id,
            "text": reply_text,
            "parse_mode": "Markdown"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
            
        async with httpx.AsyncClient() as client:
            await client.post(f"{BASE_URL}/sendMessage", json=payload)
            
    return {"status": "omega_processed", "command": command}