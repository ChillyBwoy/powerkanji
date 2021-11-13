from django.contrib import admin

from .models import Entity, Reading


class ReadingTabularInlineAdmin(admin.TabularInline):
    model = Reading
    extra = 0


class EntityAdmin(admin.ModelAdmin):
    list_filter = [
        "jlpt",
    ]
    list_display = (
        "kanji",
        "jlpt",
    )
    inlines = [
        ReadingTabularInlineAdmin,
    ]


admin.site.register(Entity, EntityAdmin)
