(function () {
  'use strict';

  var ASSET_BASE = 'assets/img/';
  var BACK_CARD = ASSET_BASE + 'back.jpg';
  var cardList = ['car', 'cycle', 'human', 'truc'];
  var cityPrefixes = {
    Charleroi: 'chr',
    Jambes: 'jmb',
    Bruxelles: 'bx',
    Beveren: 'bev',
    Courtrai: 'cou',
    Namur: 'nam',
    Liege: 'lie',
    Grobbendonk: 'gro',
    Herzele: 'her'
  };

  var errors = 0;
  var pairsFound = 0;
  var totalPairs = 0;
  var cardPairs = {};
  var cardSet = [];
  var board = [];
  var rows = 2;
  var columns = 4;
  var card1Selected = null;
  var card2Selected = null;
  var isLocked = false;
  var currentCity = '';

  function getBoardElement() {
    return document.getElementById('board');
  }

  function getVictoryElement() {
    return document.getElementById('victory');
  }

  function getMessageElement() {
    return document.getElementById('game-message');
  }

  function showMessage(text) {
    var message = getMessageElement();
    if (!message) {
      return;
    }
    message.textContent = text;
    message.hidden = !text;
  }

  function hideVictory() {
    var victory = getVictoryElement();
    if (victory) {
      victory.hidden = true;
    }
  }

  function showVictory() {
    var victory = getVictoryElement();
    if (victory) {
      victory.hidden = false;
    }
  }

  function updateErrorsDisplay() {
    var errorsElement = document.getElementById('errors');
    if (errorsElement) {
      errorsElement.textContent = String(errors);
    }
  }

  function updateCurrentCityDisplay(cityName) {
    var cityElement = document.getElementById('current-city');
    if (!cityElement) {
      return;
    }
    cityElement.textContent = 'Ville : ' + cityName;
    cityElement.hidden = false;
  }

  function setupCards(cityPrefix) {
    cardPairs = {};
    cardList.forEach(function (card) {
      cardPairs[card] = cityPrefix + '_' + card;
    });
  }

  function prepareCards(cityName) {
    var cityPrefix = cityPrefixes[cityName];
    setupCards(cityPrefix);
    cardSet = [];
    cardList.forEach(function (card) {
      cardSet.push(card);
      cardSet.push(cardPairs[card]);
    });
    totalPairs = cardList.length;
  }

  function shuffleCards() {
    for (var i = cardSet.length - 1; i > 0; i -= 1) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = cardSet[i];
      cardSet[i] = cardSet[j];
      cardSet[j] = temp;
    }
  }

  function clearBoard() {
    var boardElement = getBoardElement();
    if (boardElement) {
      boardElement.innerHTML = '';
    }
    board = [];
    card1Selected = null;
    card2Selected = null;
    isLocked = false;
  }

  function resetGameState() {
    errors = 0;
    pairsFound = 0;
    updateErrorsDisplay();
    hideVictory();
    showMessage('');
  }

  function cardImageSrc(cardName) {
    return ASSET_BASE + cardName + '.jpg';
  }

  function isCardHidden(cardElement) {
    return cardElement.src.endsWith('back.jpg');
  }

  function setCardHidden(cardElement) {
    cardElement.src = BACK_CARD;
    cardElement.setAttribute('aria-label', 'Carte face cachée');
  }

  function revealCard(cardElement, cardName) {
    cardElement.src = cardImageSrc(cardName);
    cardElement.setAttribute('aria-label', 'Carte ' + cardName.replace(/_/g, ' '));
  }

  function getCardNameFromElement(cardElement) {
    var parts = cardElement.id.split('-');
    return board[Number(parts[0])][Number(parts[1])];
  }

  function selectCard() {
    if (isLocked || !isCardHidden(this)) {
      return;
    }

    if (!card1Selected) {
      card1Selected = this;
      revealCard(card1Selected, getCardNameFromElement(card1Selected));
      return;
    }

    if (this === card1Selected || card2Selected) {
      return;
    }

    card2Selected = this;
    revealCard(card2Selected, getCardNameFromElement(card2Selected));
    isLocked = true;
    window.setTimeout(checkPair, 1000);
  }

  function getBaseNameFromSrc(src) {
    var match = src.match(/([^/]+)\.jpg$/);
    return match ? match[1] : '';
  }

  function isMatchingPair(name1, name2) {
    return cardPairs[name1] === name2 || cardPairs[name2] === name1;
  }

  function checkPair() {
    var baseName1 = getBaseNameFromSrc(card1Selected.src);
    var baseName2 = getBaseNameFromSrc(card2Selected.src);

    if (isMatchingPair(baseName1, baseName2)) {
      pairsFound += 1;
      card1Selected.setAttribute('aria-label', 'Paire trouvée');
      card2Selected.setAttribute('aria-label', 'Paire trouvée');
      if (pairsFound === totalPairs) {
        showVictory();
      }
    } else {
      setCardHidden(card1Selected);
      setCardHidden(card2Selected);
      errors += 1;
      updateErrorsDisplay();
    }

    card1Selected = null;
    card2Selected = null;
    isLocked = false;
  }

  function hideCards() {
    for (var r = 0; r < rows; r += 1) {
      for (var c = 0; c < columns; c += 1) {
        var cardElement = document.getElementById(r + '-' + c);
        if (cardElement) {
          setCardHidden(cardElement);
        }
      }
    }
    isLocked = false;
  }

  function createCardElement(row, column, cardName) {
    var card = document.createElement('img');
    card.id = row + '-' + column;
    card.src = cardImageSrc(cardName);
    card.className = 'card';
    card.alt = '';
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    card.setAttribute('aria-label', 'Carte ' + cardName.replace(/_/g, ' '));
    card.addEventListener('click', selectCard);
    card.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        selectCard.call(card);
      }
    });
    return card;
  }

  function renderBoard() {
    var boardElement = getBoardElement();
    if (!boardElement) {
      return;
    }

    for (var r = 0; r < rows; r += 1) {
      var row = [];
      for (var c = 0; c < columns; c += 1) {
        var cardName = cardSet.pop();
        row.push(cardName);
        boardElement.appendChild(createCardElement(r, c, cardName));
      }
      board.push(row);
    }

    isLocked = true;
    window.setTimeout(hideCards, 2000);
  }

  function startGame(cityName) {
    if (!cityPrefixes[cityName]) {
      showMessage('Veuillez choisir une ville valide.');
      return;
    }

    resetGameState();
    clearBoard();
    currentCity = cityName;
    updateCurrentCityDisplay(cityName);
    prepareCards(cityName);
    shuffleCards();
    renderBoard();
  }

  window.WAYBE_startGame = startGame;

  function bindControls() {
    var startButton = document.getElementById('start-game');
    var citySelect = document.getElementById('city-select');

    if (startButton && citySelect) {
      startButton.addEventListener('click', function () {
        startGame(citySelect.value);
      });
    }

    if (citySelect) {
      citySelect.addEventListener('change', function () {
        if (citySelect.value) {
          startGame(citySelect.value);
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindControls);
  } else {
    bindControls();
  }
})();
