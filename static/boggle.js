"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  $table.append("<tbody>");

  for (let row = 0; row < board.length; row++) {
    const $row = $("<tr>", { id: `row-${row}` });
    $("tbody").append($row);

    for (let col = 0; col < board[row].length; col++) {
      const $letter = $("<td>", { text: board[row][col] });
      $row.append($letter);
    }
  }
}



async function handleWordForm(evt) {
  evt.preventDefault();
  const word = $wordInput.val().toUpperCase();

  const checkResult = await checkIfValidWord(word);
  if (checkResult.result !== 'ok') {
    $('.msg').text(checkResult.result);
  } else if (checkResult.result === 'ok') {
    const $wordLi = $('<li>');
    $wordLi.text(word);
    $('#words').append($wordLi);
  }
}



async function checkIfValidWord(word) {
  const response = await fetch(`/api/score-word`, {
    method: "POST",
    body: JSON.stringify({ word, gameId }),
    headers: {
      "Content-Type": "application/json"
    }
  });
  return await response.json();
}

$form.on("submit", handleWordForm);





start();