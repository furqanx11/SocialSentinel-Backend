// document.getElementById("loginBtn").addEventListener("click", async () => {
//   const email = document.getElementById("email").value;
//   const password = document.getElementById("password").value;

//   try {
//     console.log("Attempting to log in with email:", email, "and password:", password);
//     const res = await fetch("http://127.0.0.1:5001/auth/login", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ email, password })
//     });

//     const data = await res.json();
//     console.log("Login response:", data);

//     if (res.ok && data.status_code === 200 && data.data) {
//       chrome.storage.local.set({ token: data.data }, () => {
//         document.getElementById("msg").innerText = "✅ " + data.message;
//       });
//     } else {
//       document.getElementById("msg").innerText = "❌ Login failed: " + (data.message || "Unknown error");
//     }
//   } catch (error) {
//     document.getElementById("msg").innerText = "❌ Login failed: Network error";
//   }
// });

document.getElementById("loginBtn").addEventListener("click", async () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const messageBox = document.getElementById("message");

  try {
    const response = await fetch("http://127.0.0.1:5001/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      messageBox.textContent = data.detail || "Login failed";
    } else {
      messageBox.style.color = "green";
      messageBox.textContent = "Login successful!";
      chrome.storage.local.set({ token: data.data });
      chrome.tabs.create({ url: "http://localhost:3000/" }); // store token for later use
    }
  } catch (err) {
    messageBox.textContent = "API error!";
    console.error(err);
  }
});
