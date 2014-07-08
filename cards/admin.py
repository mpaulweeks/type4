from django.contrib import admin
from cards.models import Card, Status
    
class StatusInline(admin.StackedInline):
	model = Status
	extra = 1
	
class CardAdmin(admin.ModelAdmin):
	inlines = [StatusInline]

admin.site.register(Card, CardAdmin)