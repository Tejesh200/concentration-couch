let lastUrl = "";

async function checkCurrentTab() {
    try {
        // Get the active tab in the current window
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab || !tab.url) return;

        // Skip if URL hasn't changed
        if (tab.url === lastUrl) return;
        lastUrl = tab.url;

        // Send URL + title to backend
        let response = await fetch("http://127.0.0.1:8000/classify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: tab.url, title: tab.title || "" })
        });

        let result = await response.json();
        console.log("Prediction:", result);

        // Close tab if classified as distractive
        if (result.classification && result.classification.toLowerCase().includes("distract")) {
           chrome.tabs.remove(tab.id);}


    } catch (err) {
        console.error("Error contacting backend:", err);
    }
}

// Run check every 5 seconds
setInterval(checkCurrentTab, 5000);

