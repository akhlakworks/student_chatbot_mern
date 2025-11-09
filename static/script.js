const chatBox = document.getElementById("chat-box");
const loginModal = document.getElementById("login-modal");
const signupModal = document.getElementById("signup-modal");

document.getElementById("show-login")?.addEventListener("click", () => {
  loginModal.style.display = "flex";
});

document.getElementById("show-signup")?.addEventListener("click", () => {
  signupModal.style.display = "flex";
});

document.getElementById("goto-signup")?.addEventListener("click", () => {
  loginModal.style.display = "none";
  signupModal.style.display = "flex";
});

document.getElementById("goto-login")?.addEventListener("click", () => {
  signupModal.style.display = "none";
  loginModal.style.display = "flex";
});

document.getElementById("logout-btn")?.addEventListener("click", () => {
  window.location.href = "/logout";
});

async function login() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;
  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  alert(data.message);
  if (data.status === "success") location.reload();
}

async function signup() {
  const username = document.getElementById("signup-username").value;
  const password = document.getElementById("signup-password").value;
  const res = await fetch("/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  alert(data.message);
  if (data.status === "success") location.reload();
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;
  chatBox.innerHTML += `<div class="user">${message}</div>`;
  input.value = "";

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  const data = await res.json();
  chatBox.innerHTML += `<div class="bot">${data.reply}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}
