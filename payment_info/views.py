from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import dill as pickle                     # for pickling functions


class PaymentInfo(Page):

    def vars_for_template(self):
        participant = self.participant
        payfun = pickle.loads(self.player.subsession.session.config['payment_fun'])
        csts = self.participant.vars['sum_costs']

        return {
            'redemption_code': participant.label or participant.code,
            'sum_costs': "{0:.2f}".format(csts).replace(".",","),
            'payment': "{0:.2f}".format(payfun(csts)).replace(".",","),
            'costs_lastweek': self.player.subsession.session.config['costs_lastweek'],
            'benchmark': self.player.subsession.session.config['benchmark'],
            'actual_costs': "{0:.2f}".format(csts-self.player.subsession.session.config['costs_lastweek']).replace(".",","),
        }


page_sequence = [PaymentInfo]
