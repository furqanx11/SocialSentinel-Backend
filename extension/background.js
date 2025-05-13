// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//     if (message.type === "CHECK_TEXT") {
//       const { text } = message.payload;
  
//       fetch("http://127.0.0.1:5001/detect", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ text })
//       })
//         .then((res) => res.json())
//         .then((data) => {
//           sendResponse(data);
//         })
//         .catch((err) => {
//           console.error("[Extension] API call failed:", err);
//           sendResponse({ flagged: false });
//         });
  
//       return true; // keeps sendResponse alive for async
//     }
//   });
  
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "CHECK_TEXT") {
      chrome.storage.local.get("token", ({ token }) => {
        if (!token) {
          console.warn("User not logged in.");
          sendResponse({ flagged: false, reason: "Unauthorized" });
          return;
        }
  
        const { text, update } = message.payload;

        const url = `http://127.0.0.1:5001/detect?update=${update}`;
        fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify({ text })
        })
          .then((res) => res.json())
          .then((data) => sendResponse(data))
          .catch((err) => {
            console.error("[Extension] API call failed:", err);
            sendResponse({ flagged: false });
          });

      });
  
      return true; // keeps sendResponse alive for async
    }
  });

  chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension installed or updated.");
  });
  
  chrome.runtime.onStartup.addListener(() => {
    console.log("Extension background script restarted.");
  });
  