document.addEventListener("DOMContentLoaded", () => {
    const leaderboardTable = document.getElementById("leaderboardTable");
    const searchInput = document.getElementById("searchInput");
    const sortAscBtn = document.getElementById("sortAsc");
    const sortDescBtn = document.getElementById("sortDesc");

    let players = [];

    // Fetch leaderboard data
    async function fetchLeaderboard() {
        try {
            const response = await fetch("/leaderboard/data");
            players = await response.json();
            renderLeaderboard(players);
        } catch (error) {
            console.error("Error fetching leaderboard:", error);
        }
    }

    // Render leaderboard dynamically
    function renderLeaderboard(data) {
        leaderboardTable.innerHTML = ""; // Clear table

        data.forEach((player, index) => {
            const row = document.createElement("tr");

            // Assign rank colors
            let rankClass = "";
            if (index === 0) rankClass = "rank-1";
            else if (index === 1) rankClass = "rank-2";
            else if (index === 2) rankClass = "rank-3";

            row.innerHTML = `
                <td class="px-4 py-2 ${rankClass}">${index + 1}</td>
                <td class="px-4 py-2">${player.username}</td>
                <td class="px-4 py-2">${player.score}</td>
            `;
            leaderboardTable.appendChild(row);
        });
    }

    // Search functionality
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.toLowerCase();
        const filteredPlayers = players.filter(player => player.username.toLowerCase().includes(query));
        renderLeaderboard(filteredPlayers);
    });

    // Sort leaderboard (Ascending)
    sortAscBtn.addEventListener("click", () => {
        players.sort((a, b) => a.score - b.score);
        renderLeaderboard(players);
    });

    // Sort leaderboard (Descending)
    sortDescBtn.addEventListener("click", () => {
        players.sort((a, b) => b.score - a.score);
        renderLeaderboard(players);
    });

    // Auto-refresh leaderboard every 5 seconds
    setInterval(fetchLeaderboard, 5000);

    // Initial fetch
    fetchLeaderboard();
});
function goToGame() {
    window.location.href = "/game"; // Change URL if needed
}


document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logout-btn");

    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("jwt");  // Remove JWT token
        sessionStorage.removeItem("jwt");
        window.location.href = "/";  // Redirect to login page
    });
});
