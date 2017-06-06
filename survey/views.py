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

    def vars_for_template(self):
        return { 'bgcolor': Constants.bgcolor_surv_phase,
                 'phase': Constants.name_surv_phase,
                }


class RiskAttitude(Page):

    form_model = models.Player
    form_fields = ['risk']

    def vars_for_template(self):
        return { 'bgcolor': Constants.bgcolor_surv_phase,
                 'phase': Constants.name_surv_phase,
                }

class Personality(Page):
    form_model = models.Player
    form_fields = ["big_five_{}".format(i) for i in range(1,15)]

    def vars_for_template(self):
        return { 'bgcolor': Constants.bgcolor_surv_phase,
                 'phase': Constants.name_surv_phase,
                }

class HowTo(Page):
    form_model = models.Player
    form_fields = ['how_to']

    def vars_for_template(self):
        return { 'bgcolor': Constants.bgcolor_surv_phase,
                 'phase': Constants.name_surv_phase,
                }


class Manip(Page):
    pass

class End(Page):
    pass


page_sequence = [
    End,
    HowTo,
    Manip,
    RiskAttitude,
    Personality,
    Demographics]
