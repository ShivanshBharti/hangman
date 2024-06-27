import axios from "axios";
import React, { useState, useEffect } from "react";

function GameState({ gameId, onNewGame }) {
    const [gameState, setGameState] = useState(null);

    useEffect(() => {
        axios.get(`http://127.0.0.1:8000/hangman/game/${gameId}`)
            .then(response => {
                setGameState(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the game state!", error);
            });
    }, [gameId]);

    const makeGuess = (guess) => {
        axios.put(`http://127.0.0.1:8000/hangman/game/${gameId}/guess`, { guess: guess })
            .then(response => {
                setGameState(response.data);
            })
            .catch(error => {
                console.error("There was an error making a guess!", error);
            });
    };

    if (!gameState) {
        return <div>Loading...</div>;
    }

    if (gameState.game_state === "WON" || gameState.game_state === "LOST") {
        return (
            <div className="text-center">
                {gameState.game_state === "WON" && <p>Congratulations! You won!</p>}
                {gameState.game_state === "LOST" && <p>Game over! The word was {gameState.correct_word}</p>}
                <button onClick={onNewGame} className="bg-blue-500 text-white py-2 px-4 rounded">Back to Home!</button>
            </div>
        );
    }
    const formatted_word_state = gameState.current_word_state.split('').join(' ');

    return (
        <div className="text-center">
            <p>Word to guess: {formatted_word_state}</p>
            <p>Word length: {gameState.word_to_guess_length}</p>
            <p>Incorrect guesses: {gameState.incorrect_guesses}</p>
            <p>Remaining guesses: {gameState.max_incorrect_guesses - gameState.incorrect_guesses}</p>
            <GuessForm onSubmit={makeGuess} />
        </div>
    );
}

function GuessForm({ onSubmit }) {
    const [guess, setGuess] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        if (guess.length === 1) {
            onSubmit(guess);
            setGuess('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="my-4">
            <input
                type="text"
                maxLength="1"
                value={guess}
                onChange={(e) => setGuess(e.target.value)}
                className="border p-2"
            />
            <button type="submit" className="bg-green-500 text-white py-2 px-4 rounded ml-2">
                Guess
            </button>
        </form>
    );
}

export default GameState;
