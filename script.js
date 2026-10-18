// U4U Terminal - Frontend Logic

// --- 1. Master Bridge Pipeline ---
async function routeToMasterBridge(commandName, userText) {
    try {
        const response = await fetch("https://masters-megawin-bridge.onrender.com/api/synthesize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                command: commandName,
                text: userText
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            return data.response;
        } else {
            return "Error: Master Bridge rejected the payload.";
        }
    } catch (error) {
        return "Critical Error: Could not reach the U4U Master Bridge. Check uplink.";
    }
}

// --- 2. Terminal UI Logic ---
document.addEventListener("DOMContentLoaded", () => {
    const outputDiv = document.getElementById("terminal-output");
    const inputField = document.getElementById("terminal-input");

    if (!inputField || !outputDiv) {
        console.warn("System Notice: Please ensure your HTML contains <div id='terminal-output'></div> and <input id='terminal-input'>");
        return;
    }

    // Helper to write text to the screen
    function printToTerminal(text, isCommand = false) {
        const newLine = document.createElement("div");
        newLine.style.marginBottom = "10px";
        newLine.style.whiteSpace = "pre-wrap"; // Preserves formatting from the backend
        newLine.innerText = isCommand ? "> " + text : text;
        
        outputDiv.appendChild(newLine);
        outputDiv.scrollTop = outputDiv.scrollHeight; // Auto-scroll to bottom
    }

    // Listen for 'Enter' key
    inputField.addEventListener("keydown", async (event) => {
        if (event.key === "Enter") {
            const rawInput = inputField.value.trim();
            if (!rawInput) return;

            // 1. Print what the user typed
            printToTerminal(rawInput, true);
            inputField.value = ""; // clear input box
            
            // 2. Parse the command
            const parts = rawInput.split(" ");
            const command = parts[0].toLowerCase(); // e.g., "/job_lead"
            const payloadText = parts.slice(1).join(" "); // everything after the command

            // Master list of commands your Render backend supports
            const validCommands = ["/job_lead", "/grant_lead", "swarm", "apex", "evolve"];

            if (validCommands.includes(command)) {
                printToTerminal("Uplinking to Master Bridge... [Awaiting Phase Lock]");
                
                inputField.disabled = true; // Lock input while waiting
                
                // 3. Send to Render Backend
                const result = await routeToMasterBridge(command, payloadText || "Execute standard protocol.");
                
                // 4. Print Backend Response
                printToTerminal(result);
                
                inputField.disabled = false; // Unlock input
                inputField.focus();
            } else {
                printToTerminal(`Unrecognized command. Valid protocols: /job_lead, /grant_lead, swarm, apex, evolve`);
            }
        }
    });
    
    // Initial boot sequence greeting
    printToTerminal("U4U Terminal Initialized. Enter a protocol to begin (e.g., /job_lead Hello).");
});