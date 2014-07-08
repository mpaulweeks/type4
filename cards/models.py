from django.db import models
import logging

logger = logging.getLogger(__name__)

class Card(models.Model):

	# fields
    name = models.CharField(max_length=100)
    isSorcery = models.BooleanField('is sorcery speed', default=False)
    
    # funcs
    def is_in_stack(self):
    	ordered_statuses = Status.objects.filter(
    		card_id = self.id
    	).order_by('timestamp')
    	current_status = ordered_statuses[ordered_statuses.count()-1]
    	logger.critical(current_status)
    	return current_status.is_in_stack()
    is_in_stack.boolean = True
    
    def __unicode__(self):
        return self.name

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
