from django.db import models

class Card(models.Model):
    name = models.CharField(max_length=100)
    isSorcery = models.BooleanField('is sorcery speed', default=False)
    
    def __unicode__(self):
        return self.name

class Status(models.Model):
    
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

	card = models.ForeignKey(Card)
	status = models.IntegerField(
		choices=STATUS_CHOICES,
		default=IN_STACK)
    
	def is_in_stack(self):
		return self.status == self.IN_STACK

	def __unicode__(self):
		str = ''
		if self.is_in_stack():
			str = 'NOT '
		return (self.card.name
			+ ' is ' 
			+ str
			+ 'in the stack')
