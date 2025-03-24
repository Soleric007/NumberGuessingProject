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

    let attempts = 0;
    let maxAttempts = 10;
    let secretNumber;
    let lastDifference = null;
    let userId = null;  // Stores authenticated user ID

    // ✅ Check Authentication Before Game Starts
    await checkAuth();

    // ✅ Load saved theme from localStorage
    if (localStorage.getItem("theme") === "dark") {
        body.classList.remove("light-mode");
        body.classList.add("dark-mode");
        themeToggle.textContent = "☀️ Light Mode";
    }

    // ✅ Toggle Light/Dark Mode
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

    // ✅ Generate Random Number (GET from Backend)
    async function startGame() {
        try {
            const response = await fetch("/game/start-game", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const data = await response.json();
            secretNumber = data.secret_number;
            attempts = 0;
            lastDifference = null;
            attemptsDisplay.textContent = `${attempts} / ${maxAttempts}`;
            message.textContent = "🎉 New game started! Make a guess.";
            guessInput.value = "";
            guessInput.disabled = false;
            submitButton.disabled = false;
        } catch (error) {
            console.error("Error starting game:", error);
            message.textContent = "❌ Failed to start game!";
        }
    }
    
    document.getElementById("new-game").addEventListener("click", startGame);
    await startGame();

    submitButton.addEventListener("click", handleGuess);
    guessInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") handleGuess();
    });

    function handleGuess() {
        let guess = parseInt(guessInput.value);
        if (isNaN(guess) || guess < 1 || guess > 100) {
            message.textContent = "Enter a valid number (1-100)";
            return;
        }

        attempts++;
        attemptsDisplay.textContent = `${attempts} / ${maxAttempts}`;

        let feedback = guess > secretNumber ? "📉 Too high!" : "📈 Too low!";
        let difference = Math.abs(secretNumber - guess);

        if (lastDifference !== null) {
            if (difference < lastDifference) {
                feedback += " 🔥 Getting closer!";
                guessInput.style.borderColor = "green";
            } else if (difference > lastDifference) {
                feedback += " ❄️ Getting colder...";
                guessInput.style.borderColor = "red";
            } else {
                feedback += " 😐 Same distance...";
                guessInput.style.borderColor = "yellow";
            }
        }

        message.innerHTML = feedback;
        lastDifference = difference;
        errorSound.play();

        if (guess === secretNumber) {
            message.innerHTML = "🎉 <b>Correct!</b> You guessed it!";
            successSound.play();
            submitButton.disabled = true;
            confettiEffect();
            submitScore(attempts);
            setTimeout(askToRestart, 1500);
        } else if (attempts >= maxAttempts) {
            endGame();
        }
    }

    function endGame() {
        message.innerHTML = `💀 Game Over! The correct number was ${secretNumber}`;
        guessInput.disabled = true;
        submitButton.disabled = true;
        failSound.play();
        setTimeout(askToRestart, 1500);
    }

    function askToRestart() {
        let restart = confirm("Do you want to play again?");
        if (restart) {
            location.reload();
        } else {
            lockGame();
        }
    }

    function lockGame() {
        message.innerHTML += "<br>🔒 Game locked! Refresh to play again.";
        guessInput.disabled = true;
        submitButton.disabled = true;
    }

    function confettiEffect() {
        const confettiCanvas = document.createElement("canvas");
        document.body.appendChild(confettiCanvas);
        confettiCanvas.id = "confetti-canvas";
        confettiCanvas.style.position = "fixed";
        confettiCanvas.style.top = "0";
        confettiCanvas.style.left = "0";
        confettiCanvas.width = window.innerWidth;
        confettiCanvas.height = window.innerHeight;
        const confettiCtx = confettiCanvas.getContext("2d");
        let confetti = [];

        for (let i = 0; i < 100; i++) {
            confetti.push({
                x: Math.random() * confettiCanvas.width,
                y: Math.random() * confettiCanvas.height,
                r: Math.random() * 6 + 2,
                d: Math.random() * 10 + 2,
                color: `hsl(${Math.random() * 360}, 100%, 50%)`,
            });
        }

        function drawConfetti() {
            confettiCtx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
            confetti.forEach((c, i) => {
                confettiCtx.beginPath();
                confettiCtx.arc(c.x, c.y, c.r, 0, Math.PI * 2);
                confettiCtx.fillStyle = c.color;
                confettiCtx.fill();
                c.y += c.d;
                if (c.y > confettiCanvas.height) confetti[i] = { ...c, y: -10 };
            });
            requestAnimationFrame(drawConfetti);
        }

        drawConfetti();
        setTimeout(() => document.body.removeChild(confettiCanvas), 5000);
    }

    // ✅ Check User Authentication
    async function checkAuth() {
        try {
            const response = await fetch("/auth/check-auth", { credentials: "include" });
            const data = await response.json();

            if (data.user_id) {
                userId = data.user_id;
            } else {
                alert("You need to be logged in to play.");
                window.location.href = "/login";
            }
        } catch (error) {
            console.error("Error checking authentication:", error);
            alert("Authentication failed!");
            window.location.href = "/login";
        }
    }

    // ✅ Submit Score to Leaderboard
    async function submitScore(score) {
        try {
            const response = await fetch("/leaderboard/submit", {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, score }),
            });

            if (response.ok) {
                console.log("Score submitted successfully!");
            } else {
                console.error("Failed to submit score.");
            }
        } catch (error) {
            console.error("Error submitting score:", error);
        }
    }
});