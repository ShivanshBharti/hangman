import React, { useState } from 'react';
import './App.css';
import NewGame from './components/NewGame';
import GameState from './components/GameState';

function App() {
    const [currentGameId, setCurrentGameId] = useState(null);

    const handleNewGame = (game) => {
        setCurrentGameId(game.id);
    };

    const startNewGame = () => {
        setCurrentGameId(null);
    };

    return (
        <div className="container mx-auto">
            <h1 className="text-4xl text-center my-4">Hangman Game</h1>
            {currentGameId ? (
                <GameState gameId={currentGameId} onNewGame={startNewGame} />
            ) : (
                <NewGame onNewGame={handleNewGame} />
            )}
        </div>
    );
}

export default App;
