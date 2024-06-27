from django.shortcuts import render
import math
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .models import *
from .serializers import *


class AllHangmanGames(generics.ListAPIView):
    serializer_class = HangmanGameSerializer

    def get_queryset(self):
        queryset = Hangman.objects.all()
        return queryset
    
class GetInProgessGameCount(APIView):
    def get(self,request):
        in_progress_games = Hangman.objects.filter(game_state="IN_PROGRESS").count()
        return Response({"in_progress_games":in_progress_games.count()},status=status.HTTP_200_OK)
    

class StartNewGame(generics.CreateAPIView):
    queryset = Hangman.objects.all()
    serializer_class = HangmanGameSerializer

    def create(self,request,*args,**kwargs):
        word_to_guess = random.choice(Hangman.WORDS)
        max_incorrect_guesses = math.ceil(len(word_to_guess)/2)

        game = Hangman(
            word_to_guess = word_to_guess,
            max_incorrect_guesses = max_incorrect_guesses,
            current_word_state = "_"*len(word_to_guess),
            incorrect_guesses = 0,
            game_state = "IN_PROGRESS"
        )

        game.save()

        serializer = self.get_serializer(game)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class GameState(generics.RetrieveAPIView):
    queryset = Hangman.objects.all()
    serializer_class = HangmanGameSerializer
    lookup_field = "id"

    def retrieve(self,request,*args,**kwargs):
        instance = self.get_object()
        rem_incorrect_guesses = instance.max_incorrect_guesses - instance.incorrect_guesses
        serializer = self.get_serializer(instance)
        response = serializer.data
        response["word_to_guess_length"] = len(instance.word_to_guess)
        response["remaining_incorrect_guesses"] = rem_incorrect_guesses

        return Response(response,status=status.HTTP_200_OK)
    
class GuessWord(generics.UpdateAPIView):
    queryset = Hangman.objects.all()
    serializer_class = HangmanGameSerializer
    lookup_field = "id"

    def update(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = GuessWordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        guess = serializer.validated_data["guess"].lower()

        word_to_guess_lower = instance.word_to_guess.lower()

        if instance.game_state == 'IN_PROGRESS':
            if guess in word_to_guess_lower:
                new_word_state = ''
                for i in range(len(instance.word_to_guess)):
                    if word_to_guess_lower[i] == guess:
                        new_word_state += instance.word_to_guess[i]
                    else:
                        new_word_state += instance.current_word_state[i]
                instance.current_word_state = new_word_state

                if  instance.current_word_state == instance.word_to_guess:
                    instance.game_state = "WON"
                correct_guess = True
            else:
                instance.incorrect_guesses +=1
                if instance.incorrect_guesses >= instance.max_incorrect_guesses:
                    instance.game_state = "LOST"
                    instance.incorrect_guesses = instance.max_incorrect_guesses
                correct_guess = False
            instance.save()

            resp_data = {
                "game_state":instance.game_state,
                "correct_word":instance.word_to_guess,
                "correct_guess":correct_guess,
                "current_word_state":instance.current_word_state,
                "incorrect_guesses":instance.incorrect_guesses,
                "word_to_guess_length":len(instance.word_to_guess),
            }

            if instance.game_state == "IN_PROGRESS":
                resp_data['max_incorrect_guesses'] = instance.max_incorrect_guesses
            
            return Response(resp_data,status=status.HTTP_200_OK)
        else:

            return Response({"message":"Game is already over. Start a new game."},status=status.HTTP_400_BAD_REQUEST)

