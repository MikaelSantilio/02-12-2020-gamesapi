"""
Book: Building RESTful Python Web Services
Chapter 2: Working with class based views and hyperlinked APIs in Django
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from games.models import Game
from games.serializers import GameSerializer

# 1. [POST, PUT]: Jogos não podem ter nomes repetidos;
# 2. [DELETE]: Jogos que já foram lançados não podem ser excluídos.

@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return Response(games_serializer.data)

    elif request.method == 'POST':
        games_serializer = GameSerializer(data=request.data)
        if games_serializer.is_valid():
            data = games_serializer.validated_data
            exists = Game.objects.filter(name=data['name'])

            if exists:
                return Response(
                    {'detail': 'The name of this game already exists'},
                    status=status.HTTP_400_BAD_REQUEST)

            games_serializer.save()
            return Response(games_serializer.data, status=status.HTTP_201_CREATED)
        return Response(games_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.method == 'GET':
        games_serializer = GameSerializer(game)
        return Response(games_serializer.data)

    elif request.method == 'PUT':
        games_serializer = GameSerializer(game, data=request.data)
        if games_serializer.is_valid():
            data = games_serializer.validated_data
            exists = Game.objects.filter(name=data['name']).exclude(name=game.pk)

            if exists:
                return Response(
                    {'detail': 'The name of this game already exists'},
                    status=status.HTTP_400_BAD_REQUEST)

            games_serializer.save()
            return Response(games_serializer.data)
        return Response(games_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        now_aware = timezone.make_aware(datetime.now())
        if game.release_date < now_aware:
            return Response(
                    {'detail': 
                    ("A game that has already been released can't be deleted." +
                        f" This game was released in {game.release_date}")},
                    status=status.HTTP_400_BAD_REQUEST)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
