from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import timezone
from type4.models import Card, Status
import time
from time import mktime
from datetime import datetime

def extract_names(cards):
	return '|'.join(list(c.name for c in cards))
	
def fix_time(time_arg):
	time_struct = time.strptime(time_arg, '%Y-%m-%d')
	dt = datetime.fromtimestamp(mktime(time_struct))
	return dt

def index(request):
    all_cards = Card.objects.order_by('name')
    filtered_cards = list(c for c in all_cards if c.is_in_stack())
    card_names = extract_names(filtered_cards)
    context = {
    	'filtered_cards': filtered_cards, 
    	'card_names': card_names,
    	'show_art': 'false',
	}
    return render(request, 'type4/decklist.html', context)  
    
def changes(request, from_timestamp_arg, to_timestamp_arg):
	from_timestamp = fix_time(from_timestamp_arg)
	to_timestamp = fix_time(to_timestamp_arg)
	all_cards = Card.objects.order_by('name')
	cards_before = list(c for c in all_cards if c.was_in_stack(from_timestamp))
	cards_after = list(c for c in all_cards if c.was_in_stack(to_timestamp))
	cards_added = list(c for c in cards_after if c not in cards_before)
	cards_removed = list(c for c in cards_before if c not in cards_after)
	context = {
		'added_names': extract_names(cards_added),
		'removed_names': extract_names(cards_removed),
		'show_art': 'true',
	}
	return render(request, 'type4/changes.html', context)
	    
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
		new_status.timestamp = timezone.now()
		new_status.save()
	return HttpResponseRedirect(reverse('type4:add_cards'))
