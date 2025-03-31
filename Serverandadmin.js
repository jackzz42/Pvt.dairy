const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const Database = require('better-sqlite3');

const db = new Database('/Persistent/onion_website/solvers.db');

// Create database table if not exists
db.prepare("CREATE TABLE IF NOT EXISTS solvers (ip TEXT UNIQUE, approved INTEGER DEFAULT 0)").run();

app.use(bodyParser.json());

// Handle riddle submission
app.post('/check-code', (req, res) => {
    const correctPhrase = "A Forgotten Way";
    const userCode = req.body.code.trim();
    const userIP = req.headers['x-forwarded-for'] || req.socket.remoteAddress;

    if (userCode !== correctPhrase) {
        return res.json({ message: "❌ Wrong! Try again." });
    }

    try {
        db.prepare("INSERT INTO solvers (ip) VALUES (?)").run(userIP);
    } catch (error) {
        return res.json({ message: "✅ Already submitted! Wait for approval." });
    }

    const count = db.prepare("SELECT COUNT(*) AS total FROM solvers").get().total;

    if (count >= 2) {
        return res.json({ message: "✅ Correct! Waiting for admin approval..." });
    } else {
        return res.json({ message: "✅ Correct! Waiting for another friend to solve..." });
    }
});

// Admin Panel at /admin*_$&
app.get('/admin*_$&', (req, res) => {
    const solvers = db.prepare("SELECT * FROM solvers").all();
    let html = "<h2>Approval Panel</h2>";

    solvers.forEach((row) => {
        html += `<p>IP: ${row.ip} <button onclick="approve('${row.ip}')">Approve</button></p>`;
    });

    html += `
        <script>
            function approve(ip) {
                fetch('/approve', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ip }) })
                .then(response => response.json())
                .then(data => alert(data.message));
            }
        </script>
    `;

    res.send(html);
});

// Approve Users
app.post('/approve', (req, res) => {
    const ip = req.body.ip;
    db.prepare("UPDATE solvers SET approved = 1 WHERE ip = ?").run(ip);
    res.json({ message: "✅ Approved! They can now see the next riddle." });
});

// Show Next Riddle Only to Approved Users
app.get('/next-riddle', (req, res) => {
    const userIP = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    const approved = db.prepare("SELECT approved FROM solvers WHERE ip = ?").get(userIP);

    if (approved && approved.approved === 1) {
        res.send("<h2>Your Next Riddle: Solve This...</h2>");
    } else {
        res.send("<h2>Access Denied! Wait for Admin Approval.</h2>");
    }
});

// Start Server
app.listen(3000, () => console.log('Server running on port 3000'));
