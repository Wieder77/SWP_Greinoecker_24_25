let score = 0;
let highscore = 0;
let time = 0;
let game = {
    canvas: document.getElementById("field"),
    start() {
        console.log(this.canvas);
        this.context = this.canvas.getContext("2d");
        this.clear();
        this.interval = setInterval(redraw, 20);              // Redraw every 20ms (50 FPS)
        if (!this.intervalTime) {                             // Only start the timer if it hasn't started yet
            this.intervalTime = setInterval(updateTime, 1000); // Increment time every second
        }
        this.intervalNewEnemy = setInterval(newEnemy, 600);    // Spawn new enemy every 600ms
        this.player = new sprite("player", 30, 30, "red", 10, 120);
        this.enemies = [];
        this.bonus = [];
        this.keyCode = -1;
        window.addEventListener('keydown', (e) => {
            this.keyCode = e.keyCode;
        });
        window.addEventListener('keyup', (e) => {
            this.keyCode = -1;
        });
    },
    clear() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
};

function start() {
    console.log("Game started");
    game.start();
    newBonus(10); // Start with 10 bonuses
}

function resetGame() {
    clearInterval(game.interval);          // Stop the redraw interval
    clearInterval(game.intervalNewEnemy);  // Stop spawning enemies
    clearInterval(game.intervalTime);      // Stop the time counter

    // Reset key variables
    score = 0;
    time = 0;
    game.enemies = [];
    game.bonus = [];
    updateScoreDisplay();                  // Reset score display
    document.getElementById("time").innerText = "Time: " + time; // Reset time display

    // Start the game again
    start();
}

function sprite(id, width, height, color, x, y) {
    this.width = width;
    this.height = height;
    this.x = x;
    this.y = y;
    let img = document.getElementById(id);
    ctx = game.context;

    this.redraw = function() {
        if (img.complete) {
            ctx.drawImage(img, this.x, this.y, this.width, this.height);
        } else {
            img.onload = () => {
                ctx.drawImage(img, this.x, this.y, this.width, this.height);
            };
        }
    };
    this.redraw();
}

function checkCollision(player, enemy) {
    if (player.x < enemy.x + enemy.width &&
        player.x + player.width > enemy.x &&
        player.y < enemy.y + enemy.height &&
        player.y + player.height > enemy.y) {
        alert("Game over");
        resetGame();  // Reset the game after collision
    }
}

function bonusEaten(player, bonus) {
    if (player.x < bonus.x + bonus.width &&
        player.x + player.width > bonus.x &&
        player.y < bonus.y + bonus.height &&
        player.y + player.height > bonus.y) {
        console.log("You won");
        score++;
        newBonus(1);
        updateScoreDisplay();
        const index = game.bonus.indexOf(bonus);
        if (index > -1) {
            game.bonus.splice(index, 1); // Remove the collected bonus
        }
    }
}

function redraw() {
    game.clear();
    switch (game.keyCode) {
        case 37: // Left
            game.player.x -= 2;
            break;
        case 38: // Up
            game.player.y -= 2;
            break;
        case 39: // Right
            game.player.x += 2;
            break;
        case 40: // Down
            game.player.y += 2;
            break;
    }

    game.player.redraw();
    game.bonus.forEach((b) => {
        b.redraw();
        bonusEaten(game.player, b); // Check if player collects bonus
    });
    game.enemies.forEach((e) => {
        let yDelta = Math.floor(Math.random() * 11) - 5;
        e.x -= 1;
        e.y += yDelta;
        e.redraw();
        checkCollision(game.player, e); // Check for collision with enemy
    });
}

function newEnemy() {
    let y = Math.floor(Math.random() * 1024);
    e = new sprite("enemy", 30, 30, "blue", 1000, y);
    game.enemies.push(e);
}

function newBonus(bonus_count) {
    for (var i = 0; i < bonus_count; i++) {
        let y = Math.floor(Math.random() * game.canvas.height);
        let x = Math.floor(Math.random() * game.canvas.width);
        let b = new sprite("bonus", 40, 40, "blue", x, y);
        game.bonus.push(b);
    }
}

function updateTime() {
    time++;
    document.getElementById("time").innerText = "Time: " + time;
}

function updateScoreDisplay() {
    if (highscore <= score) {
        highscore = score;
    }
    document.getElementById("score").innerText = "Score: " + score;
    document.getElementById("highscore").innerText = "Highscore: " + highscore;
}
