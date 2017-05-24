from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv
import os
from os import environ
from django import forms
from django.db import models as dmodels
from operator import attrgetter
from datetime import datetime
from datetime import timedelta

author = 'Stefan Häussler, Anita Klotz, Manuel Schneckenreither'

doc = """
Lead Time Syndrome Experiment.
"""

# define debug variable
debug = environ.get('OTREE_PRODUCTION') in {None, '', '0'}


class Period(models.Model):
    "Holds information about a period"

    nr = models.IntegerField(primary_key=True, null=False) # period number
    start = models.IntegerField(null=False) # period Date start
    end = models.IntegerField(null=False)   # period Date end
    # per_date = models.DateField()           # date

    def __str__(self):
        return str(self.nr) + ": " + str(self.start) + " until " + str(self.end)


class Constants(BaseConstants):
    name_in_url = 'lts'
    players_per_group = None
    test_round_ID = -3          # ID for first period of test rounds
    release_last_week_ID = 0    # ID for last weeks release


    # Test data
    test_round_length = 3       # round to play for each test round
    max_test_rounds = 15        # maximum number of test rounds
    test_timeout = 300          # seconds until test is over

    test_period = 1

    # rounds
    exp_rounds = 2             # number of experiment rounds

    # plus 1 for round in which releases of last week are given
    num_rounds = max_test_rounds + 1 + exp_rounds

    # background colors
    bgcolor_trial_phase = "#8fbc8f"
    bgcolor_prep_phase = "#20b2aa"
    bgcolor_exec_phase = "#9acd32"

    # names of phases
    name_trial_phase ="Probephase"
    name_prep_phase = "Vorbereitungsphase"
    name_exec_phase = "Durchführungsphase"

    costs_wip = c(5)            # costs for wip per period and order
    costs_fgi = c(5)            # costs for fgi per period and order
    costs_bo = c(15)            # costs for back-orders per period and order

    rush_order_days = 11        # iff order.due-order.arrival <= rush_order_days
                                # then the order is an rush order


class Order(models.Model):
    order_id = models.IntegerField(null=False)                  # id
    participant_id = models.IntegerField(null=False, default=0) # participant_id
    nr = models.IntegerField()                                  # order number as
                                                                # shown to
                                                                # participant
    arrival = models.IntegerField()                             # arrival date
                                                                # (Note: date not
                                                                # period)
    due = models.IntegerField()                                 # due date (Note:
                                                                # date not period)
    full_processing_time = models.FloatField()                  # processing time
    time_until_finished = models.FloatField()                   # used later on
    release_date = models.FloatField(default=None)              # release date
                                                                # (Note: date not
                                                                # period). Is
                                                                # beginning of
                                                                # period.
    is_processing = models.BooleanField(default=False, null=False)
    fgi_arrived_date = models.FloatField(default=None) # arrival date at fgi
    sent_date = models.FloatField(default=None)        # sent date (Node: date not
                                                       # period)

    from_test_round = models.BooleanField(null=False,default=True)


    class Meta:
        "defines that this tuple must uniquely occur only once"
        unique_together = (("order_id", "participant_id", "from_test_round"),)

    def set_release(self, release_date):
        self.release_date = release_date

    def get_order_id(self):
        return self.order_id

    def is_rush_order(self):
        "Returns a Boolean weather this order is a rush order or not."
        return self.due - self.arrival <= Constants.rush_order_days


    def set_participant_id(self, participant_id):
        self.participant_id = participant_id

    def __str__(self):
        return str(self.order_id) + "(" + str(self.nr) + "): " + \
          (",".join(str(v) for v in [self.participant_id, self.arrival,
                                     self.due, self.full_processing_time,
                                     self.time_until_finished, self.release_date,
                                     self.fgi_arrived_date, self.sent_date,
                                     self.from_test_round]))


class Particip(models.Model):
    "Own participant object, for holding several information."

    particip_id = models.IntegerField(primary_key=True, null=False)
    orders = models.ManyToManyField(Order,
                                    through='Membership',
                                    through_fields=('particip', 'order'))
    in_current_period = models.IntegerField(default=1)
    test_time_left = models.IntegerField(default=0)


    def __str__(self):
        return "Id: " + str(self.particip_id) + " in period " + \
            str(self.in_current_period) + "with orders: " + str(self.orders)


class Membership(models.Model):
    "This class defines association of participant and its orders."

    particip = models.ForeignKey(Particip, on_delete=dmodels.CASCADE)
    order = models.ForeignKey(Order, on_delete=dmodels.CASCADE)


class Costs(models.Model):
    wip = models.CurrencyField(default=0) # work in process
    fgi = models.CurrencyField(default=0) # finished goods inventory
    bo = models.CurrencyField(default=0)  # back order costs

    def __str__(self):
        return "WIP: " + str(self.wip) + ", FGI: " + str(self.fgi) + \
            ", BO: " + str(self.bo)


class Subsession(BaseSubsession):
    "Multiple subsession (rounds) combine to one session"

    def before_session_starts(self):

        if self.round_number == 1:
            testStart = 1
            testEnd = 10
            for i in range(Constants.test_round_ID,0):
                p = Period(i, testStart, testEnd) # must have id 0
                p.save()
                testStart += 10
                testEnd += 10
            p = Period(Constants.release_last_week_ID, -9, 0) # must have id -1
            p.save()
            file_per = "./doc/data/Perioden.csv"

            with open(file_per, 'r') as csvfile:
                periods = []
                for p in list(csv.DictReader(csvfile, dialect='excel', delimiter=';')):
                    periods.append(Period(nr=int(p.get('id')),
                                          start=int(p.get('start')),
                                          end=int(p.get('end'))))
                    periods = sorted(periods, key=attrgetter('nr')) # sort by nr
                for period in periods:
                    period.save()   # save to db

        # set is test round
        test_round = False
        release_last_week = False
        for p in self.get_players():
            p.test_round = False
            p.release_last_week_round = False
            if self.round_number <= Constants.max_test_rounds:
                test_round = True
                p.test_round = True
            elif self.round_number == Constants.max_test_rounds+1:
                release_last_week = True
                p.release_last_week_round = True

        # create costs, save in db and associate to player, further set period
        for p in self.get_players():
            csts = Costs(wip=0, fgi=0, bo=0)
            csts.save()
            p.costs = csts
            if test_round:
                p.period = Period.objects.get(nr=(self.round_number % Constants.test_round_ID)-1)
            elif release_last_week:
                p.period = Period.objects.get(nr=Constants.release_last_week_ID)
            else:
                p.period = Period.objects.get(nr=self.round_number-Constants.max_test_rounds-1)

        # load corresponding data from files or previous rounds
        if self.round_number == 1 or \
           self.round_number == Constants.max_test_rounds+1 or \
           self.round_number == Constants.max_test_rounds+2:
            # first round of test or release from last week or first round of real
            # exp


            for p in self.get_players():
                # set starting flow_time
                if release_last_week:
                    p.flow_time = self.session.config['intro_beg_flow_time']
                else:
                    p.flow_time = self.session.config['start_flow_time']

            # LOAD PARTICIP OBJECT
            if self.round_number != 1:
                for p in self.get_players():
                    particip = Particip.objects.get(particip_id=p.participant.id)
                    p.particip = particip # set the participant to be able to link
                                          # to the data

            # CREATE PARTICIP OBJECT,ORDERS AND SAVE TO DATABASE
            if self.round_number == 1:

                # Fetch current period
                cur_period = 1
                if test_round:
                    cur_period = Constants.test_round_ID
                elif release_last_week:
                    cur_period = Constants.release_last_week_ID

                # set particip reference for newly generated player object
                for p in self.get_players():
                    particip = Particip(particip_id=p.participant.id,
                                        in_current_period=cur_period,
                                        test_time_left=Constants.test_timeout)
                    particip.save()
                    if debug:
                        print("Particip object was created: ", particip)

                    p.particip = particip # set the participant to be able to link to
                                          # the data


                # ["arrival","due","baz","id"]
                file_dem = self.session.config['file_dem']

                # load demand and convert to corresponding data structures
                print(os.path.abspath(file_dem))
                with open(file_dem, 'r') as csvfile:
                    demands = []
                    demandsTest = []
                    for d in list(csv.DictReader(csvfile, dialect='excel', delimiter=';')):
                        demands.append(Order(order_id=int(d.get('id')),
                                             # participant_id=participants_id,
                                             arrival=int(d.get('arrival')),
                                             due=int(d.get('due')),
                                             full_processing_time=float(d.get('baz')),
                                             time_until_finished=float(d.get('baz')),
                                             from_test_round=False
                        ))
                        demandsTest.append(Order(order_id=int(d.get('id')),
                                             # participant_id=participants_id,
                                             arrival=int(d.get('arrival')),
                                             due=int(d.get('due')),
                                             full_processing_time=float(d.get('baz')),
                                             time_until_finished=float(d.get('baz')),
                                             from_test_round=True
                        ))
                    if debug:
                        print("Demand is as follows:")
                        for d in demands:
                            print(d)


                    # load starting wip
                    # start_wip = self.session.config['start_wip']

                    num_test_orders=self.session.config['num_test_orders']
                    test_date_arr_move=self.session.config['test_date_arr_move']
                    test_date_due_move=self.session.config['test_date_due_move']

                    # add demand to player
                    if test_round:
                        demandsTest.reverse()
                        demandsTest = demandsTest[:num_test_orders]
                        demandsTest.reverse()
                        for d in demandsTest:
                            if d.is_rush_order():
                                test_date_due_rush_move=self.session.config['test_date_due_rush_move']
                                d.due -= test_date_due_rush_move
                            else:
                                d.due -= test_date_due_move
                            d.arrival -= test_date_arr_move

                    for o in demandsTest:
                        o.set_participant_id(p.participant.id)
                        print("order: ", o)
                        print("self.round_number: ", self.round_number)
                        print("test_round: ", test_round)
                        o.save()
                        memb = Membership(particip=p.particip, order=o)
                        memb.save()

                    for o in demands:
                        o.set_participant_id(p.participant.id)
                        print("order: ", o)
                        print("self.round_number: ", self.round_number)
                        print("test_round: ", test_round)
                        print("HERE")
                        o.save()
                        memb = Membership(particip=p.particip, order=o)
                        memb.save()


                # add starting wip
                # for p in self.get_players():
                #     # add starting wip to player
                #     for (n, oid, ar, du, fpt, tuf, rd, ip, fad, sd) in start_wip:
                #         o = Order(nr=n,
                #                   order_id=oid,
                #                   arrival=ar,
                #                   due=du,
                #                   full_processing_time=fpt,
                #                   time_until_finished=tuf,
                #                   release_date=rd,
                #                   is_processing=ip,
                #                   fgi_arrived_date=fad,
                #                   sent_date=sd,
                #                   from_test_round=False
                #                  )
                #         o.set_participant_id(p.participant.id)
                #         o.save()
                #         memb = Membership(particip=p.particip, order=o)
                #         memb.save()


        else:
            print("self.round_number: ", self.round_number)
            # set particip object
            for p in self.get_players():
                particip = Particip.objects.get(particip_id=p.participant.id)
                # particip.save()
                p.particip = particip # set the participant to be able to link to
                                      # the data

                # set whether this is a testround or not
                # if self.round_number <= Constants.max_test_rounds:
                #     p.test_round = True
                # else:
                #     p.test_round = False

                # p.save()              # save info to player object


            # move data from previous rounds
            # for p in self.get_players():
            #     if debug:
            #         print("Particip object was loaded: ", particip)
            #     print("New orders: ")
            #     for order in p.particip.orders.all():
            #         print(order)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    costs = models.ForeignKey(Costs, on_delete=dmodels.CASCADE, null=True)
    particip = models.ForeignKey(Particip, on_delete=dmodels.CASCADE, null=True)
    period = models.ForeignKey(Period, on_delete=dmodels.CASCADE, default=1)
    flow_time = models.FloatField(default=None)
    click_show = models.IntegerField(default=0)
    test_round = models.BooleanField(default=True)
    release_last_week_round = models.BooleanField(default=False)
