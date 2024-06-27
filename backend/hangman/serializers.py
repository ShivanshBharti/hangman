from rest_framework import serializers
from .models import *

class HangmanGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hangman
        fields = '__all__'


class GuessWordSerializer(serializers.Serializer):
    guess = serializers.CharField(max_length=1)

    def validate_guess(self,value):
        value = value.lower()
        
        if not value.isalpha() or len(value) > 1:
            raise serializers.ValidationError("Invalid guess. It should be a single letter.")
        
        return value