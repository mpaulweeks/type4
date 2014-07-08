from django.http import HttpResponse
from django.shortcuts import render

from cards.models import Card

def index(request):
    filtered_cards = Card.objects.all()
    context = {'filtered_cards': filtered_cards}
    return render(request, 'cards/index.html', context)   
    