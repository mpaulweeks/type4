from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import timezone
from type4.models import Card, Status
from type4.classes import CardWrapper, CardChecker
from type4.forms import ChangesForm

import logging
logger = logging.getLogger(__name__)

def extract_names(cards):
	return '|'.join(sorted(c.name for c in cards)) #change to sorted?

def index(request):
    all_cards = CardWrapper.get_cards()
    filtered_cards = list(c for c in all_cards if c.is_in_stack())
    card_names = extract_names(filtered_cards)
    context = {
    	'card_names': card_names,
    	'card_count': len(filtered_cards),
    	'show_art': 'false',
	}
    return render(request, 'type4/default.html', context)  

def __all_cards_context(wrappers):
	dict = CardWrapper.filter_cards_by_status(wrappers)    
	in_cards = dict[Status.IN_STACK]
	want_cards = dict[Status.GOING_IN_STACK]
	removed_cards = dict[Status.REMOVED_FROM_STACK]
	rejected_cards = dict[Status.REJECTED_FROM_STACK]
	context = {
		'show_art': 'false',
		'in_names': extract_names(in_cards),
		'want_names': extract_names(want_cards),
		'removed_names': extract_names(removed_cards),
		'rejected_names': extract_names(rejected_cards),
		'in_count': len(in_cards),
		'want_count': len(want_cards),
		'removed_count': len(removed_cards),
		'rejected_count': len(rejected_cards),
	}
	return context
	
def all_cards(request):
	wrappers = CardWrapper.get_cards()
	context = __all_cards_context(wrappers)
	return render(request, 'type4/all_cards.html', context)  

def filter(request):
	flag_set = Card.flags()
	filter_dict = {}
	for f in flag_set:
		if f in request.GET:
			s = request.GET[f]
			if s == 'True':
				filter_dict[f] = True
			if s == 'False':
				filter_dict[f] = False
	cards = Card.objects.filter(**filter_dict)
	ids = list(c.id for c in cards)
	wrappers = CardWrapper.get_cards_by_id(ids)
	context = __all_cards_context(wrappers)
	context['flag_set'] = flag_set
	return render(request, 'type4/filter.html', context)  
    
def changes(request):
	form = ChangesForm(request.GET)
	if form.is_valid(): # All validation rules pass
		cd = form.cleaned_data
		from_timestamp = cd['from_timestamp']
		to_timestamp = cd['to_timestamp']
		if to_timestamp <= from_timestamp:
			raise Exception('From must be before To')
		all_cards = CardWrapper.get_cards()
		cards_before = list(c for c in all_cards if c.was_in_stack(from_timestamp))
		cards_after = list(c for c in all_cards if c.was_in_stack(to_timestamp))
		cards_added = list(c for c in cards_after if c not in cards_before)
		cards_removed = list(c for c in cards_before if c not in cards_after)
		context = {
			'form': form,
			'added_names': extract_names(cards_added),
			'added_count': len(cards_added),
			'removed_names': extract_names(cards_removed),
			'removed_count': len(cards_removed),
			'show_art': 'true',
		}
		return render(request, 'type4/changes.html', context)
	return render(request, 'type4/changes.html', {
		'form': form,
	})
	    
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
	checker = CardChecker()
	for n in card_names:
		id = checker.get_id(n)
		if id:
			new_card = Card.objects.get(id=id)
		else:
			new_card = Card()
			new_card.name = n
		for f in flag_status:
			setattr(new_card, f['flag_id'], f['status'])
		new_card.save()
		new_status = Status()
		new_status.card = new_card
		new_status.status = selected_status
		new_status.timestamp = timezone.now()
		new_status.save()
	return HttpResponseRedirect(reverse('type4:add_cards'))
