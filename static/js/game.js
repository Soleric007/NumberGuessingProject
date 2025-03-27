document.addEventListener("DOMContentLoaded", async () => {
    const guessInput = document.getElementById("guess");
    const submitButton = document.getElementById("submit-guess");
    const message = document.getElementById("message");
    const attemptsDisplay = document.getElementById("attempts");
    const successSound = document.getElementById("success-sound");
    const errorSound = document.getElementById("error-sound");
    const failSound = document.getElementById("fail-sound");
    const themeToggle = document.getElementById("toggle-mode");
    const body = document.body;
    let gameId = null; 
    let attempts = 0;
    let maxAttempts = 10;
    let secretNumber;
    let lastDifference = null;
    let userId = null; 

    await checkAuth();

    if (localStorage.getItem("theme") === "dark") {
        body.classList.remove("light-mode");
        body.classList.add("dark-mode");
        themeToggle.textContent = "☀️ Light Mode";
    }

    themeToggle.addEventListener("click", () => {
        if (body.classList.contains("light-mode")) {
            body.classList.remove("light-mode");
            body.classList.add("dark-mode");
            localStorage.setItem("theme", "dark");
            themeToggle.textContent = "☀️ Light Mode";
        } else {
            body.classList.remove("dark-mode");
            body.classList.add("light-mode");
            localStorage.setItem("theme", "light");
            themeToggle.textContent = "🌙 Dark Mode";
        }
    });

    async function startGame(level = "low") {
        
    try {
        localStorage.setItem("difficulty", level);

        const response = await fetch("/game/start-game", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ level })
        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        gameId = data.game_id;
        maxAttempts = data.attempts_left;
        attempts = 0;
        attemptsDisplay.textContent = `${attempts} / ${maxAttempts}`;
        message.textContent = "🎉 New game started! Make a guess.";
        guessInput.value = "";
        guessInput.disabled = false;
        submitButton.disabled = false;

        const maxRanges = {
            low: 100,
            moderate: 999,
            expert: 9999
        };
        guessInput.max = maxRanges[level] || 100;
        guessInput.placeholder = `Enter a number (1-${guessInput.max})`; 
    } catch (error) {
        console.error("Error starting game:", error);
        message.textContent = "❌ Failed to start game!";
    }
}

// Add buttons for difficulty selection in game.html
document.getElementById("difficulty-low").addEventListener("click", () => startGame("low"));
document.getElementById("difficulty-moderate").addEventListener("click", () => startGame("moderate"));
document.getElementById("difficulty-expert").addEventListener("click", () => startGame("expert"));

    
    document.getElementById("new-game").addEventListener("click", startGame);
    await startGame();

    submitButton.addEventListener("click", handleGuess);
    guessInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") handleGuess();
    });

    async function handleGuess() {
        if (!gameId || submitButton.disabled) return;
    
        let guess = parseInt(guessInput.value);

                // ✅ Dynamically set validation based on difficulty
        const maxRanges = {
            low: 100,
            moderate: 999,
            expert: 9999
        };

        const currentMax = maxRanges[localStorage.getItem("difficulty")] || 100;

        if (isNaN(guess) || guess < 1 || guess > currentMax) {
            message.textContent = `Enter a valid number (1-${currentMax})`;
            return;
        }
    
        if (attempts >= maxAttempts) {
            endGame();
            return;
        }
    
        try {
            const response = await fetch(`/game/guess/${gameId}`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ guess }),
            });
    
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    
            const data = await response.json();
            console.log("Server Response:", data);
    
            let hintMessage = data.message ? data.message : (data.hint ? data.hint : "No hint provided");
            message.innerHTML = hintMessage;
    
            attempts = maxAttempts - (data.attempts_left ?? maxAttempts);
            attemptsDisplay.textContent = `${attempts} / ${maxAttempts}`;
    
            if (data.message && data.message.toLowerCase().includes("congratulations")) {
                message.innerHTML = "🎉 <b>Correct!</b> You guessed it!";
                successSound.play();  // ✅ Play success sound only on win
                submitButton.disabled = true;
                guessInput.disabled = true;
                confettiEffect();
                submitScore(attempts);
                setTimeout(askToRestart, 1500);
                return;
            }
    
            if (attempts >= maxAttempts) {
                setTimeout(endGame, 500);
                return;
            }
    
            let difference = Math.abs(secretNumber - guess);
            if (lastDifference !== null) {
                if (difference < lastDifference) {
                    message.innerHTML += " 🔥 Getting closer!";
                    guessInput.style.borderColor = "green";
                } else if (difference > lastDifference) {
                    message.innerHTML += " ❄️ Getting colder...";
                    guessInput.style.borderColor = "red";
                } else {
                    message.innerHTML += " 😐 Same distance...";
                    guessInput.style.borderColor = "yellow";
                }
            }
            lastDifference = difference;
            errorSound.play();  // ✅ Play only if the guess is wrong
    
        } catch (error) {
            console.error("Error making guess:", error);
            message.textContent = "❌ Failed to submit guess!";
        }
    }
    
    
    function endGame() {
        message.innerHTML = `💀 Game Over! The correct number was ${secretNumber}`;
        guessInput.disabled = true;
        submitButton.disabled = true;
        setTimeout(() => {
            failSound.play();
            askToRestart();
        }, 500);  // ✅ Delay so sound plays at the right time
    }
    

    async function askToRestart() {
        let restart = confirm("Do you want to play again?");
        if (restart) {
            await startGame();  // ✅ Ensure game restarts properly
        } else {
            lockGame();
        }
    }
    

    function lockGame() {
        message.innerHTML += "<br>🔒 Game locked! Refresh to play again.";
        guessInput.disabled = true;
        submitButton.disabled = true;
    }

    async function checkAuth() {
        try {
            const response = await fetch("/auth/check-auth", { credentials: "include" });
            const data = await response.json();
            if (data.user_id) {
                userId = data.user_id;
            } else {
                alert("You need to be logged in to play.");
                window.location.href = "/";
            }
        } catch (error) {
            console.error("Error checking authentication:", error);
            alert("Authentication failed!");
            window.location.href = "/";
        }
    }

    async function submitScore(score) {
        try {
            await fetch("/game/update-score", {  
                method: "POST",
                credentials: "include",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}` 
                },
                body: JSON.stringify({ score })
            });
        } catch (error) {
            console.error("Error submitting score:", error);
        }
    }
    
});
document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logout-btn");

    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("jwt");  // Remove JWT token
        sessionStorage.removeItem("jwt");
        window.location.href = "/";  // Redirect to login page
    });
});
function goToLeaderboard() {
    // Redirect to leaderboard page
    window.location.href = "/leaderboard";
}
function confettiEffect() {
    const duration = 2 * 1000; // 2 seconds
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 2000 };

    function randomInRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    const interval = setInterval(() => {
        const timeLeft = animationEnd - Date.now();

        if (timeLeft <= 0) {
            clearInterval(interval);
            return;
        }

        const particleCount = 50 * (timeLeft / duration);
        confetti({
            particleCount,
            angle: randomInRange(55, 125),
            spread: 70,
            origin: { y: 0.6 },
            ...defaults
        });
    }, 250);
}
