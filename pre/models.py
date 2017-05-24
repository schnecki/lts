from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from lts import models as lts

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'pre'
    players_per_group = None
    num_rounds = 1

    # settings
    days_last_release = 10      # number of days when last release was

    # background colors
    bgcolor_test_phase = "#a2cd5a"
    name_test_phase = "Testaufgabenphase"


class Subsession(BaseSubsession):
    wip = models.CurrencyField(default=0)
    fgi = models.CurrencyField(default=0)
    bo =  models.CurrencyField(default=0)

    def before_session_starts(self):
        self.wip = self.session.config['intro_end_csts_wip']
        self.fgi = self.session.config['intro_end_csts_fgi']
        self.bo = self.session.config['intro_end_csts_bo']

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    triesTestQ1 = models.IntegerField(default=0)
    triesTestQ2 = models.IntegerField(default=0)
    triesTestQ3 = models.IntegerField(default=0)
    triesTestQ4 = models.IntegerField(default=0)
    triesTestQ5 = models.IntegerField(default=0)


