document.addEventListener("DOMContentLoaded", () => {
    const feedbackForm = document.getElementById("feedback-form");

    feedbackForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const message = document.getElementById("message").value.trim();

        if (!name || !email || !message) {
            alert("Please fill in all fields.");
            return;
        }

        try {
            const response = await fetch("/feedback", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name, email, message }) // ✅ Ensure JSON format
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.success);
                feedbackForm.reset();
            } else {
                alert(result.error || "Something went wrong!");
            }
        } catch (error) {
            alert("Failed to submit feedback. Please try again.");
        }
    });
});

// ✅ Navigation Functions
function goHome() {
    window.location.href = "/";
}

function goLeaderboard() {
    window.location.href = "/leaderboard";
}

function goBackToGame() {
    window.location.href = "/game";
}
