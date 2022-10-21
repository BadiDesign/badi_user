import datetime

from unidecode import unidecode


def jalali_to_gregorian(jy, jm, jd):
    if (jy > 979):
        gy = 1600
        jy -= 979
    else:
        gy = 621
    if (jm < 7):
        days = (jm - 1) * 31
    else:
        days = ((jm - 7) * 30) + 186
    days += (365 * jy) + ((int(jy / 33)) * 8) + (int(((jy % 33) + 3) / 4)) + 78 + jd
    gy += 400 * (int(days / 146097))
    days %= 146097
    if (days > 36524):
        gy += 100 * (int(--days / 36524))
        days %= 36524
        if (days >= 365):
            days += 1
    gy += 4 * (int(days / 1461))
    days %= 1461
    if (days > 365):
        gy += int((days - 1) / 365)
        days = (days - 1) % 365
    gd = days + 1
    if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while (gm < 13):
        v = sal_a[gm]
        if (gd <= v):
            break
        gd -= v
        gm += 1
    return [gy, gm, gd]


def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gy > 1600):
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = (365 * gy) + (int((gy2 + 3) / 4)) - (int((gy2 + 99) / 100)) + (int((gy2 + 399) / 400)) - 80 + gd + g_d_m[
        gm - 1]
    jy += 33 * (int(days / 12053))
    days %= 12053
    jy += 4 * (int(days / 1461))
    days %= 1461
    if (days > 365):
        jy += int((days - 1) / 365)
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + int(days / 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + int((days - 186) / 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]


def custom_change_date(value, mode=1):
    """
    Arguments:
        value():
            Date/DateTime
        mode(int):
            Mode of Change Date
    """
    # Change Str Date to Str Persian Date
    if mode == 2:
        value = str(unidecode(str(value)))
        year, month, day = value.split('-')
        date = gregorian_to_jalali(int(year), int(month), int(day))
        string_date = "{y}/{m}/{d}".format(y=date[0], m=date[1], d=date[2])
        return string_date

    # Str Persian DateTime to DjangoDateTime
    if mode == 3:
        d = unidecode(value).split(' -- ')
        if len(d) == 1:
            d = unidecode(value).split(' ')
        y, m, day = d[0].split('/')
        hour, min, ss = d[1].split(':')
        pdate = jalali_to_gregorian(int(y), int(m), int(day))
        date_time = datetime.datetime(int(pdate[0]), int(pdate[1]), int(pdate[2]), int(hour), int(min), int(ss))
        return date_time

    # Change DjangoDateTime to PersianDateTime
    if mode == 4:
        splitter = ' '
        if 'T' in str(value):
            splitter = 'T'
        d = str(value).split(splitter)
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        time = time[0].split('.')
        hour, min, sec = time[0].split(':')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        date_time = "{y}/{m}/{d} {h}:{min}:{s}".format(y=pdate[0], m=pdate[1], d=pdate[2], h=hour, min=min, s=sec)
        return date_time

    # Change DateTime To DjangoDateTime
    if mode == 5:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        hour, min, sec = time[0].split(':')
        date_time = datetime.datetime(int(y), int(m), int(day), int(hour), int(min), int(sec))
        return date_time

    # Change Persian Date to DjangoDate
    if mode == 6:
        y, m, day = value.split('/')
        pdate = jalali_to_gregorian(int(y), int(m), int(day))
        djangodate = datetime.date(int(pdate[0]), int(pdate[1]), int(pdate[2]))
        return djangodate

    # Change DjangoDateTime to PersianMonthDay
    if mode == 7:
        monthlist = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                     'اسفند']
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        date_time = "{d} {m}".format(m=monthlist[pdate[1] - 1], d=pdate[2])
        return date_time

    # Change DjangoDateTime to PersianDateTime For Tables
    if mode == 8:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        time = time[0].split('.')
        hour, min, sec = time[0].split(':')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        date_time = "{h}:{min}:{s} {y}/{m}/{d}".format(y=pdate[0], m=pdate[1], d=pdate[2], h=hour, min=min, s=sec)
        return date_time

    # Change DjangoDateTime to Year
    if mode == 9:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        return pdate[0]

    # Change DjangoDateTime to Month
    if mode == 10:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        time = time[0].split('.')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        return pdate[1]

    if mode == 11:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        time = time[0].split('.')
        hour, min, sec = time[0].split(':')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        date_time = "{y}-{m}-{d} {h}:{min}:{s}".format(y=pdate[0], m=pdate[1], d=pdate[2], h=hour, min=min, s=sec)
        return date_time

    # 1398/3 => (1398/3/31 : 23:59:59) => DjangoDateTime
    if mode == 12:
        pdate = []
        y, m = value.split('/')
        for i in [28, 29, 30, 31]:
            if jalali_to_gregorian(int(y), int(m), i)[2] != jalali_to_gregorian(int(y), int(m) + 1, 1)[2]:
                pdate = jalali_to_gregorian(int(y), int(m), i)
        djangodate = datetime.datetime(int(pdate[0]), int(pdate[1]), int(pdate[2]), 23, 59, 59)
        return djangodate

    # 1398/3 => (1398/3/1 : 00:00:00) => DjangoDateTime
    if mode == 14:
        y, m = value.split('/')
        pdate = jalali_to_gregorian(int(y), int(m), 1)
        djangodate = datetime.datetime(int(pdate[0]), int(pdate[1]), int(pdate[2]), 00, 00, 00)
        return djangodate

    # get Current Persian Date => [ 1399 , 4 , 16 ]
    if mode == 13:
        now = datetime.datetime.now()
        return gregorian_to_jalali(now.year, now.month, now.day)
    return 0
