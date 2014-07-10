from type4.models import Card, Status
from operator import attrgetter
from collections import defaultdict

import logging
logger = logging.getLogger(__name__)

class CardWrapper():

	def was_in_stack(self, moment):
		for status in self.status_history:
			if status.timestamp < moment:
				return status.is_in_stack()
		return False
	
	def is_in_stack(self):
		return self.current_status.is_in_stack()

	def __init__(self, card, statuses):
		self.card = card
		self.name = card.name
		sorted_statuses = sorted(
			statuses, key=attrgetter('timestamp'), reverse=True)
		self.status_history = sorted_statuses
		self.current_status = sorted_statuses[0]

	@staticmethod
	def get_card_dict():
		statuses = Status.objects.all()
		status_dict = defaultdict(list)
		for s in statuses:
			status_dict[s.card_id].append(s)
		cards = Card.objects.all()
		card_dict = {}
		for c in cards:
			card_dict[c.name] = CardWrapper(c, status_dict[c.id])
		return card_dict

	@staticmethod
	def get_cards():
		return CardWrapper.get_card_dict().values()

	@staticmethod
	def get_card(name):
		return CardWrapper.get_card_dict()[name]