import datetime
import time


# Создает списки lats и lons, содержащие значения mlat и mlt соответственно из словарей в coordinates.
# Удаляет дубликаты и сортирует значения lats и lons в порядке возрастания.
# Вычисляет разницу между первым и вторым элементами списка lats и сохраняет ее в lat_diff.
# Вычисляет начальное значение begin как среднее между последним элементом lats, деленным на два, и lat_diff.
# Вычисляет конечное значение end как среднее между последним элементом lats и lat_diff.
# Используя numpy.arange, генерирует значения lat в диапазоне от begin до end с шагом lat_diff.
# Вложенным циклом проходит по каждому lat и lon и создает словарь fix с соответствующими значениями mlat,
# mlt и value равным 0.
# Добавляет словарь fix в список coordinates.
# Возвращает обновленный список coordinates.




def date_to_year(date: datetime.datetime) -> float:
    """

    :param date: рассматриваемая дата
    :return: десятичное значение года
    """

    def sinceEpoch(date):  # returns seconds since epoch
        return time.mktime(date.timetuple())

    s = sinceEpoch

    year = date.year
    startOfThisYear = datetime.datetime(year=year, month=1, day=1)
    startOfNextYear = datetime.datetime(year=year + 1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed / yearDuration

    return date.year + fraction


print(date_to_year(datetime.datetime(year=2023, month=12, day=1)))
