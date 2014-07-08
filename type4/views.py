from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
import datetime
from type4.models import Card, Status

def index(request):
    all_cards = Card.objects.order_by('name')
    filtered_cards = list(c for c in all_cards if c.is_in_stack())
    context = {'filtered_cards': filtered_cards, 'show_art':False}
    return render(request, 'type4/index.html', context) 
    
def gallery(request):
    all_cards = Card.objects.order_by('name')
    show_art = True
    filtered_cards = list(c for c in all_cards if c.is_in_stack())
    context = {'filtered_cards': filtered_cards, 'show_art':show_art}
    return render(request, 'type4/gallery.html', context)  
    
def add_cards(request):
	status_set = Status().status_choices()
	flag_set = Card.flags()
	context = {'status_set': status_set, 'flag_set': flag_set}
	return render(request, 'type4/add_cards.html', context)
    
def update(request):
	flag_set = Card.flags()
	flag_status = []
	for f in flag_set:
		s = request.POST[f]
		if s == 'True':
			flag_status.append({'flag_id': f, 'status':True})
		if s == 'False':
			flag_status.append({'flag_id': f, 'status':False})
	selected_status = request.POST['status']
	card_names = request.POST['card_names'].splitlines()
	for n in card_names:
		new_card = Card.objects.get_or_create(name=n)[0]
		for f in flag_status:
			setattr(new_card, f['flag_id'], f['status'])
		new_card.save()
		new_status = Status()
		new_status.card = new_card
		new_status.status = selected_status
		new_status.timestamp = datetime.datetime.now()
		new_status.save()
	return HttpResponseRedirect(reverse('type4:add_cards'))
