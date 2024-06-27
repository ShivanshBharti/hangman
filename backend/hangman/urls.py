from django.urls import path
from .views import *

urlpatterns = [
    path('game/new',StartNewGame.as_view(),name="start_new_game"),
    path('game/<int:id>',GameState.as_view(),name="game_state"), 
    path('game/<int:id>/guess',GuessWord.as_view(),name="guess_word"),
    path('games/all',AllHangmanGames.as_view(),name="all_hangman_games"),
]