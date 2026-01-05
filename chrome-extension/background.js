const WS_URL = "ws://localhost:8765";
let socket = null;

// 🔹 Open (or reopen) WebSocket
function connectWebSocket() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    return;
  }

  socket = new WebSocket(WS_URL);

  socket.onopen = () => {
    console.log("✅ Connected to Python WebSocket server");
    sendTabs(); // send immediately on connect
  };

  socket.onerror = (err) => {
    console.error("❌ WebSocket error", err);
  };

  socket.onclose = () => {
    console.warn("⚠ WebSocket closed. Reconnecting...");
    socket = null;
  };
}

// 🔹 Extract domain safely
function getDomain(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return "unknown";
  }
}

// 🔹 Collect all tab titles
function sendTabs() {
  chrome.tabs.query({}, (tabs) => {
    const titles = tabs.map(tab => tab.title).filter(Boolean);

    const payload = {
      browser: "Chrome",
      tabs: titles
    };

    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(payload));
      console.log("📤 Sent tabs to desktop app:", payload);
    }
  });
}

/* =====================
   EVENT TRIGGERS
   ===================== */

// When extension installs / reloads
chrome.runtime.onInstalled.addListener(() => {
  connectWebSocket();
});

// When user switches tabs
chrome.tabs.onActivated.addListener(() => {
  connectWebSocket();
  sendTabs();
});

// When tab URL or title changes
chrome.tabs.onUpdated.addListener(() => {
  connectWebSocket();
  sendTabs();
});

// When tab closes
chrome.tabs.onRemoved.addListener(() => {
  connectWebSocket();
  sendTabs();
});