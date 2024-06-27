import axios from 'axios';
import React, { useState } from 'react';

function NewGame({onNewGame}){
    const startNewGame = () => {
        axios.post('http://127.0.0.1:8000/hangman/game/new')
          .then(response => {
            onNewGame(response.data);
          })
          .catch(error => {
            console.error("There was an error starting a new game!", error);
          });
      };

      return (
        <div className="text-center">
          <button 
            className="bg-blue-500 text-white py-2 px-4 rounded"
            onClick={startNewGame}
          >
            Start New Game
          </button>
        </div>
      );
    
}

export default NewGame;