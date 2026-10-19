async function routeToMasterBridge(commandName, userText) {
    try {
        const response = await fetch("https://masters-megawin-bridge.onrender.com/api/synthesize", {
            method: "POST",
            headers: { "Content-Type": "application/json", "Accept": "application/json" },
            body: JSON.stringify({ command: parsedCommandName, text: userText })
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

document.addEventListener("DOMContentLoaded", () => {
    const outputDiv = document.getElementById("terminal-output");
    const inputField = document.getElementById("terminal-input");

    if (!inputField || !outputDiv) return;

    function printToTerminal(text, isCommand = false) {
        const newLine = document.createElement("div");
        newLine.style.marginBottom = "10px";
        newLine.style.whiteSpace = "pre-wrap";
        newLine.innerText = isCommand ? "> " + text : text;
        outputDiv.appendChild(newLine);
        outputDiv.scrollTop = outputDiv.scrollHeight;
    }

    inputField.addEventListener("keydown", async (event) => {
        if (event.key === "Enter") {
            const rawInput = inputField.value.trim();
            if (!rawInput) return;

            printToTerminal(rawInput, true);
            inputField.value = ""; 
            
            const parts = rawInput.split(" ");
            const command = parts[0].toLowerCase();
            const payloadText = parts.slice(1).join(" "); 

            // Whitelist expanded to include /analyze_code
            const validCommands = ["/job_lead", "/grant_lead", "/analyze_code", "swarm", "apex", "evolve", "evolve 01"];

            if (validCommands.includes(command)) {
                printToTerminal("Uplinking to Master Bridge... [Awaiting Phase Lock]");
                inputField.disabled = true; 
                
                const result = await routeToMasterBridge(command, payloadText || "Execute standard protocol.");
                
                printToTerminal(result);
                inputField.disabled = false; 
                inputField.focus();
            } else {
                printToTerminal(`Unrecognized command. Valid protocols: /job_lead, /grant_lead, /analyze_code, swarm, apex, evolve`);
            }
        }
    });
    
    printToTerminal("U4U Terminal Initialized. Enter a protocol to begin (e.g., /analyze_code def hello_world(): pass).");
});
