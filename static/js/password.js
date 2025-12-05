

tableBody.addEventListener("click", (e) => {
  if (e.target.classList.contains("show-password")) {
    const btn = e.target;
    const span = btn.previousElementSibling;
    if (!span) return;

    if (span.textContent === "••••••••") {
      span.textContent = btn.dataset.password; // reveal
      btn.textContent = "Hide";
    } else {
      span.textContent = "••••••••"; // hide
      btn.textContent = "Show";
    }
  }
});

