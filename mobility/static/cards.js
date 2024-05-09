var errors = 0; // Compteur d'erreurs
var pairsFound = 0; // Compteur de paires trouvées
var totalPairs; // Nombre total de paires à trouver

var cardList = ["car", "cycle", "human", "truc"]; // Cartes disponibles
var cardPairs = {}; // Paires de cartes
var cardSet; // Ensemble de cartes pour le jeu
var board = []; // Tableau de jeu
var rows = 2; // Nombre de lignes du plateau
var columns = 4; // Nombre de colonnes du plateau

var card1Selected; // Première carte sélectionnée
var card2Selected; // Deuxième carte sélectionnée

window.onload = function() {
    prepareCards();
    shuffleCards();
    startGame();
}

function setupCards(cityPrefix) {
    cardPairs = {};
    cardList.forEach(card => {
        cardPairs[card] = `${cityPrefix}_${card}`;
    });
}

function prepareCards() {
    const cityPrefixes = {
        "Charleroi": "chr",
        "Jambes": "jmb",
        "Bruxelles": "bx",
        "Beveren": "bev",
        "Courtrait": "cou",
        "Namur": "nam",
        "Liege": "lie",
        "Grobbendonk": "gro",
        "Herzel": "her"
    };
    setupCards(cityPrefixes[chosenCity] || "chr");
    cardSet = [];
    cardList.forEach(card => {
        cardSet.push(card);
        cardSet.push(cardPairs[card]);
    });
    totalPairs = cardList.length; // Mise à jour du total des paires
}

function shuffleCards() {
    for (let i = cardSet.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [cardSet[i], cardSet[j]] = [cardSet[j], cardSet[i]];
    }
    console.log(cardSet);
}

function startGame() {
    for (let r = 0; r < rows; r++) {
        let row = [];
        for (let c = 0; c < columns; c++) {
            let card = document.createElement("img");
            let cardImg = cardSet.pop();
            row.push(cardImg);
            card.id = `${r}-${c}`;
            card.src = "../static/back.jpg";
            card.classList.add("card");
            card.addEventListener("click", selectCard);
            document.getElementById("board").appendChild(card);
        }
        board.push(row);
    }
    console.log(board);
    setTimeout(hideCards, 2000);
}

function hideCards() {
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < columns; c++) {
            document.getElementById(`${r}-${c}`).src = "../static/back.jpg";
        }
    }
}

function selectCard() {
    if (this.src.includes("back")) {
        if (!card1Selected) {
            card1Selected = this;
            let [r, c] = card1Selected.id.split("-");
            card1Selected.src = `../static/${board[r][c]}.jpg`;
        } else if (!card2Selected && this !== card1Selected) {
            card2Selected = this;
            let [r, c] = card2Selected.id.split("-");
            card2Selected.src = `../static/${board[r][c]}.jpg`;
            setTimeout(checkPair, 1000);
        }
    }
}

function checkPair() {
    let baseName1 = card1Selected.src.match(/([^\/]+)\.jpg$/)[1];
    let baseName2 = card2Selected.src.match(/([^\/]+)\.jpg$/)[1];

    if (cardPairs[baseName1] === baseName2 || cardPairs[baseName2] === baseName1) {
        pairsFound += 1;
        if (pairsFound === totalPairs) {
            displayCongratulations();
        }
    } else {
        card1Selected.src = "../static/back.jpg";
        card2Selected.src = "../static/back.jpg";
        errors += 1;
        document.getElementById("errors").innerText = errors;
    }
    card1Selected = null;
    card2Selected = null;
}

function displayCongratulations() {
    alert("Bien joué ! Vous avez trouvé toutes les paires. Nous vous invitons a aller voir Request pour avoir plus d'info sur vôtre ville ! ");
}
