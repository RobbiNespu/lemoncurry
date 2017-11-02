from django.contrib import admin
from .models import Entry, Syndication


class SyndicationInline(admin.TabularInline):
    model = Syndication
    extra = 1


class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('title', 'id', 'kind', 'created')
    list_filter = ('kind',)
    inlines = (
        SyndicationInline,
    )


admin.site.register(Entry, EntryAdmin)
