const tableBody = document.querySelector("table"); 

// Ensure the element was found before adding the listener
if (tableBody) {
    tableBody.addEventListener("click", (e) => {
        if (e.target.classList.contains("show-password")) {
            const btn = e.target;
            const span = btn.previousElementSibling;
            
            if (!span) return;

            if (span.textContent === "••••••••") {
                span.textContent = btn.dataset.password;
                btn.textContent = "Hide";
            } else {
                span.textContent = "••••••••";
                btn.textContent = "Show";
            }
        }
    });
} else {
    console.error("Error: Table element not found.");
}
