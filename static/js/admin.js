document.addEventListener("DOMContentLoaded", function () {
    loadDashboard();
    loadUsers();
    loadGames();
});

// 📌 Show Active Section
function showSection(section) {
    document.querySelectorAll(".admin-section").forEach(sec => sec.style.display = "none");
    document.getElementById(section).style.display = "block";
}

// 📌 Load Dashboard Stats
function loadDashboard() {
    fetch('/admin/users')
        .then(response => response.json())
        .then(data => {
            document.getElementById("totalUsers").textContent = data.length;
        });

    fetch('/admin/games')
        .then(response => response.json())
        .then(data => {
            document.getElementById("totalGames").textContent = data.length;
        });
}

// 📌 Load Users
function loadUsers() {
    fetch('/admin/users')
        .then(response => response.json())
        .then(data => {
            const usersTable = document.querySelector("#usersTable tbody");
            usersTable.innerHTML = "";
            data.forEach(user => {
                usersTable.innerHTML += `
                    <tr>
                        <td>${user.id}</td>
                        <td>${user.username}</td>
                        <td>${user.is_admin ? "Admin" : "User"}</td>
                        <td>
                            <button id="try" onclick="promoteUser(${user.id})">Promote</button>
                            <button id="try" onclick="deleteUser(${user.id})">Delete</button>
                        </td>
                    </tr>
                `;
            });
        })
        .catch(error => console.error("Error loading users:", error));
}

// 📌 Load Games
function loadGames() {
    fetch('/admin/games')
        .then(response => response.json())
        .then(data => {
            const gamesTable = document.querySelector("#gamesTable tbody");
            gamesTable.innerHTML = "";
            data.forEach(game => {
                gamesTable.innerHTML += `
                    <tr>
                        <td>${game.id}</td>
                        <td>${game.user_id}</td>
                        <td>${game.attempts}</td>
                        <td><button id="try" onclick="deleteGame(${game.id})">Delete</button></td>
                    </tr>
                `;
            });
        })
        .catch(error => console.error("Error loading games:", error));
}

// 📌 Promote User
function promoteUser(userId) {
    fetch(`/admin/promote/${userId}`, { method: "PATCH" })
        .then(response => response.json())
        .then(() => loadUsers())
        .catch(error => console.error("Error promoting user:", error));
}

// 📌 Delete User
function deleteUser(userId) {
    if (!confirm("Are you sure you want to delete this user?")) return;
    
    fetch(`/admin/delete-user/${userId}`, { method: "DELETE" })
        .then(response => response.json())
        .then(() => loadUsers())
        .catch(error => console.error("Error deleting user:", error));
}

// 📌 Delete Game
function deleteGame(gameId) {
    if (!confirm("Are you sure you want to delete this game?")) return;

    fetch(`/admin/delete-game/${gameId}`, {
        method: "DELETE",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(result => {
        alert(result.message);
        loadGames(); // Refresh game list
    })
    .catch(error => console.error("Error deleting game:", error));
}
document.addEventListener("DOMContentLoaded", function () {
    fetchAdminLeaderboard();
});

function fetchAdminLeaderboard() {
    fetch("/leaderboard/data")  // ✅ Match this with your Flask route
        .then(response => response.json())
        .then(data => {
            const leaderboardTable = document.getElementById("adminLeaderboardTable"); // Ensure this ID exists
            leaderboardTable.innerHTML = ""; // Clear previous data

            data.forEach((player, index) => {
                const row = `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${player.username}</td>
                        <td>${player.score}</td>
                    </tr>
                `;
                leaderboardTable.innerHTML += row;
            });
        })
        .catch(error => console.error("Error loading leaderboard:", error));
}
async function loadFeedback() {
    try {
        const response = await fetch("/admin/feedbacks");
        const feedbacks = await response.json();

        const tableBody = document.getElementById("feedbackTableBody");
        tableBody.innerHTML = ""; // ✅ Clear old data

        feedbacks.forEach(feedback => {
            const row = `
                <tr>
                    <td>${feedback.id}</td>
                    <td>${feedback.name}</td>
                    <td>${feedback.email}</td>
                    <td>${feedback.message}</td>
                    <td>${feedback.submitted_at}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error("Error loading feedback:", error);
    }
}

// ✅ Load Feedback when Admin Panel is Opened
document.addEventListener("DOMContentLoaded", loadFeedback);

