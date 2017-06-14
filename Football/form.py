from django import forms
from django.contrib.admin.helpers import ActionForm

from Football.models import *

list_display = [(f.name, f.verbose_name) for f in LabThree._meta.get_fields()]


class UpdateScoreForm(ActionForm):
    field = forms.ChoiceField(choices=list_display, label=' поля', required=False)
    from_ = forms.CharField(label='с', required=False)
    to = forms.CharField(label='на', required=False)


list_player = [(f.name, f.verbose_name) for f in Player._meta.get_fields() if f.name not in ['Position', 'Club', 'do']]


class UpdatePlayerForm(ActionForm):
    field = forms.ChoiceField(choices=list_player, label=' поля', required=False)
    from_ = forms.CharField(label='с', required=False)
    to = forms.CharField(label='на', required=False)


list_club = [(f.name, f.verbose_name) for f in Club._meta.get_fields() if f.name not in ['City', 'League', 'player',
                                                                                         'match']]


class UpdateClubForm(ActionForm):
    field = forms.ChoiceField(choices=list_club, label=' поля', required=False)
    from_ = forms.CharField(label='с', required=False)
    to = forms.CharField(label='на', required=False)


list_opposing = [(f.name, f.verbose_name) for f in Opposing._meta.get_fields() if f.name not in ['Country', 'match']]


class UpdateOpposingForm(ActionForm):
    field = forms.ChoiceField(choices=list_opposing, label=' поля', required=False)
    from_ = forms.CharField(label='с', required=False)
    to = forms.CharField(label='на', required=False)


list_match = [(f.name, f.verbose_name) for f in Match._meta.get_fields() if f.name not in ['Country', 'GameLevel',
                                                                                           'Opposing', 'Club', 'do']]


class UpdateMatchForm(ActionForm):
    field = forms.ChoiceField(choices=list_match, label=' поля', required=False)
    from_ = forms.CharField(label='с', required=False)
    to = forms.CharField(label='на', required=False)
