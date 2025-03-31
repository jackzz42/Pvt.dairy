const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const Database = require('better-sqlite3');
const db = new Database('solvers.db');

app.use(bodyParser.json());
app.use(express.static('public'));

// Create table to store the player solving
db.prepare("CREATE TABLE IF NOT EXISTS solvers (ip TEXT UNIQUE, next_step TEXT)").run();

let activePlayerIP = null; // Only one player can be active at a time
let nextStepText = ""; // The next riddle or URL to be sent

app.post('/check-code', (req, res) => {
    const correctPhrase = "A Forgotten Way";
    const userCode = req.body.code.trim();
    const userIP = req.headers['x-forwarded-for'] || req.socket.remoteAddress;

    if (userCode !== correctPhrase) {
        return res.json({ message: "❌ Wrong! Try again." });
    }

    if (activePlayerIP && activePlayerIP !== userIP) {
        return res.json({ message: "🚫 Wait until the first player finishes." });
    }

    activePlayerIP = userIP;
    return res.json({ message: "✅ Correct! Wait for Admin to give you the next way." });
});

// Admin sends the next step (text or URL)
app.post('/set-next-step', (req, res) => {
    const nextStep = req.body.nextStep;

    if (!activePlayerIP) {
        return res.json({ message: "❌ No active player to send the next way." });
    }

    nextStepText = nextStep;
    db.prepare("UPDATE solvers SET next_step = ? WHERE ip = ?").run(nextStep, activePlayerIP);

    return res.json({ message: "✅ Next step sent!" });
});

// Player checks for the next step
app.get('/get-next-step', (req, res) => {
    const userIP = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    
    if (userIP !== activePlayerIP) {
        return res.json({ message: "🚫 Wait until the first player finishes." });
    }

    if (!nextStepText) {
        return res.json({ message: "" });
    }

    return res.json({ nextStep: nextStepText });
});

// Admin Panel API
app.get('/admin-data', (req, res) => {
    res.json({ activePlayer: activePlayerIP });
});

app.listen(3000, () => console.log('Server running on port 3000'));
