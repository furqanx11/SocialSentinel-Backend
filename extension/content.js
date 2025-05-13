// // Function to find the WhatsApp message input box
// function findWhatsAppInputBox() {
//     // WhatsApp Web selector for the message input div
//     // This selector might need updates if WhatsApp changes their structure
//     const inputSelectors = [
//       '[contenteditable="true"][data-tab="10"]', // Primary selector for message input
//       '.selectable-text[contenteditable="true"]', // Alternative selector
//       '[data-testid="conversation-compose-box-input"]', // Another possible selector
//     ];
  
//     for (const selector of inputSelectors) {
//       const element = document.querySelector(selector);
//       if (element) return element;
//     }
    
//     return null;
//   }
  
//   // Function to highlight problematic text
//   function highlightText(element, problematicTexts) {
//     // Add a visual indicator to the input box
//     element.style.boxShadow = "0 0 0 2px #ff6b6b";
    
//     // Create warning icon
//     const warningIcon = document.createElement('div');
//     warningIcon.innerHTML = '⚠️';
//     warningIcon.style.position = 'absolute';
//     warningIcon.style.right = '60px';
//     warningIcon.style.bottom = '15px';
//     warningIcon.style.fontSize = '20px';
//     warningIcon.style.zIndex = '1000';
//     warningIcon.style.cursor = 'pointer';
//     warningIcon.title = 'This message may contain abusive content';
    
//     // Insert the warning icon near the input
//     const footerElement = document.querySelector('footer');
//     if (footerElement) {
//       footerElement.style.position = 'relative';
//       footerElement.appendChild(warningIcon);
      
//       // Remove warning after 5 seconds
//       setTimeout(() => {
//         element.style.boxShadow = "";
//         if (warningIcon.parentNode) {
//           warningIcon.parentNode.removeChild(warningIcon);
//         }
//       }, 5000);
//     }
//   }
  
//   // Function to check text for abusive content
//   function checkForAbusiveContent(text, update = false) {
//     if (!text || text.trim() === '') return;
  
//     console.log("Checking text for abusive content:", text, " | update:", update);
  
//     chrome.runtime.sendMessage(
//       { type: "CHECK_TEXT", payload: { text, update } },
//       (response) => {
//         console.log("Received response from background script:", response);
//         if (chrome.runtime.lastError) {
//           console.warn("Runtime error:", chrome.runtime.lastError.message);
//           return;
//         }
//         if (response?.flagged && !update) { // Highlight only during typing
//           console.log("🚨 Flagged (typing):", response.reason, response.score);
//           const inputBox = findWhatsAppInputBox();
//           if (inputBox) {
//             highlightText(inputBox, [text]);
//           }
//         }
//       }
//     );
//   }
  

 
  

//   // Set up the mutation observer to watch for changes
//   function setupInputWatcher() {
//     let lastCheckedText = '';
//     let debounceTimer;
    
//     // Function to debounce the text checking
//     const debouncedCheck = (text) => {
//       clearTimeout(debounceTimer);
//       debounceTimer = setTimeout(() => {
//         if (text !== lastCheckedText && text.trim() !== '') {
//           console.log("Text changed, checking:", text);
//           lastCheckedText = text;
//           checkForAbusiveContent(text);
//         }
//       }, 1000); // Wait 1 second after typing stops
//     };
    
//     // Set up interval to periodically check for the input box
//     // (WhatsApp loads dynamically, so the element might not be available immediately)
//     const checkInterval = setInterval(() => {
//       const inputBox = findWhatsAppInputBox();
      
//       if (inputBox) {
//         console.log("WhatsApp input box found, setting up listeners");
//         clearInterval(checkInterval);
        
//         // Listen for input events
//         inputBox.addEventListener('input', () => {
//           debouncedCheck(inputBox.innerText);
//         });

//         inputBox.addEventListener('keydown', (e) => {
//           if (e.key === 'Enter' && !e.shiftKey) {
//             const text = inputBox.innerText.trim();
//             if (text) {
//               checkForAbusiveContent(text, true); // <- update=true
//             }
//           }
//         });
        
//         // Also add mutation observer as a backup
//         const observer = new MutationObserver((mutations) => {
//           const text = inputBox.innerText;
//           debouncedCheck(text);
//         });
        
//         observer.observe(inputBox, { 
//           characterData: true, 
//           childList: true, 
//           subtree: true 
//         });
//       }
//     }, 1000);
//   }
  
//   // Initialize the extension
//   console.log("Text Abuse Detector initialized for WhatsApp Web");
  
//   // Simple test to verify messaging works
//   setTimeout(() => {
//     console.log("Sending test message to background script");
//     chrome.runtime.sendMessage(
//       { type: "CHECK_TEXT", payload: { text: "This is a test message with hate speech" } },
//       (response) => {
//         console.log("Test message response:", response);
//       }
//     );
//   }, 5000);
  
//   setupInputWatcher();

// Function to find the WhatsApp message input box
function findWhatsAppInputBox() {
  const inputSelectors = [
    '[contenteditable="true"][data-tab="10"]',
    '.selectable-text[contenteditable="true"]',
    '[data-testid="conversation-compose-box-input"]',
  ];

  for (const selector of inputSelectors) {
    const element = document.querySelector(selector);
    if (element) return element;
  }

  return null;
}

// Function to highlight problematic text
function highlightText(element, problematicTexts) {
  element.style.boxShadow = "0 0 0 2px #ff6b6b";

  const warningIcon = document.createElement('div');
  warningIcon.innerHTML = '⚠️';
  warningIcon.style.position = 'absolute';
  warningIcon.style.right = '60px';
  warningIcon.style.bottom = '15px';
  warningIcon.style.fontSize = '20px';
  warningIcon.style.zIndex = '1000';
  warningIcon.style.cursor = 'pointer';
  warningIcon.title = 'This message may contain abusive content';

  const footerElement = document.querySelector('footer');
  if (footerElement) {
    footerElement.style.position = 'relative';
    footerElement.appendChild(warningIcon);

    setTimeout(() => {
      element.style.boxShadow = "";
      if (warningIcon.parentNode) {
        warningIcon.parentNode.removeChild(warningIcon);
      }
    }, 5000);
  }
}

// Function to check text for abusive content
function checkForAbusiveContent(text, update = false) {
  if (!text || text.trim() === '') return;

  console.log("Checking text for abusive content:", text, " | update:", update);

  chrome.runtime.sendMessage(
    { type: "CHECK_TEXT", payload: { text, update } },
    (response) => {
      if (chrome.runtime.lastError) {
        console.warn("Runtime error:", chrome.runtime.lastError.message);
        return;
      }

      console.log("Received response from background script:", response);

      if (response?.flagged && !update) {
        const inputBox = findWhatsAppInputBox();
        if (inputBox) {
          highlightText(inputBox, [text]);
        }
      }
    }
  );
}

// Set up input watcher
function setupInputWatcher() {
  let lastCheckedText = '';
  let debounceTimer;

  const debouncedCheck = (text) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      if (text !== lastCheckedText && text.trim() !== '') {
        lastCheckedText = text;
        checkForAbusiveContent(text);
      }
    }, 1000);
  };

  const checkInterval = setInterval(() => {
    const inputBox = findWhatsAppInputBox();

    if (inputBox) {
      console.log("WhatsApp input box found, setting up listeners");
      clearInterval(checkInterval);

      // Typing event
      inputBox.addEventListener('input', () => {
        debouncedCheck(inputBox.innerText);
      });

      // Sending event (Enter)
      inputBox.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          const text = inputBox.innerText.trim();
          if (text) {
            console.log("Sending message, triggering update check");
            checkForAbusiveContent(text, true); // update = true
          }
        }
      });

      // Optional MutationObserver
      const observer = new MutationObserver(() => {
        const text = inputBox.innerText;
        debouncedCheck(text);
      });

      observer.observe(inputBox, {
        characterData: true,
        childList: true,
        subtree: true
      });
    }
  }, 1000);
}

// Initialize
console.log("Text Abuse Detector initialized for WhatsApp Web");

setTimeout(() => {
  console.log("Sending test message to background script");
  chrome.runtime.sendMessage(
    { type: "CHECK_TEXT", payload: { text: "This is a test message with hate speech" } },
    (response) => {
      console.log("Test message response:", response);
    }
  );
}, 5000);

setupInputWatcher();
