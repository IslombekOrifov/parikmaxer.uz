from django.db import models


class Gender(models.TextChoices):
        NONE = '', 'None'
        MALE = 'ma', 'Male'
        FEMALE = 'fe', 'Female'

class PersonCategory(models.TextChoices):
    NONE = '', 'None'
    ALL = 'all', 'All'
    MALE = 'ma', 'Male'
    FEMALE = 'fe', 'Female'
    BABY = 'ba', 'Baby'

class PostStatus(models.TextChoices):
    ACTIVE = 'ac', 'Active'
    NOTACTIVE = 'na', 'Not Active'
    ARCHIVE = 'ar', 'Archive'
    BANNED = 'bn', 'Banned'


class OrderStatus(models.TextChoices):
    ACTIVE = 'ac', 'Active'
    WAITING = 'wt', 'Waiting'
    RECIVED = 'rc', 'Recived'
    REJECTED = 'rj', 'Rejected'


class AdStatus(models.TextChoices):
    ACTIVE = 'ac', 'Active'
    WAITING = 'wt', 'Waiting'
    NOTACTIVE = 'na', 'Not Active'
    ARCHIVE = 'ar', 'Archive'