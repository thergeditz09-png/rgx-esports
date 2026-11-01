const content = document.getElementById("content");
const API_URL = "http://127.0.0.1:8000";

const pages = {
  tournaments: `
    <div class="section-heading">
      <div><small>COMPETE NOW</small><h2>TOURNAMENTS</h2></div>
      <span class="live">● LIVE</span>
    </div>
    <div id="tournament-list">
      <div class="empty">
        <div class="empty-icon">⏳</div>
        <h3>LOADING...</h3>
        <p>Fetching tournaments.</p>
      </div>
    </div>`,

  matches: `
    <div class="section-heading"><div><small>YOUR GAMES</small><h2>MY MATCHES</h2></div></div>
    <div class="empty"><div class="empty-icon">🎮</div><h3>NO MATCHES FOUND</h3><p>Your registered matches will appear here.</p></div>`,

  leaderboard: `
    <div class="section-heading"><div><small>TOP PLAYERS</small><h2>LEADERBOARD</h2></div></div>
    <div class="empty"><div class="empty-icon">📊</div><h3>RANKINGS COMING SOON</h3><p>Compete to reach the top.</p></div>`,

  profile: `
    <div class="section-heading"><div><small>PLAYER ACCOUNT</small><h2>MY PROFILE</h2></div></div>
    <div class="empty"><div class="empty-icon">👤</div><h3>PLAYER PROFILE</h3><p>Telegram account integration coming soon.</p></div>`
};

async function loadTournaments() {
  const list = document.getElementById("tournament-list");
  if (!list) return;

  try {
    const response = await fetch(`${API_URL}/tournaments`);
    if (!response.ok) throw new Error("API request failed");

    const tournaments = await response.json();

    if (!tournaments.length) {
      list.innerHTML = `
        <div class="empty">
          <div class="empty-icon">🏆</div>
          <h3>NO TOURNAMENTS YET</h3>
          <p>New tournaments will appear here.</p>
        </div>`;
      return;
    }

    list.innerHTML = tournaments.map(t => `
      <div class="empty tournament-card">
        <div class="empty-icon">🏆</div>
        <h3>${escapeHTML(t.title)}</h3>
        <p>Game: ${escapeHTML(t.game)}</p>
        <p>Mode: ${escapeHTML(t.mode)}</p>
        <p>Slots: ${Number(t.max_players)}</p>
        <p>Status: ${escapeHTML(t.status)}</p>
      </div>
    `).join("");
  } catch (error) {
    list.innerHTML = `
      <div class="empty">
        <div class="empty-icon">⚠️</div>
        <h3>CONNECTION ERROR</h3>
        <p>Could not connect to the tournament server.</p>
      </div>`;
  }
}

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;",
    '"': "&quot;", "'": "&#39;"
  })[char]);
}

function navigate(page) {
  content.innerHTML = pages[page] || pages.tournaments;

  document.querySelectorAll(".bottom-nav button")
    .forEach(button => button.classList.remove("active"));

  const index = ["tournaments", "matches", "leaderboard", "profile"].indexOf(page);

  if (index >= 0) {
    document.querySelectorAll(".bottom-nav button")[index].classList.add("active");
  }

  if (page === "tournaments") loadTournaments();
}

navigate("tournaments");
