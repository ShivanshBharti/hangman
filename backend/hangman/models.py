from django.db import models
import math

class Hangman(models.Model):
    WORDS = ["Hangman", "Python", "Audacix", "Bottle", "Pen"]
    word_to_guess = models.CharField(max_length=100)
    # there are 3 game states - "won", "lost", "in_progress" and default is "in_progress"
    game_state = models.CharField(max_length=100, default="IN_PROGRESS")
    current_word_state = models.CharField(max_length=100)
    incorrect_guesses = models.PositiveIntegerField(default=0)
    max_incorrect_guesses = models.PositiveIntegerField(default=6)

    def save(self, *args, **kwargs):
       self.max_incorrect_guesses = math.ceil(len(self.word_to_guess)/2)
       if not self.current_word_state:
           self.current_word_state = "_"*len(self.word_to_guess)
       super().save(*args, **kwargs)