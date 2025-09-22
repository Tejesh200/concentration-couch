let lastUrl = "";

async function checkCurrentTab(force = false) {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab || !tab.url) return;

        // ✅ Get focus session end time
        const data = await new Promise(resolve => {
            chrome.storage.local.get("focusEnd", resolve);
        });
        const focusEnd = data.focusEnd;

        if (!focusEnd || Date.now() > focusEnd) return; // no active session

        if (!force && tab.url === lastUrl) return;
        lastUrl = tab.url;

        // ✅ Step 1: Blacklist check
        const blacklist = [
            "youtube.com",
            "instagram.com",
            "facebook.com",
            "twitter.com",
            "tiktok.com",
            "reddit.com",
            "netflix.com/in/",
            "primevideo.com",
            "hotstar.com",
            "discord.com",
            "pinterest.com"
        ];

        if (blacklist.some(site => tab.url.includes(site))) {
            console.log("🚫 Blacklisted site — blocking:", tab.url);
            chrome.tabs.update(tab.id, { url: chrome.runtime.getURL("blocked.html") });
            return; // skip backend
        }

        // ✅ Step 2: ML model check
        let response;
        try {
            response = await fetch("http://localhost:8000/classify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: tab.url, title: tab.title || "" })
            });
        } catch (netErr) {
            console.error("❌ Network error while calling backend:", netErr);
            return;
        }

        console.log("✅ Fetch completed. Status:", response.status);

        let result;
        try {
            result = await response.json();
        } catch (jsonErr) {
            console.error("❌ Failed to parse JSON:", jsonErr);
            const text = await response.text();
            console.error("Raw backend response:", text);
            return;
        }

        const cls = (result.classification || "").toLowerCase();
        console.log("🔎 Classification result for", tab.url, "=>", cls);

        if (cls === "distractive" || cls === "distracting") {
            console.log("🚫 Blocking tab via ML:", tab.url);
            chrome.tabs.update(tab.id, { url: chrome.runtime.getURL("blocked.html") });
        } else {
            console.log("✅ Allowed tab:", tab.url);
        }

    } catch (err) {
        console.error("🔥 Unexpected error in checkCurrentTab:", err);
    }
}

setInterval(checkCurrentTab, 5000);

// ✅ Handle popup -> background message
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "checkNow") {
        checkCurrentTab(true); // force immediate check
        sendResponse({ status: "ok" });
    }
});
