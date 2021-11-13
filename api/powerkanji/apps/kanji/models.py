from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _


class Reading(models.Model):
    class Kind(models.IntegerChoices):
        ONYOMI = 1
        KUNYOMI = 2

    reading = models.CharField(_("how to read"), max_length=140)
    meaning = models.TextField(_("meaning"), blank=True)
    kind = models.IntegerField(_("kind"), choices=Kind.choices)
    entity = models.ForeignKey("kanji.Entity", on_delete=models.CASCADE, related_name="readings")

    def __str__(self):
        return self.reading


class Entity(models.Model):
    class Jlpt(models.IntegerChoices):
        N5 = 5
        N4 = 4
        N3 = 3
        N2 = 2
        N1 = 1

    kanji = models.CharField(_("kanji"), max_length=2, unique=True)
    ext_id = models.IntegerField(_("external id"))
    ext_key = models.IntegerField(_("external key"))
    strokes = models.IntegerField(_("strokes count"))
    jlpt = models.IntegerField(_("jlpt level"), choices=Jlpt.choices)

    class Meta:
        verbose_name_plural = _("entities")

    def __str__(self):
        return self.kanji
