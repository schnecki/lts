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
    form_fields = ['how_to', 'uncertainty']

    def vars_for_template(self):
        return { 'bgcolor': Constants.bgcolor_surv_phase,
                 'phase': Constants.name_surv_phase,
                }


class Manip(Page):
    form_model = models.Player
    form_fields = ['variation_demand', 'variation_throughputtime',
                   'imp_flowtime_year', 'imp_flowtime_round']


    def vars_for_template(self):
        return { 'bgcolor': Constants.bgcolor_surv_phase,
                 'phase': Constants.name_surv_phase,
                 # fields = list(form_fields),
                 # part1, part2 = fields[:2], fields[2:]
                 'part1': [self.player.variation_demand,
                           self.player.variation_throughputtime]
                }

class Manip2(Page):
    form_model = models.Player
    form_fields = ['imp_flowtime_comp',
                   'imp_costs', 'imp_cockpit_release',
                   'predict_order', 'nr_order_for_release']

    def vars_for_template(self):
        return { 'bgcolor': Constants.bgcolor_surv_phase,
                 'phase': Constants.name_surv_phase,
                 'imp_flowtime_comp_show': self.player.imp_flowtime_year != 1 and
                                           self.player.imp_flowtime_round != 1,
                 'cockpit_on': self.player.subsession.session.config['wlc_enabled'],
        }

class Manip2Cockpit(Page):

    form_model = models.Player
    form_fields = ['help_cockpit',
                   'imp_cockpit_comp',
                   'imp_cockpit_comp2',
                  ]


    def vars_for_template(self):
        return { 'bgcolor': Constants.bgcolor_surv_phase,
                 'phase': Constants.name_surv_phase,
                 'cockpit_on': self.player.subsession.session.config['wlc_enabled'],
                 'show_cockpits_questions': self.player.subsession.session.config['wlc_enabled'] and
                                            self.player.imp_cockpit_release != 1
        }

    def is_displayed(self):
        return self.player.subsession.session.config['wlc_enabled'] and \
            self.player.imp_cockpit_release != 1


class Manip3(Page):
    form_model = models.Player
    form_fields = ['release_more_necessary',
                   'release_too_many',
                   'release_to_little',
                   'comp_flowtimes_both',
                   'comp_flowtimes_rounds',
                  ]

    def vars_for_template(self):
        return { 'bgcolor': Constants.bgcolor_surv_phase,
                 'phase': Constants.name_surv_phase,
        }


class End(Page):
    pass


page_sequence = [
    End,
    HowTo,
    Manip,
    Manip2,
    Manip2Cockpit,
    Manip3,
    RiskAttitude,
    Personality,
    Demographics]
