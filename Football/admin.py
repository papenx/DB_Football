from django.contrib import admin
from django.contrib import messages
from imagekit.admin import AdminThumbnail
from Football.models import *
from import_export.admin import ImportExportModelAdmin
from Football.generate import *
from Football.form import *
from django.db import transaction
from django.db.models import F, Func, Value
from bulk_update.helper import bulk_update
import itertools
from django import forms
from operator import itemgetter

from django.utils.translation import ugettext_lazy

template = 'thumbnail.html'


class RealizationInline(admin.StackedInline):
    model = Do
    extra = 2


def set_score_action_match(self, request, queryset):
    from_ = request.POST['from_']
    to = request.POST['to']
    field = request.POST['field']
    kwargs_filter = {'{0}'.format(field): from_, }

    kwargs_update = {'{0}'.format(field): to, }

    Match.objects.filter(**kwargs_filter).update(**kwargs_update)
    messages.success(request, 'Записи обновлены')


set_score_action_match.short_description = 'Заменить все значения'


def delete_all_matches(self, request, queryset):
    Match.objects.all().delete()


delete_all_matches.short_description = 'Удалить все данные'


def delete_match(self, request, queryset):
    from_ = request.POST['from_']
    field = request.POST['field']
    kwargs_filter = {'{0}'.format(field): from_, }
    Match.objects.filter(**kwargs_filter).delete()
    messages.success(request, 'Записи удалены')


delete_match.short_description = 'Удалить по значению'


def generate_match(self, request, queryset):
    opposing_id = list(map(itemgetter(0), Opposing.objects.all().values_list()))
    country_id = list(map(itemgetter(0), Country.objects.all().values_list()))
    game_level_id = list(map(itemgetter(0), GameLevel.objects.all().values_list()))
    club_id = list(map(itemgetter(0), Club.objects.all().values_list()))
    Match.objects.bulk_create([CreateMatch(opposing_id, country_id, game_level_id, club_id) for i in range(100)])
    messages.success(request, 'Сгенерированы данные')

generate_match.short_description = 'Сгенерировать'


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [RealizationInline]
    list_display = ['id', 'Club', 'GameLevel', 'Country', 'CountStart', 'CountFinish', 'Opposing', 'Date']
    search_fields = ('id', 'Club__Name')
    list_filter = ['Club', 'GameLevel', 'Country']
    action_form = UpdateMatchForm
    actions = [set_score_action_match, delete_all_matches, delete_match, generate_match]

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] in ['set_score_action_match', 'delete_all_matches',
                                                                   'delete_match', 'generate_match']:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Match.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(CompetitionAdmin, self).changelist_view(request, extra_context)


class HelperAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name']
    search_fields = ('id', 'Name')
    list_filter = ['Name']


def set_score_action_opposing(self, request, queryset):
    from_ = request.POST['from_']
    to = request.POST['to']
    field = request.POST['field']
    kwargs_filter = {'{0}'.format(field): from_, }

    kwargs_update = {'{0}'.format(field): to, }

    Opposing.objects.filter(**kwargs_filter).update(**kwargs_update)
    messages.success(request, 'Записи обновлены')


set_score_action_opposing.short_description = 'Заменить все значения'


def delete_all_opposing(self, request, queryset):
    Opposing.objects.all().delete()


delete_all_opposing.short_description = 'Удалить все данные'


def delete_opposing(self, request, queryset):
    from_ = request.POST['from_']
    field = request.POST['field']
    kwargs_filter = {'{0}'.format(field): from_, }
    Opposing.objects.filter(**kwargs_filter).delete()
    messages.success(request, 'Записи удалены')


delete_opposing.short_description = 'Удалить по значению'


def generate_opposing(self, request, queryset):
    country_ids = list(map(itemgetter(0), Country.objects.all().values_list()))
    Opposing.objects.bulk_create([CreateOpposing(country_ids) for i in range(100)])
    messages.success(request, 'Сгенерированы данные')

generate_opposing.short_description = 'Сгенерировать'


class OpposingAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Country', 'Coach']
    search_fields = ('id', 'Name')
    list_filter = ['Name', 'Country']
    action_form = UpdateOpposingForm
    actions = [set_score_action_opposing, delete_all_opposing, delete_opposing, generate_opposing]

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] in ['set_score_action_opposing', 'delete_all_opposing',
                                                                   'delete_opposing', 'generate_opposing']:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Opposing.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(OpposingAdmin, self).changelist_view(request, extra_context)


def set_score_action_club(self, request, queryset):
    from_ = request.POST['from_']
    to = request.POST['to']
    field = request.POST['field']
    kwargs_filter = {'{0}'.format(field): from_, }

    kwargs_update = {'{0}'.format(field): to, }

    Club.objects.filter(**kwargs_filter).update(**kwargs_update)
    messages.success(request, 'Записи обновлены')


set_score_action_club.short_description = 'Заменить все значения'


def delete_all_clubs(self, request, queryset):
    Club.objects.all().delete()


delete_all_clubs.short_description = 'Удалить все данные'


def delete_club(self, request, queryset):
    from_ = request.POST['from_']
    field = request.POST['field']
    kwargs_filter = {'{0}'.format(field): from_, }
    Club.objects.filter(**kwargs_filter).delete()
    messages.success(request, 'Записи удалены')


delete_club.short_description = 'Удалить по значению'


def generate_clubs(self, request, queryset):
    city_ids = list(map(itemgetter(0), City.objects.all().values_list()))
    league_ids = list(map(itemgetter(0), League.objects.all().values_list()))
    Club.objects.bulk_create([CreateClub(city_ids, league_ids) for i in range(100)])
    messages.success(request, 'Сгенерированы данные')

generate_clubs.short_description = 'Сгенерировать'


class ClubAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Base', 'City', 'Head_FIO', 'Head_number', 'League', 'Year']
    search_fields = ('id', 'Name')
    list_filter = ['Name', 'Base', 'City', 'League']
    action_form = UpdateClubForm
    actions = [set_score_action_club, delete_all_clubs, delete_club, generate_clubs]

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] in ['set_score_action_club', 'delete_all_clubs',
                                                                   'delete_club', 'generate_clubs']:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Club.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(ClubAdmin, self).changelist_view(request, extra_context)


def generate_players(self, request, queryset):
    position_ids = list(map(itemgetter(0), Position.objects.all().values_list()))
    club_ids = list(map(itemgetter(0), Club.objects.all().values_list()))
    Player.objects.bulk_create([CreatePlayer(position_ids, club_ids) for i in range(100)])
    messages.success(request, 'Сгенерированы данные')

generate_players.short_description = 'Сгенерировать'


def set_score_action_player(self, request, queryset):
    from_ = request.POST['from_']
    to = request.POST['to']
    field = request.POST['field']
    kwargs_filter = {'{0}'.format(field): from_, }

    kwargs_update = {'{0}'.format(field): to, }

    Player.objects.filter(**kwargs_filter).update(**kwargs_update)
    messages.success(request, 'Записи обновлены')


set_score_action_player.short_description = 'Заменить все значения'


def delete_all_players(self, request, queryset):
    Player.objects.all().delete()


delete_all_players.short_description = 'Удалить все данные'


def delete_player(self, request, queryset):
    from_ = request.POST['from_']
    field = request.POST['field']
    kwargs_filter = {'{0}'.format(field): from_, }
    Player.objects.filter(**kwargs_filter).delete()
    messages.success(request, 'Записи удалены')


delete_player.short_description = 'Удалить по значению'


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Position', 'Birthday', 'YearFact', 'Photo', 'Contract_comments', 'Contract_cost',
                    'Club']
    search_fields = ('id', 'Name')
    list_filter = ['Position', 'Club']
    action_form = UpdatePlayerForm
    actions = [set_score_action_player, generate_players, delete_all_players, delete_player]

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] in ['generate_players', 'set_score_action_player',
                                                                   'delete_all_players',
                                                                   'delete_player']:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Player.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(PlayerAdmin, self).changelist_view(request, extra_context)


from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)


class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'last_login')


admin.site.register(User, UserProfileAdmin)
admin.site.register(League, HelperAdmin)
admin.site.register(Position, HelperAdmin)
admin.site.register(Country, HelperAdmin)
admin.site.register(Opposing, OpposingAdmin)
admin.site.register(GameLevel, HelperAdmin)
admin.site.register(City, HelperAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Match, CompetitionAdmin)
admin.site.register(Player, PlayerAdmin)


admin.site.site_header = 'Учёт деятельности ФК' \
                         'Разработчик: Чернышов Б.'
admin.site.index_title = ''
admin.site.site_title = 'Курсовая работа по бд'
