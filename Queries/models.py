from django.db import models
from Football.models import *


class Proxy_Opposing(Opposing):
    class Meta:
        proxy = True
        verbose_name_plural = 'Симметричное объединение без условия'
        verbose_name = 'запись'


class Proxy_Country(Country):
    class Meta:
        proxy = True
        verbose_name_plural = 'Страны'
        verbose_name = 'Страна'


class Proxy_Player(Player):
    class Meta:
        proxy = True
        verbose_name_plural = 'Симметричное объединение (соответствие шаблону LIKE)'
        verbose_name = 'запись'


class Proxy_Club(Club):
    class Meta:
        proxy = True
        verbose_name_plural = 'Симметричное объединение по текстовому полю'
        verbose_name = 'запись'


class Proxy_Match(Match):
    class Meta:
        proxy = True
        verbose_name_plural = 'Симметричное объединение с условием по датам'
        verbose_name = 'запись'


class Proxy_Match_Between(Match):
    class Meta:
        proxy = True
        verbose_name_plural = 'Симметричное объединение (диапазон BETWEEN)'
        verbose_name = 'запись'


class Proxy_Club_In(Club):
    class Meta:
        proxy = True
        verbose_name_plural = 'Симметричное объединение (соответствие шаблону IN)'
        verbose_name = 'запись'


class Proxy_Club_Left(Club):
    class Meta:
        proxy = True
        verbose_name_plural = 'Левое объединение'
        verbose_name = 'запись'


class Proxy_Club_Distinct(Club):
    class Meta:
        proxy = True
        verbose_name_plural = 'Симметричное объединение с предикатом DISTINCT'
        verbose_name = 'запись'


class Proxy_Player_Agregate(Player):
    class Meta:
        proxy = True
        verbose_name_plural = 'Запрос с функциями агрегирования'
        verbose_name = 'запись'


class Proxy_Balls_Summary(Match):
    class Meta:
        proxy = True
        verbose_name_plural = 'Итоговый запрос без условия'
        verbose_name = 'запись'


class Proxy_Balls_Summary1(Match):
    class Meta:
        proxy = True
        verbose_name_plural = 'Итоговый запрос с условием на данные'
        verbose_name = 'запись'


class Proxy_Attackers_Summary(Player):
    class Meta:
        proxy = True
        verbose_name_plural = 'Итоговый запрос с условием на группы'
        verbose_name = 'запись'


class Proxy_GoalKeepers_Summary(Player):
    class Meta:
        proxy = True
        verbose_name_plural = 'Итоговый запрос с условием на группы и на данные'
        verbose_name = 'запись'


class Proxy_Subquery1(Match):
    class Meta:
        proxy = True
        verbose_name_plural = 'Подчиненный запрос EXISTS'
        verbose_name = 'запись'


class Proxy_Param(Player):
    class Meta:
        proxy = True
        verbose_name_plural = 'Параметрический запрос'
        verbose_name = 'запись'


class Proxy_Top5(Player):
    class Meta:
        proxy = True
        verbose_name_plural = 'Подчиненный запрос TOP'
        verbose_name = 'запись'

