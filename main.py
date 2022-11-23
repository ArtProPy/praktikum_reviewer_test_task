
# Для лучшего усваивания кода и дальнейшего лучшего понимания, 
# я бы посоветовал использовать Docstring.
# Учитывая, что это тестовое задание, в будующем может пригадиться часть 
# написанного тут кода, и тогда комментарии с Docstring помогут лучше 
# ориентироваться в старом, даже уже забытом, коде
import datetime as dt

class Record:
    # Если date может и не быть, то лучше всё таки указывать date=None
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # 1-е не правильно указаны скобки во время переноса. Они должны 
        # иметь следующий вид:
        # 
        # variable = (
        #   value
        # )
        # 
        # 2-е не верно произведён перенос if else. Он должен иметь 
        # следующий вид:
        # 
        # variable = (
        #   value1
        #   if сondition
        #   else value2
        # )
        # 
        # а лучше
        # 
        # variable = value1
        #   if сondition
        #   else value2
        # 
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)
        # Зависит конечно от задачи, но я бы рекомендовал добавить 
        # return с некоторым значением,чтобы пользователю возвращался 
        # некий отклик и он мог понять, отработал ли данный 
        # функционал, или нет.

    def get_today_stats(self):
        today_stats = 0
        # 1-е В качестве переменной было использованно имя класса
        # 2-е Все переменные должны начинаться с маленькой быквы 
        for Record in self.records:
            # dt.datetime.now().date() используется каждую итерацию, 
            # что не корректно. Лучше создать переменную и вынести
            # её за цикл, и уже сравнивать с ней, как было сделанно 
            # в функции get_week_stats
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # здесь я бы порекоммендовал искользовать конструкцию вида
            # if value1 <= value2 < value3:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий - это хорошо, но он только здесь и малоинформативный.
    # Рекомендую воспользоваться Docstring.
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Неинформативное название переменной. Не ясно ни что в ней, 
        # ни формат содержащихся данных
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Использование f-string без необходимости (строка 91).
            # Не рекомендую использовать '\'. Лучше уж '+'
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Скобки здесь лишние
            return('Хватит есть!')


class CashCalculator(Calculator):
    # 1-е для целочисленных переменных, используется int.
    # Если используешь float, то лучше о объевить соответствующе - 60.0
    # 2-е раз USD_RATE и EURO_RATE написанны большими буквами, то я 
    # их как const значения, что не очень вяжется с ежедневней смены курса
    # валют. Это является не очень гибким решением задачи.
    # 3-е Неинформативные комментирии в валютам (Если тебе это поможет, то можно оставить)
    # Чтобы не награмождать в дальнейшем (строки 125-134)
    # код условиями (конструкциями if... elif... else...)
    # я бы порекомендовал использовать словарь, ключи которых тип валюты,
    # значение - словарь с данными курса валюты и с корректным типом и уже
    # к данному словарю обращаться для получение данных.
    # Это позволит не изменять код get_today_cash_remained при добавлении 
    # новых валют и облегчит читаемость
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # USD_RATE и EURO_RATE уже есть в экземпляре класса. Стоит либо удрать 
    # их из класса, или из функции(рекомендую этот вариант)    
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # На мой взгляд, эта переменная лишняя.
        # Проще просто сзменить в логике значение переменной currency
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # На строке 125 обращаются к одной переменной, а на 128,131 - 
        # другой, хотя они и имеют одно и то же значение переменной.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Вместо присвоения указано сравнение
            cash_remained == 1.00
            currency_type = 'руб'
        # Для улучшения читаемости кода, я бы рекомендовал отделить логику 
        # пробелом от вывода
        if cash_remained > 0:
            # Рекомендую исполдьзовать одну стилитику написания кода. 
            # (использовать или f-string[рекомендуется] или format)
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Рекомендуется исподьзовать f-string 
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # 1-е Переопределениефенкции необходимо только в случае изменения логики.
    # Здесь же вызывается только родительская функция.
    # 2-е Данная функция ничего не вернёт, т.к. нет return, что ещё и ломает логику.
    def get_week_stats(self):
        super().get_week_stats()
        
# Рекомендации по итогу - ознакомиться с Docstring, PEP 8, делать пробелы в коде и 
# больше комментировать 
