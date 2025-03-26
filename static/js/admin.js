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
                            <button onclick="promoteUser(${user.id})">Promote</button>
                            <button onclick="deleteUser(${user.id})">Delete</button>
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
                        <td><button onclick="deleteGame(${game.id})">Delete</button></td>
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
