from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import dill as pickle                     # for pickling functions


class PaymentInfo(Page):

    # form_model = models.Player
    # form_fields = ['auszahlung']

    def vars_for_template(self):
        participant = self.participant
        payfun = pickle.loads(self.player.subsession.session.config['payment_fun'])
        csts = self.participant.vars['sum_costs']
        csts_last_week = self.player.subsession.session.config['costs_lastweek']
        self.player.auszahlung = payfun(csts-csts_last_week)


        return {
            'redemption_code': participant.label or participant.code,
            'sum_costs': "{0:.2f}".format(csts).replace(".",","),
            'payment': "{0:.2f}".format(payfun(csts-csts_last_week)).replace(".",","),
            'costs_lastweek': csts_last_week,
            'benchmark': self.player.subsession.session.config['benchmark'],
            'actual_costs': "{0:.2f}".format(csts-self.player.subsession.session.config['costs_lastweek']).replace(".",","),
            'code': participant.code,
        }


page_sequence = [PaymentInfo]
