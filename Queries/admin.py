from django.contrib import admin
from Queries.models import *
from datetime import date, time
from django.db.models import Count, Max, Min, Sum, Subquery, Exists, OuterRef


class ProxyListView(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'
    actions = None

    def has_add_permission(self, request):
        return False


class ProxyListView_(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list_new.html'
    actions = None

    def has_add_permission(self, request):
        return False


class Proxy_OpposingAdmin(ProxyListView):
    list_display = ['Name', 'Country']

    def get_queryset(self, request):
        t = Opposing.objects.select_related('Country').order_by('Country__Name')
        print(t.query)
        return t


class Proxy_PlayerAdmin(ProxyListView):
    list_display = ['Name', 'Position']

    def get_queryset(self, request):
        t = Player.objects.select_related('Position').filter(Name__contains='Джарахов').order_by('Position__Name')
        print(t.query)
        return t


class Proxy_ClubAdmin(ProxyListView):
    list_display = ['Name', 'Base', 'City', 'Year', 'Head_FIO']

    def get_queryset(self, request):
        t = Club.objects.all().filter(City__Name='Донецк').order_by('Name')
        print(t.query)
        return t


class Proxy_MatchAdmin(ProxyListView):
    list_display = ['Club', 'Opposing', 'Date', 'GameLevel', 'CountStart', 'CountFinish', 'Country']

    def get_queryset(self, request):
        t = Match.objects.all().select_related('Country').filter(
            Date__gte=datetime.datetime.now().date() - datetime.timedelta(days=365 * 2),
            Date__lte=datetime.datetime.now().date()).order_by('Club__Name')
        print(t.query)
        return t


class Proxy_MatchBetweenAdmin(ProxyListView):
    list_display = ['Club', 'Opposing', 'Date', 'GameLevel', 'CountStart', 'CountFinish', 'Country']

    def get_queryset(self, request):
        t = Match.objects.all().select_related('Country').filter(Date__range=(date(2012, 1, 2), date(2012, 4, 1))).order_by('Club__Name')
        print(t.query)
        return t


class Proxy_ClubInAdmin(ProxyListView):
    list_display = ['Name', 'Base', 'City', 'Year', 'Head_FIO']

    def get_queryset(self, request):
        t = Club.objects.all().select_related('City').filter(City__Name__in=['Донецк', 'Киев']).order_by('Name')
        print(t.query)
        return t


class Proxy_CityLeftAdmin(ProxyListView):
    list_display = ['City', 'Name']

    def get_queryset(self, request):
        t = Club.objects.select_related('City').order_by('City__Name')
        print(t.query)
        return t


class Proxy_ClubDistinctAdmin(ProxyListView):
    list_display = ['Name', 'City']

    def get_queryset(self, request):
        t = Club.objects.filter(player__isnull=False).distinct().order_by('Name')
        print(t.query)
        return t


class Proxy_PlayerAgregateAdmin(ProxyListView_):

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context, )

        list_display = [('Минимальная стоимость контракта', 'min_cost'), ('Максимальная стоимость контракта', 'max_cost')]
        res = Player.objects.aggregate(min_cost=Min('Contract_cost'), max_cost=Max('Contract_cost'))
        print(res)
        response.context_data['data'] = [res]
        response.context_data['headers'] = list_display
        return response


class Proxy_Balls_SummaryAdmin(ProxyListView_):

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context, )

        list_display = [('Клуб', 'Club__Name'), ('Количество забитых мячей', 'count_start')]
        res = Match.objects.annotate(count_start=Sum('CountStart')).values('count_start', 'Club__Name').order_by('Club__Name')
        print(res.query)
        response.context_data['data'] = res
        response.context_data['headers'] = list_display
        return response


class Proxy_Balls_Summary1Admin(ProxyListView_):

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context, )

        list_display = [('Клуб', 'Club__Name'), ('Количество сыгранных игр', 'count_games')]
        res = Match.objects.filter(Date__year__gt=2012).values('Club__Name').annotate(count_games=Count('Club__Name'))\
            .values('count_games', 'Club__Name').order_by('Club__Name')
        print(res.query)
        response.context_data['data'] = res
        response.context_data['headers'] = list_display
        return response


class Proxy_Attackers_SummaryAdmin(ProxyListView_):
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context, )

        list_display = [('Клуб', 'Club__Name'), ('Количество нападающих', 'count_attackers')]
        res = Player.objects.all().filter(Position__Name='Нападающий').values('Position').annotate(count_attackers=Count('Position'))\
            .filter(count_attackers__gt=5)\
            .values('count_attackers', 'Club__Name').order_by('Club__Name')
        print(res.query)
        response.context_data['data'] = res
        response.context_data['headers'] = list_display
        return response


class Proxy_GoalKeepers_SummaryAdmin(ProxyListView_):
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context, )

        list_display = [('Клуб', 'Club__Name'), ('Количество вратарей', 'count_goalkeepers')]
        res = Player.objects.filter(Position__Name='Вратарь').select_related().values('Position')\
            .annotate(count_goalkeepers=Count('Position'))\
            .filter(count_goalkeepers__gt=0, YearFact__gt=2000)\
            .values('count_goalkeepers', 'Club__Name').order_by('Club__Name')
        print(res.query)
        response.context_data['data'] = res
        response.context_data['headers'] = list_display
        return response


class Proxy_Subquery1Admin(ProxyListView_):
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context, )

        list_display = [('Клуб', 'Name'), ('Сыграли хотя бы одну игру', 'test')]
        games = Match.objects.filter(Club__isnull=False, Club=OuterRef('pk'))
        res = Club.objects.values('id').annotate(test=Exists(games)).values('Name', 'test').filter(test=True)\
            .order_by('Name')
        print(res.query)
        response.context_data['data'] = res
        response.context_data['headers'] = list_display
        return response


class Proxy_ParamAdmin(admin.ModelAdmin):
    list_display = ['player_name', 'player_club']

    actions = None
    search_fields = ['Club__Name']

    def has_add_permission(self, request):
        return False

    def player_club(self, object):
        return object.Club.Name

    def player_name(self, object):
        return object.Name

    def get_queryset(self, request):
        t = Player.objects.filter(Club__Name__contains='').order_by('Name')
        print(t.query)
        return t


class Proxy_TopAdmin(ProxyListView_):
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context, )

        list_display = [('Игрок', 'Name'), ('Стоимость контракта', 'Contract_cost')]
        prices = Player.objects.values('Contract_cost').order_by('-Contract_cost')
        res = Player.objects.values('Name', 'Contract_cost').filter(Contract_cost__in=prices[:5]).order_by('-Contract_cost')
        print(res.query)
        response.context_data['data'] = res
        response.context_data['headers'] = list_display
        return response


admin.site.register(Proxy_Top5, Proxy_TopAdmin)
admin.site.register(Proxy_Param, Proxy_ParamAdmin)
admin.site.register(Proxy_Subquery1, Proxy_Subquery1Admin)
admin.site.register(Proxy_GoalKeepers_Summary, Proxy_GoalKeepers_SummaryAdmin)
admin.site.register(Proxy_Attackers_Summary, Proxy_Attackers_SummaryAdmin)
admin.site.register(Proxy_Balls_Summary1, Proxy_Balls_Summary1Admin)
admin.site.register(Proxy_Balls_Summary, Proxy_Balls_SummaryAdmin)
admin.site.register(Proxy_Player_Agregate, Proxy_PlayerAgregateAdmin)
admin.site.register(Proxy_Club_Distinct, Proxy_ClubDistinctAdmin)
admin.site.register(Proxy_Club_Left, Proxy_CityLeftAdmin)
admin.site.register(Proxy_Club_In, Proxy_ClubInAdmin)
admin.site.register(Proxy_Match_Between, Proxy_MatchBetweenAdmin)
admin.site.register(Proxy_Match, Proxy_MatchAdmin)
admin.site.register(Proxy_Club, Proxy_ClubAdmin)
admin.site.register(Proxy_Opposing, Proxy_OpposingAdmin)
admin.site.register(Proxy_Player, Proxy_PlayerAdmin)
