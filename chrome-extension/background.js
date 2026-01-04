function getDomain(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return "unknown";
  }
}

function logActiveTabs() {
  chrome.tabs.query({}, (tabs) => {
    console.clear();
    console.log("Active Websites:");

    tabs.forEach(tab => {
      console.log(
        `• ${tab.title} (${getDomain(tab.url)})`
      );
    });
  });
}

// 🔹 Trigger when extension loads
chrome.runtime.onInstalled.addListener(() => {
  console.log("Interview Transparency Monitor installed");
  logActiveTabs();
});

// 🔹 Trigger when a tab becomes active
chrome.tabs.onActivated.addListener(() => {
  logActiveTabs();
});

// 🔹 Trigger when tab URL or title changes
chrome.tabs.onUpdated.addListener(() => {
  logActiveTabs();
});

// 🔹 Trigger when a tab is closed
chrome.tabs.onRemoved.addListener(() => {
  logActiveTabs();
});
