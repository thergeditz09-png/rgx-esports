const content = document.getElementById("content");
const API_URL = "http://127.0.0.1:8000";

const tg = window.Telegram?.WebApp;
if (tg) {
  tg.ready();
  tg.expand();
}

let isAdmin = false;

const pages = {
  tournaments: `
    <div class="section-heading">
      <div><small>COMPETE NOW</small><h2>TOURNAMENTS</h2></div>
      <span class="live">● LIVE</span>
    </div>
    <div id="tournament-list" class="empty">
      <div class="empty-icon">⏳</div>
      <h3>LOADING...</h3>
    </div>`,

  matches: `
    <div class="section-heading"><div><small>YOUR GAMES</small><h2>MY MATCHES</h2></div></div>
    <div class="empty"><div class="empty-icon">🎮</div><h3>NO MATCHES FOUND</h3></div>`,

  leaderboard: `
    <div class="section-heading"><div><small>TOP PLAYERS</small><h2>LEADERBOARD</h2></div></div>
    <div class="empty"><div class="empty-icon">📊</div><h3>RANKINGS COMING SOON</h3></div>`,

  profile: `
    <div class="section-heading"><div><small>PLAYER ACCOUNT</small><h2>MY PROFILE</h2></div></div>
    <div class="empty"><div class="empty-icon">👤</div><h3>PLAYER PROFILE</h3></div>`,

  admin: `
    <div class="section-heading"><div><small>CONTROL CENTER</small><h2>ADMIN PANEL</h2></div></div>
    <div class="empty">
      <div class="empty-icon">🛡️</div>
      <h3>ADMIN DASHBOARD</h3>
      <p>Admin tools will be activated after API hosting.</p>
    </div>`
};

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;",
    '"': "&quot;", "'": "&#39;"
  })[c]);
}

async function api(path, options = {}) {
  const initData = tg?.initData || "";

  return fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Telegram-Init-Data": initData,
      ...(options.headers || {})
    }
  });
}

async function loadTournaments() {
  const list = document.getElementById("tournament-list");
  if (!list) return;

  try {
    const response = await api("/tournaments");
    if (!response.ok) throw new Error("API unavailable");

    const tournaments = await response.json();

    if (!tournaments.length) {
      list.innerHTML = "<h3>NO TOURNAMENTS YET</h3><p>New tournaments will appear here.</p>";
      return;
    }

    list.className = "";
    list.innerHTML = tournaments.map(t => `
      <div class="empty">
        <h3>${escapeHTML(t.title)}</h3>
        <p>${escapeHTML(t.game)} · ${escapeHTML(t.mode)}</p>
        <p>Slots: ${Number(t.max_players)} · ${escapeHTML(t.status)}</p>
      </div>
    `).join("");
  } catch {
    list.innerHTML = "<h3>SERVER NOT CONNECTED</h3><p>Tournament data will appear when the API is online.</p>";
  }
}

async function checkAdmin() {
  const button = document.getElementById("adminNav");
  if (!tg?.initData) return;

  try {
    const response = await api("/me");
    if (!response.ok) return;

    const data = await response.json();
    isAdmin = data.is_admin === true;

    if (button && isAdmin) button.style.display = "flex";
  } catch {
    isAdmin = false;
  }
}

function navigate(page) {
  if (page === "admin" && !isAdmin) return;

  content.innerHTML = pages[page] || pages.tournaments;

  document.querySelectorAll(".bottom-nav button")
    .forEach(button => button.classList.remove("active"));

  const names = ["tournaments", "matches", "leaderboard", "profile", "admin"];
  const index = names.indexOf(page);

  if (index >= 0) {
    const buttons = document.querySelectorAll(".bottom-nav button");
    if (buttons[index]) buttons[index].classList.add("active");
  }

  if (page === "tournaments") loadTournaments();
}

checkAdmin().then(() => navigate("tournaments"));
