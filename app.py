<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Pinnacle – Planner</title>
  <link rel="stylesheet" href="style.css" />
  <style>
    /* page-specific polish that complements style.css */
    .planner-wrap { max-width: 900px; margin: 0 auto; }
    .inputs { 
      display: grid; 
      grid-template-columns: 1fr 1fr; 
      gap: 1rem; 
      margin: 1rem 0 1.5rem; 
    }
    .inputs .field { 
      background: #fff; 
      color:#111; 
      border-radius: 12px; 
      padding: 1rem; 
      box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    .field label { display:block; font-weight: 600; margin-bottom: .4rem; color:#0f172a;}
    .field input[type="number"], .field select, .field input[type="range"] {
      width: 100%; padding: .6rem .7rem; border-radius: 10px; border: 1px solid #e5e7eb; 
      outline: none; background:#f8fafc; 
    }
    .percent-row { display:flex; align-items:center; gap:.75rem; }
    .pill { 
      display:inline-block; padding:.35rem .7rem; border-radius:999px; 
      background:#e7f5ff; color:#004aad; font-weight:600; font-size:.9rem;
    }

    .result-box { margin-top: 1.5rem; background:#ffffff; color:#111; border-radius: 16px; padding: 1.25rem; box-shadow: 0 8px 24px rgba(0,0,0,.08); }
    .amount-line { display:flex; justify-content:space-between; align-items:center; gap:1rem; flex-wrap:wrap; }
    .amount-line h2 { margin:0; color:#0f172a; }
    .mini-note { color:#475569; font-size:.95rem; }
    .alloc-grid { 
      margin-top: 1rem; 
      display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;
    }
    .alloc-card {
      background:#0f172a; color:#fff; border: 1px solid #1f2937; 
      border-radius: 14px; padding: 1rem; transition:.25s; text-decoration:none; 
      display:flex; flex-direction:column; gap:.5rem;
    }
    .alloc-card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,.25); }
    .alloc-card .title { font-weight: 700; font-size:1.05rem; display:flex; align-items:center; gap:.5rem; }
    .bar { height:10px; border-radius:999px; background:#1e293b; overflow:hidden; }
    .bar > span { display:block; height:100%; width:0%; background:#ffd700; transition: width .6s ease; }
    .pct { font-weight:700; color:#ffd700; }
    .backline { text-align:center; margin-top:1.25rem; }
  </style>
</head>
<body>
  <header>
    <h1>💼 Pinnacle – Investment Planner</h1>
    <p>Enter your salary, choose your risk, and get a smart, clickable portfolio mix.</p>
  </header>

  <main class="planner-wrap">
    <div class="inputs">
      <div class="field">
        <label for="salary">Monthly Salary (₹)</label>
        <input id="salary" type="number" min="1000" step="500" placeholder="e.g. 50000">
      </div>

      <div class="field">
        <label for="risk">Risk Appetite</label>
        <select id="risk">
          <option value="low">Low (Safety first)</option>
          <option value="medium">Medium (Balanced)</option>
          <option value="high">High (Growth focus)</option>
        </select>
      </div>

      <div class="field" style="grid-column: span 2;">
        <label for="percent">Invest % of Salary</label>
        <div class="percent-row">
          <input id="percent" type="range" min="5" max="50" value="20" oninput="updateLabel(this.value)">
          <span class="pill"><span id="percentLabel">20</span>%</span>
        </div>
      </div>
    </div>

    <button class="btn" onclick="plan()">Generate Plan</button>

    <div id="result" class="result-box" style="display:none"></div>

    <div class="backline">
      <a href="index.html" class="btn">⬅ Back Home</a>
    </div>
  </main>

  <footer>
    <p>© 2025 Pinnacle • Climb Higher. Invest Smarter.</p>
  </footer>

  <script>
    function updateLabel(v){ document.getElementById('percentLabel').textContent = v; }

    // allocation recipes per risk (percentages must sum to 100)
    const RECIPES = {
      low: [
        { name: "Fixed Deposits", key:"fd", pct: 25, href:"fd.html", emoji:"🏦" },
        { name: "Bonds", key:"bonds", pct: 25, href:"bonds.html", emoji:"📜" },
        { name: "Debt Mutual Funds", key:"debtmf", pct: 25, href:"mutualfunds.html", emoji:"📊" },
        { name: "Gold", key:"gold", pct: 25, href:"gold.html", emoji:"🥇" },
      ],
      medium: [
        { name: "Balanced/Hybrid Mutual Funds", key:"hybridmf", pct: 30, href:"mutualfunds.html", emoji:"📊" },
        { name: "Large Cap Stocks", key:"stocks", pct: 25, href:"stocks.html", emoji:"📈" },
        { name: "REITs", key:"reits", pct: 20, href:"realestate.html", emoji:"🏠" },
        { name: "Gold", key:"gold", pct: 15, href:"gold.html", emoji:"🥇" },
        { name: "Bonds", key:"bonds", pct: 10, href:"bonds.html", emoji:"📜" },
      ],
      high: [
        { name: "Equity (Mid/Small Cap)", key:"stocks", pct: 45, href:"stocks.html", emoji:"📈" },
        { name: "Equity/Index Mutual Funds", key:"equitymf", pct: 25, href:"mutualfunds.html", emoji:"📊" },
        { name: "Crypto (Optional)", key:"crypto", pct: 10, href:"crypto.html", emoji:"💠" },
        { name: "REITs", key:"reits", pct: 10, href:"realestate.html", emoji:"🏠" },
        { name: "Gold", key:"gold", pct: 10, href:"gold.html", emoji:"🥇" },
      ]
    };

    function formatINR(n){
      if(isNaN(n)) return "₹0";
      return "₹" + Number(n).toLocaleString('en-IN', { maximumFractionDigits: 0 });
    }

    function plan(){
      const salary = parseFloat(document.getElementById('salary').value);
      const risk = document.getElementById('risk').value; // low/medium/high
      const percent = parseInt(document.getElementById('percent').value, 10);

      if(!salary || salary < 1000){
        alert("Please enter a valid monthly salary (₹1,000 or more).");
        return;
      }

      const monthlyInvest = (salary * percent) / 100;
      const recipe = RECIPES[risk];

      // build allocation cards
      let cards = "";
      recipe.forEach(item=>{
        const amount = Math.round(monthlyInvest * (item.pct/100));
        cards += `
          <a class="alloc-card" href="${item.href}">
            <div class="title">${item.emoji} ${item.name}</div>
            <div class="mini-note"><span class="pct">${item.pct}%</span> • ${formatINR(amount)} / month</div>
            <div class="bar"><span style="width:${item.pct}%"></span></div>
          </a>
        `;
      });

      document.getElementById('result').style.display = 'block';
      document.getElementById('result').innerHTML = `
        <div class="amount-line">
          <h2>You can invest <span style="color:#004aad">${formatINR(monthlyInvest)}</span> per month</h2>
          <div class="pill">${percent}% of your salary</div>
        </div>
        <p class="mini-note">Click any card to learn more about that investment.</p>
        <div class="alloc-grid">${cards}</div>
      `;
      // smooth scroll to results
      document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
    }
  </script>
</body>
</html>
