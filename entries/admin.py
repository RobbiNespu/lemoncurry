from django.contrib import admin
from .models import Entry, Syndication


class SyndicationInline(admin.TabularInline):
    model = Syndication
    extra = 1


class EntryAdmin(admin.ModelAdmin):
    inlines = (
        SyndicationInline,
    )


admin.site.register(Entry, EntryAdmin)
