document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");

    // 🚀 Handle Registration
    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value;
            const email = document.getElementById("email")?.value || ""; // Optional email field
            const password = document.getElementById("password").value;

            try {
                const response = await fetch("/auth/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, email, password }),
                });

                const data = await response.json();
                if (response.ok) {
                    alert("Registration successful! Redirecting to login...");
                    window.location.href = "/login.html"; // Redirect to login page
                } else {
                    alert(data.error || "Registration failed. Try again.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    }

    // 🔑 Handle Login
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("loginUsername").value;
            const password = document.getElementById("loginPassword").value;

            try {
                const response = await fetch("/auth/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password }),
                });

                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem("token", data.token); // Store JWT token
                    alert("Login successful! Redirecting to game...");
                    window.location.href = "/game.html"; // Redirect to game page
                } else {
                    alert(data.error || "Login failed. Check credentials.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    }
});
