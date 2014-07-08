from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
import datetime
from type4.models import Card, Status

def index(request):
    all_cards = Card.objects.order_by('name')
    filtered_cards = list(c for c in all_cards if c.is_in_stack())
    context = {'filtered_cards': filtered_cards}
    return render(request, 'type4/index.html', context)   
    
def add_cards(request):
	status_set = Status().status_choices()
	context = {'status_set': status_set}
	return render(request, 'type4/add_cards.html', context)
    
def update(request):
	selected_status = request.POST['status']
	card_names = request.POST['card_names'].splitlines()
	for n in card_names:
		new_card = Card()
		new_card.name = n
		new_card.save()
		new_status = Status()
		new_status.card = new_card
		new_status.status = selected_status
		new_status.timestamp = datetime.datetime.now()
		new_status.save()
	return HttpResponseRedirect(reverse('type4:add_cards'))
