let interval = null;

function startTimer(endTime) {
    const timerEl = document.getElementById("timer");

    function updateTimer() {
        const now = Date.now();
        const remaining = endTime - now;

        if (remaining <= 0) {
            clearInterval(interval);
            interval = null;
            timerEl.textContent = "00:00";
            chrome.storage.local.remove("focusEnd");
        } else {
            const mins = Math.floor(remaining / 60000);
            const secs = Math.floor((remaining % 60000) / 1000);
            timerEl.textContent = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
        }
    }

    if (interval) clearInterval(interval); // avoid multiple intervals
    updateTimer(); 
    interval = setInterval(updateTimer, 1000);
}

// Start button
document.getElementById("startBtn").addEventListener("click", () => {
    const endTime = Date.now() + 25 * 60 * 1000; // 25 minutes
    chrome.storage.local.set({ focusEnd: endTime }, () => {
        startTimer(endTime);

        // 👉 Tell background to check active tab immediately
        chrome.runtime.sendMessage({ action: "checkNow" });
    });
});

// ✅ Stop button
document.getElementById("stopBtn").addEventListener("click", () => {
    if (interval) clearInterval(interval);
    interval = null;
    document.getElementById("timer").textContent = "25:00";
    chrome.storage.local.remove("focusEnd");
});

// Resume if session already active
chrome.storage.local.get("focusEnd", (data) => {
    if (data.focusEnd && Date.now() < data.focusEnd) {
        startTimer(data.focusEnd);
    }
});
