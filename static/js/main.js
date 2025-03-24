document.addEventListener("DOMContentLoaded", () => {
    const toggleTheme = document.getElementById("toggleTheme");

    // 🌙 Theme Toggle
    toggleTheme.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
    });

    // Set initial theme
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark");
    }

    // 🚀 Check if user is logged in
    if (localStorage.getItem("token")) {
        window.location.href = "/game"; // Redirect to game page if already logged in
    }

    // Handle Login/Register Redirection
    document.querySelectorAll("a[href='/login'], a[href='/register']").forEach(button => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const isLogin = button.getAttribute("href") === "/login";
            openAuthModal(isLogin);
        });
    });
});

// 📝 Function to open Login/Register Modal
function openAuthModal(isLogin) {
    const authModal = document.createElement("div");
    authModal.innerHTML = `
        <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg w-80 text-center">
                <h2 class="text-xl font-bold">${isLogin ? "Login" : "Register"}</h2>
                <input type="text" id="username" placeholder="Username" class="mt-3 p-2 w-full border rounded">
                <input type="password" id="password" placeholder="Password" class="mt-3 p-2 w-full border rounded">
                <button id="authBtn" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded w-full">${isLogin ? "Login" : "Register"}</button>
                <p id="authError" class="text-red-500 mt-2 text-sm"></p>
                <button id="closeModal" class="mt-2 text-gray-500">Cancel</button>
            </div>
        </div>
    `;
    document.body.appendChild(authModal);

    // Close Modal
    document.getElementById("closeModal").addEventListener("click", () => authModal.remove());

    // Handle Login/Register
    document.getElementById("authBtn").addEventListener("click", async () => {
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();
        const authError = document.getElementById("authError");

        if (!username || !password) {
            authError.textContent = "Please enter both fields!";
            return;
        }

        const endpoint = isLogin ? "/login" : "/register";
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem("token", data.token); // Store JWT token
            window.location.href = "/game"; // Redirect to game page
        } else {
            authError.textContent = data.message || "Something went wrong!";
        }
    });
}
