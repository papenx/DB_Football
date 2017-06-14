from django.db import models
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class League(models.Model):
    Name = models.CharField('Название лиги', max_length=64)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Таблица лиг'
        verbose_name = 'Лигу'


class Position(models.Model):
    Name = models.CharField('Название положения', max_length=20, null=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Таблица положений в команде'
        verbose_name = 'Положение'


class Country(models.Model):
    Name = models.CharField('Название', max_length=64, null=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Таблица страны'
        verbose_name = 'Страну'


class Opposing(models.Model):
    Name = models.CharField('Название команды противника', max_length=64, null=True)
    Country = models.ForeignKey(Country, verbose_name='Страна команды противника')
    Coach = models.CharField('Тренер', max_length=256)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Таблица команд противника'
        verbose_name = 'Команду противника'


class GameLevel(models.Model):
    Name = models.CharField('Тип уровня', max_length=64, null=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Таблица уровней игры'
        verbose_name = 'Уровень'


class City(models.Model):
    Name = models.CharField('Название города', max_length=64, null=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Таблица города'
        verbose_name = 'Город'


def validate_year(value):
    current_date = datetime.datetime.now().year
    if value > current_date:
        raise ValidationError(
            _('Год должен быть меньше текущего')
        )
    elif value <= 0:
        raise ValidationError('Год не может быть отрицательным')


class Club(models.Model):
    Name = models.CharField('Название клуба', max_length=64, null=True)
    Base = models.CharField('Тренировочная база', max_length=64)
    City = models.ForeignKey(City, verbose_name='Город размещения клуба',  null=True)
    Head_FIO = models.CharField('ФИО руководителя', max_length=256)
    Head_number = models.CharField('Телефон руководителя', max_length=13, null=True)
    League = models.ForeignKey(League, verbose_name='Лига', null=True)
    Year = models.PositiveSmallIntegerField('Год основания клуба', validators=[validate_year])

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Таблица клубы'
        verbose_name = 'Запись о клубе'


class Match(models.Model):
    Opposing = models.ForeignKey(Opposing, verbose_name='Команда противника', null=True)
    Country = models.ForeignKey(Country, verbose_name='Страна проведения')
    Date = models.DateTimeField('Дата проведения')
    GameLevel = models.ForeignKey(GameLevel, verbose_name='Уровень игры',  null=True)
    CountStart = models.PositiveIntegerField('К-во забитых мячей')
    CountFinish = models.PositiveIntegerField('К-во пропущенных мячей')
    Club = models.ForeignKey(Club, verbose_name='Клуб')

    def __str__(self):
        return '{} - {}'.format(self.Club, self.Opposing)

    class Meta:
        verbose_name_plural = 'Таблица игры'
        verbose_name = 'Игра'


class Player(models.Model):
    Name = models.CharField('ФИО игрока', max_length=256)
    Position = models.ForeignKey(Position, verbose_name='Положение игрока в команде')
    Birthday = models.DateField('Дата рождения', null=True)
    YearFact = models.PositiveSmallIntegerField('Принят в команду (год)')
    Photo = models.ImageField('Фото игрока', null=True, blank=True)
    Contract_comments = models.TextField('Условия контракта', null=True)
    Contract_cost = models.PositiveSmallIntegerField('Стоимость контракта', null=True)
    Club = models.ForeignKey(Club, verbose_name='Клуб', null=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Таблица игроков'
        verbose_name = 'Игрока'


class Do(models.Model):
    Match_key = models.ForeignKey(Match, verbose_name='Игра', blank=True, null=True)
    Player_key = models.ManyToManyField(Player, verbose_name='Игроки', null=True)
    Salary = models.PositiveSmallIntegerField('Премия игрока за игру')

    class Meta:
        verbose_name_plural = 'Таблица участие в игре'
        verbose_name = 'Участие'


class LabThree(models.Model):
    Club = models.CharField('Название клуба', max_length=64)
    City = models.CharField('Город размещения клуба', max_length=64)
    Base = models.CharField('Тренировочная база', max_length=64)
    Year = models.PositiveSmallIntegerField('Год создания клуба')
    League = models.CharField('Принадлежность к лиге', max_length=64)
    FIO = models.CharField('ФИО руководителя клуба', max_length=256)
    Phone = models.CharField('Телефон руководителя клуба', max_length=13)
    FIOGamer = models.CharField('ФИО игрока', max_length=256)
    Position = models.CharField('Положение игрока в команде', max_length=20)
    Birthday = models.DateTimeField('Дата рождения')
    YearFact = models.PositiveSmallIntegerField('Принят в команду(год)')
    Photo = models.ImageField('Фото игрока', null=True, blank=True, upload_to='static')
    Comments = models.TextField('Контракт с игроком')
    Cost = models.PositiveSmallIntegerField('Стоимость контракта')
    Opposing = models.CharField('Название команды противника', max_length=64)
    CountryTeam = models.CharField('Страна команды противника', max_length=64)
    TeamCoach = models.CharField('Тренер команды', max_length=256)
    DateGame = models.DateTimeField('Дата проведения игры')
    Country = models.CharField('Страна проведения игры', max_length=64)
    GameLevel = models.CharField('Уровень игры', max_length=30)
    CountStart = models.PositiveSmallIntegerField('Количество забитых мячей')
    CountFinish = models.PositiveSmallIntegerField('Количество пропущенных мячей')
    Salary = models.PositiveSmallIntegerField('Премия игрока за игру')
    Order = models.BooleanField('Участие в игре(да/нет)', blank=True)

    class Meta:
        verbose_name_plural = 'Учёт футбольных клубов'
        verbose_name = 'Запись о клубе'
