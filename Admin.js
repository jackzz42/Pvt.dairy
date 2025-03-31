function loadAdminPanel() {
    fetch('/admin-data')
    .then(response => response.json())
    .then(data => {
        let html = "<h3>Active Player</h3>";

        if (data.activePlayer) {
            html += `<p>Current Player: ${data.activePlayer}</p>`;
            html += `<input type="text" id="nextStepInput" placeholder="Enter Next Step (URL/Text)">`;
            html += `<button onclick="sendNextStep()">Send Next Step</button>`;
        } else {
            html += "<p>No active player.</p>";
        }

        document.getElementById("adminContent").innerHTML = html;
    });
}

function sendNextStep() {
    var nextStep = document.getElementById("nextStepInput").value.trim();
    
    fetch('/set-next-step', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nextStep })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

setInterval(loadAdminPanel, 5000); // Refresh admin panel every 5 seconds
