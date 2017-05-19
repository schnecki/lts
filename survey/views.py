from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class Demographics(Page):

    form_model = models.Player
    form_fields = [# 'country', übersetzen!!!
                   'age',
                   'gender',
                   'edu',
                   'faculity',
                   'participate']

class RiskAttitude(Page):
    
    form_model = models.Player
    form_fields = ['risk']


class Personality(Page):
    form_model = models.Player
    form_fields = ["big_five_{}".format(i) for i in range(1,15)]


class HowTo(Page):
    form_model = models.Player
    form_fields = ['how_to']

class End(Page):
    pass


page_sequence = [
    End,
    HowTo,
    RiskAttitude,
    Personality,
    Demographics]
