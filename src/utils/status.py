from django.db import models


class Gender(models.TextChoices):
    NONE = '', 'None'
    MALE = 'ma', 'Male'
    FEMALE = 'fe', 'Female'

class PersonCategory(models.TextChoices):
    NONE = '', 'None'
    ALL = 'all', 'All'
    MAN = 'mn', 'Man'
    WOMEN = 'wn', 'Women'
    BABY = 'ba', 'Baby'

class Status1(models.TextChoices):
    ACTIVE = 'ac', 'Active'
    NOTACTIVE = 'na', 'Not Active'
    ARCHIVE = 'ar', 'Archive'
    BANNED = 'bn', 'Banned'


class ReciveStatus(models.TextChoices):
    ACTIVE = 'ac', 'Active'
    WAITING = 'wt', 'Waiting'
    RECIVED = 'rc', 'Recived'
    REJECTED = 'rj', 'Rejected'


class AdStatus(models.TextChoices):
    ACTIVE = 'ac', 'Active'
    WAITING = 'wt', 'Waiting'
    NOTACTIVE = 'na', 'Not Active'
    ARCHIVE = 'ar', 'Archive'