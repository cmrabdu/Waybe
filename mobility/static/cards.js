var errors = 0; // Compteur d'erreurs
var cardList = [
    "car",
    "truc",
    "cycle",
    "human"
];

// Dictionnaire pour associer chaque carte à son double spécifique
var cardPairs = {
    "car": "number_car",
    "truc": "number_truc",
    "cycle": "number_cycle",
    "human": "number_human"
};

var cardSet;
var board = [];
var rows = 4; // Nombre de lignes du plateau
var columns = 2; // Nombre de colonnes du plateau

var card1Selected;
var card2Selected;

window.onload = function() {
    prepareCards();
    shuffleCards();
    startGame();
}

// Préparation des paires de cartes
function prepareCards() {
    cardSet = [];
    for (let card of cardList) {
        cardSet.push(card);
        cardSet.push(cardPairs[card]); // Ajoute le double spécifique de chaque carte
    }
}

// Fonction pour mélanger les cartes
function shuffleCards() {
    for (let i = cardSet.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        let temp = cardSet[i];
        cardSet[i] = cardSet[j];
        cardSet[j] = temp;
    }
    console.log(cardSet);
}

// Fonction pour démarrer le jeu
function startGame() {
    for (let r = 0; r < rows; r++) {
        let row = [];
        for (let c = 0; c < columns; c++) {
            let card = document.createElement("img");
            let cardImg = cardSet.pop();
            row.push(cardImg);
            card.id = r.toString() + "-" + c.toString();
            card.src = "back.jpg";
            card.classList.add("card");
            card.addEventListener("click", selectCard);
            document.getElementById("board").append(card);
        }
        board.push(row);
    }
    console.log(board);
    setTimeout(hideCards, 2000);
}

// Fonction pour cacher les cartes après un temps initial
function hideCards() {
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < columns; c++) {
            let card = document.getElementById(r.toString() + "-" + c.toString());
            card.src = "back.jpg";
        }
    }
}

// Fonction pour gérer les sélections de cartes
function selectCard() {
    if (this.src.includes("back")) {
        if (!card1Selected) {
            card1Selected = this;
            let coords = card1Selected.id.split("-");
            let r = parseInt(coords[0]);
            let c = parseInt(coords[1]);
            card1Selected.src = board[r][c] + ".jpg";
        } else if (!card2Selected && this !== card1Selected) {
            card2Selected = this;
            let coords = card2Selected.id.split("-");
            let r = parseInt(coords[0]);
            let c = parseInt(coords[1]);
            card2Selected.src = board[r][c] + ".jpg";
            setTimeout(update, 1000);
        }
    }
}

// Fonction pour vérifier si les deux cartes sélectionnées sont des doubles spécifiques
function update() {
    // Extraire les noms de base des images en enlevant le chemin et l'extension
    let baseName1 = card1Selected.src.replace(/^.*[\\\/]/, '').replace(/\..+$/, '');
    let baseName2 = card2Selected.src.replace(/^.*[\\\/]/, '').replace(/\..+$/, '');

    // Vérifie si l'une est le double de l'autre en utilisant le dictionnaire cardPairs
    if (!(cardPairs[baseName1] === baseName2 || cardPairs[baseName2] === baseName1)) {
        card1Selected.src = "back.jpg";
        card2Selected.src = "back.jpg";
        errors += 1;
        document.getElementById("errors").innerText = errors; // Met à jour le compteur d'erreurs
    } else {
        // Optionnel : Ajouter une rétroaction positive ici si la paire est correcte
    }

    // Réinitialiser les sélections pour permettre de nouvelles sélections
    card1Selected = null;
    card2Selected = null;
}

