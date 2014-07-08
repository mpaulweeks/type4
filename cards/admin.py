from django.contrib import admin
from cards.models import Card, Status
    
class StatusInline(admin.StackedInline):
	model = Status
	extra = 1
	
class CardAdmin(admin.ModelAdmin):
	inlines = [StatusInline]
	flags = ['isSorcery']
	fieldsets = [
		(None,		{'fields': ['name']}),
		('Flags',	{'fields': flags}),
	]
 	list_display = ['name', 'is_in_stack'] + flags
 	list_filter = flags
	search_fields = ['name']


admin.site.register(Card, CardAdmin)