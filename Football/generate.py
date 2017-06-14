import random
import datetime
from Football.models import *

Club_values = ['Барселона', 'Реал Мадрид', 'Манчестер Юнайтед', 'Ювентус» (Италия)', 'Бавария', 'Галатасарай', 'Шахтер']

City = ['Донецк', 'Москва', 'Пекин', 'Мадрид', 'Череповец', 'Шахты', 'Лондон', 'Бутово', 'Алжир', 'Ростов']

Base = ['Мемориал Стэдиум', 'Джордан-Хейр', 'Донбасс Арена', 'Бунг Карно', 'Бен Хилл Гриффин', 'Уэмбли', 'Азади',
        'Мичиган Стэдиум', 'Бивер Стэдиум']


def Year():
    return str(random.randint(1500, 2010))


League = ['Высшая', 'Первая', 'Вторая', 'Третья']

Names = ['Ян', 'Николай', 'Дмитрий', 'Эльдар', 'Мирон', 'Слава', 'Виталий']

Surnames = ['Степаненко', 'Кпсс', 'Добродушный', 'Киселев', 'Ларин', 'Джарахов', 'Фёдоров']

Patronymic = ['Сергеевич', 'Александрович', 'Борисович', 'Янович', 'Игоревич', 'Леонидович', 'Алексеевич']


def FIO():
    return random.choice(Surnames) + ' ' + random.choice(Names) + ' ' + random.choice(Patronymic)


def Phone():
    return ''.join([str(random.randint(0, 9)) for __ in range(13)])


Position = ['Нападающий', 'Вратарь', 'Защитник', 'Полузащитник']


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_seconds = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_seconds)


def Birthday():
    return random_date((datetime.datetime.now() - datetime.timedelta(days=365 * 15)), datetime.datetime.now())


def Date():
    year = random.choice(range(1950, 1995))
    month = random.choice(range(1, 13))
    day = random.choice(range(1, 29))
    birth_date = datetime.datetime(year, month, day)


def YearFact():
    return str(random.randint(1900, 2012))


Comments = ['Вечен', 'Не вечен', '*Образец контракта*']


def Cost():
    return str(random.randint(0, 10000))


Opposing_values = ['Команда А', 'Заря', 'Галичина', 'Спартак', 'Лужники', 'Алтын']

Country = ['Украина', 'Россия', 'Испания', 'Молдавия', 'Польша', 'Китай', 'Алжир']


def DateGame():
    return random_date((datetime.datetime.now() - datetime.timedelta(days=365 * 15)), datetime.datetime.now())


GameLevel = ['Мировой', 'Континентальный', 'Региональный', 'Городской', 'Галактический']


def CountStart():
    return str(random.randint(0, 20))


def CountFinish():
    return str(random.randint(0, 20))


def Salary():
    return str(random.randint(0, 200000))


def Order():
    return bool(random.getrandbits(1))


def getCountries():
    return list(map(itemgetter(1), Country.objects.all().values('Name').values_list()))


def getCities():
    return list(map(itemgetter(1), City.objects.all().values('Name').values_list()))


def getLeagues():
    return list(map(itemgetter(1), League.objects.all().values('Name').values_list()))


def Create():
    return LabThree(Club=random.choice(Club_values), City=random.choice(City), Base=random.choice(Base), Year=Year(),
                    League=random.choice(League), FIO=FIO, Phone=Phone(), FIOGamer=FIO,
                    Position=random.choice(Position), Birthday=Birthday(), YearFact=YearFact(),
                    Comments=random.choice(Comments), Cost=Cost(), Opposing=random.choice(Opposing_values),
                    CountryTeam=random.choice(Country), TeamCoach=FIO, DateGame=DateGame(),
                    Country=random.choice(Country), GameLevel=random.choice(GameLevel), CountStart=CountStart(),
                    CountFinish=CountFinish(), Salary=Salary(), Order=Order())


def CreatePlayer(position_ids, club_ids):
    obj = Player(Name=FIO(), Birthday=Birthday(), YearFact=YearFact(), Contract_comments=random.choice(Comments),
                 Contract_cost=Cost())
    obj.Position_id = random.choice(position_ids)
    obj.Club_id = random.choice(club_ids)
    return obj


def CreateOpposing(country_ids):
    obj = Opposing(Name=random.choice(Opposing_values), Coach=FIO())
    obj.Country_id = random.choice(country_ids)
    return obj


def CreateClub(city_ids, league_ids):
    obj = Club()
    obj.Name = random.choice(Club_values)
    obj.Base=random.choice(Base)
    obj.Head_FIO=FIO()
    obj.Head_number=Phone()
    obj.Year=YearFact()
    obj.City_id = random.choice(city_ids)
    obj.League_id = random.choice(league_ids)
    return obj


def CreateMatch(opposing_id, country_id, game_level_id, club_id):
    obj = Match(Date=DateGame(), CountStart=CountStart(), CountFinish=CountFinish())
    obj.Opposing_id = random.choice(opposing_id)
    obj.Country_id = random.choice(country_id)
    obj.GameLevel_id = random.choice(game_level_id)
    obj.Club_id = random.choice(club_id)
    return obj