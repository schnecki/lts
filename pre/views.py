from otree.api import Currency as c, currency_range
from lts import models as lts
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from datetime import date, timedelta

class OrderRelease(Page):

    def vars_for_template(self):


        wip = self.player.subsession.wip
        fgi = self.player.subsession.fgi
        bo = self.player.subsession.bo
        sum_csts = wip + fgi + bo

        return {'current_day': -Constants.days_last_release,
                'player': lts.Player(costs=lts.Costs(wip=0,fgi=0,bo=0)),
                'sum_costs_object': lts.Costs(wip=wip,fgi=fgi,bo=bo),
                'sum_costs': sum_csts,

                'datetimetext': "Morgen",
                'szenario': self.player.subsession.session.config['szenario'],

                'wip': wip,
                'fgi': fgi,
                'bo': bo,
                'wipfgibo': sum_csts,
                'sum_wip': wip,
                'sum_fgi': fgi,
                'sum_bo': bo,

                'flow_time': self.player.subsession.session.config['intro_beg_flow_time'],
                'flow_time_year': self.player.subsession.session.config['flow_time_last_year'],
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):

    def vars_for_template(self):


        wip = self.player.subsession.session.config['intro_end_csts_wip']
        fgi = self.player.subsession.session.config['intro_end_csts_fgi']
        bo =  self.player.subsession.session.config['intro_end_csts_bo']
        sum_csts = wip + fgi + bo

        return {'current_day': 0,
                'player': lts.Player(costs=lts.Costs(wip=wip,fgi=fgi,bo=bo)),
                'sum_costs_object': lts.Costs(wip=wip,fgi=fgi,bo=bo),
                'sum_costs': c(sum_csts),
                'flow_time': self.player.subsession.session.config['start_flow_time'],
                'flow_time_year': self.player.subsession.session.config['flow_time_last_year'],

                'datetimetext': "Abend",

                'wip': c(wip),
                'fgi': c(fgi),
                'bo': c(bo),
                'wipfgibo': c(sum_csts),
                'sum_wip': c(wip),
                'sum_fgi': c(fgi),
                'sum_bo': c(bo),
        }


class Info(Page):
    pass

class Welcome(Page):
    pass

class WelcomeTestphase(Page):
    pass


class Test(Page):

    form_model = models.Player
    form_fields = ['triesTestQ1', 'triesTestQ2', 'triesTestQ3', 'triesTestQ4', 'triesTestQ5']


page_sequence = [
    # OrderRelease,
    # ResultsWaitPage,
    # Results,
    Welcome,
    Test,
    Info
]
