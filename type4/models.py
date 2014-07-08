from django.db import models
import logging

logger = logging.getLogger(__name__)

class Card(models.Model):

	# fields
    name = models.CharField(max_length=100, primary_key=True)
    is_sorcery = models.BooleanField('is sorcery speed', default=False)
    is_wrath = models.BooleanField('is mass removal', default=False)
    is_burn = models.BooleanField('burns players', default=False)
    is_lifegain = models.BooleanField('gives life', default=False)
    is_fat = models.BooleanField('has combined p/t >= 14', default=False)
    is_counterspell = models.BooleanField('counters spells', default=False)
    is_masticore = models.BooleanField('provides repeated removal', default=False)
    is_draw = models.BooleanField('draws more than one card', default=False)
    
    # funcs
    def is_in_stack(self):
    	ordered_statuses = Status.objects.filter(
    		card_id = self.name
    	).order_by('timestamp')
    	if ordered_statuses.count() == 0:
    		return False
    	current_status = ordered_statuses[ordered_statuses.count()-1]
    	logger.critical(current_status)
    	return current_status.is_in_stack()
    is_in_stack.boolean = True
    
    def __unicode__(self):
        return self.name
    
    @staticmethod
    def flags():
    	return list(n for n in Card._meta.get_all_field_names() if n.startswith('is_'))

class StatusChoice():
	name = ''
	id = 0

class Status(models.Model):
    
    # status enum
	IN_STACK = 1
	GOING_IN_STACK = 2
	REMOVED_FROM_STACK = 3
	REJECTED_FROM_STACK = 4
	STATUS_CHOICES = (
		(IN_STACK, 'Currently in stack'),
		(GOING_IN_STACK, 'Waiting to be added'),
		(REMOVED_FROM_STACK, 'Playtested and then removed'),
		(REJECTED_FROM_STACK, 'Do NOT intend to try'),
	)

	# fields
	card = models.ForeignKey(Card)
	status = models.IntegerField(
		choices=STATUS_CHOICES,
		default=IN_STACK)
	timestamp = models.DateTimeField('timestamp')
    
    # funcs	
	def status_choices(self):
		choices = []
		for c in self.STATUS_CHOICES:
			s = StatusChoice()
			s.id = c[0]
			s.name = c[1]
			choices.append(s)
		return choices
    
	def is_in_stack(self):
		return self.status == self.IN_STACK

	def __unicode__(self):
		str = ''
		if not self.is_in_stack():
			str = 'NOT '
		return (self.card.name
			+ ' is ' 
			+ str
			+ 'in the stack')
