from django.http import HttpResponse
from django.shortcuts import render

from type4.models import Card

def index(request):
    all_cards = Card.objects.order_by('name')
    filtered_cards = list(c for c in all_cards if c.is_in_stack())
    context = {'filtered_cards': filtered_cards}
    return render(request, 'cards/index.html', context)   
    