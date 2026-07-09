const API = "http://localhost:8000";

async function classify() {
  const text = document.getElementById("contract-input").value.trim();
  if (!text) { alert("Please paste a contract."); return; }
  document.getElementById("loading").style.display = "block";
  document.getElementById("results").innerHTML = "";
  document.getElementById("summary-bar").style.display = "none";
  try {
    const res = await fetch(`${API}/classify`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({text}),
    });
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail); }
    renderResults(await res.json());
  } catch(e) { alert("Error: " + e.message); }
  finally { document.getElementById("loading").style.display = "none"; }
}

function renderResults(data) {
  const counts = {};
  data.clauses.forEach(c => { counts[c.category] = (counts[c.category]||0)+1; });
  document.getElementById("summary-text").textContent =
    `${data.total_clauses} clauses in ${data.processing_time_ms}ms — ` +
    Object.entries(counts).map(([k,v])=>`${v} ${k}`).join(" · ");
  document.getElementById("summary-bar").style.display = "block";
  const container = document.getElementById("results");
  data.clauses.forEach(c => {
    const safe = c.category.replace(/[\/\s]/g,"");
    container.innerHTML += `
      <div class="clause-card ${safe}">
        <div style="display:flex;gap:10px;align-items:center">
          <span style="color:#6c757d;font-size:12px">#${c.clause_number}</span>
          <span class="badge ${safe}">${c.category}</span>
          <span style="font-size:12px;color:#6c757d">Confidence: ${(c.confidence*100).toFixed(0)}%</span>
        </div>
        <div class="clause-text">${c.clause_text}</div>
        <div class="clause-reasoning">💡 ${c.reasoning}</div>
      </div>`;
  });
}
