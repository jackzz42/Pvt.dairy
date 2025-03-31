function submitCode() {
    var input = document.getElementById("codeInput").value.trim();

    fetch('/check-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: input })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.message;
        
        if (data.nextStep) {
            document.getElementById("nextWay").style.display = "block";
            document.getElementById("nextStep").innerText = data.nextStep;
        }
    });
}

function checkForNextStep() {
    fetch('/get-next-step')
    .then(response => response.json())
    .then(data => {
        if (data.nextStep) {
            document.getElementById("nextWay").style.display = "block";
            document.getElementById("nextStep").innerText = data.nextStep;
        }
    });
}

setInterval(checkForNextStep, 5000); // Check for updates every 5 seconds
