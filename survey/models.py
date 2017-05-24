from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
# import floppyforms.__future__ as forms

from django_countries.fields import CountryField


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

    name_surv_phase = "Befragungsphase"
    bgcolor_surv_phase = "hsla(147, 58%, 53.3%, 0.1)"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    country = CountryField(
        verbose_name='What is your country of citizenship?')

    age = models.PositiveIntegerField(verbose_name='Ihr Alter in Jahren?',
                                      choices=range(13, 91),
                                      initial=None)

    gender = models.CharField(initial=None,
                              choices=['männlich', 'weiblich'],
                              verbose_name='Geschlecht?',
                              widget=widgets.RadioSelect())

    how_to = models.TextField()

    edu = models.CharField(initial=None,
                           verbose_name='Ihr höchster Bildungsabschluss?',
                           max_length=50,
                           choices=['Allgemein bildende Pflichtschule',
                                    'Lehrabschluss',
                                    'BMS (berufsbildende mittlere Schule)',
                                    'AHS (allgemein bildende hohere Schule)',
                                    'BHS (berufsbildende hohere Schule)',
                                    'Kolleg',
                                    'Hochschulverwandte Lehranstalten (z.B. Akademie)',
                                    'Universität/Fachhochschule'])


    faculity = models.CharField(initial=None,
                                verbose_name='Sie studieren an folgender Fakutät?',
                                max_length=50,
                                choices=['Fakultät für Architektur',
                                         'Fakultät für Betriebswirtschaft',
                                         'Fakultät für Bildungswissenschaften',
                                         'Fakultät für Biologie',
                                         'Fakultät für Chemie und Pharmazie',
                                         'Fakultät für Geo- und Atmosphärenwissenschaften',
                                         'Fakultät für Mathematik, Informatik und Physik',
                                         'Fakultät für Politikwissenschaft und Soziologie',
                                         'Fakultät für Psychologie und Sportwissenschaft',
                                         'Fakultät für Technische Wissenschaften',
                                         'Fakultät für Volkswirtschaft und Statistik',
                                         'Katholisch-Theologische Fakultät',
                                         'Philologisch-Kulturwissenschaftliche Fakultät',
                                         'Philosophisch-Historische Fakultät',
                                         'Rechtswissenschaftliche Fakultät',
                                         'School of Education ',
                                         'Sonstiges',
                                         'Ich studiere nicht'])

    participate = models.CharField(initial=None,
                                   choices=['Ja', 'Nein'],
                                   verbose_name='Möchten Sie an weiteren Experimenten teilnehmen?',
                                   widget=widgets.RadioSelect())


    risk = models.PositiveIntegerField(initial=None,
                                       widget=widgets.SliderInput(attrs={'step': '1',
                                                                         'min':'0',
                                                                         'max':'10'}))


    big_five_1 = models.PositiveIntegerField(initial=None,
                                             choices=range(1,8),
                                             verbose_name="gründlich arbeitet.",
                                             widget=widgets.RadioSelect())
    big_five_2 = models.PositiveIntegerField(initial=None,
                                             choices=range(1,8),
                                             verbose_name="kommunikativ, gesprächig ist.",
                                             widget=widgets.RadioSelect())
    big_five_3 = models.PositiveIntegerField(initial=None,
                                             choices=range(1,8),
                                             verbose_name="manchmal etwas grob zu anderen ist.",
                                             widget=widgets.RadioSelect())
    big_five_4 = models.PositiveIntegerField(initial=None,
                                             choices=range(1,8),
                                             verbose_name="originell ist, neue Ideen einbringt.",
                                             widget=widgets.RadioSelect())
    big_five_5 = models.PositiveIntegerField(initial=None,
                                             choices=range(1,8),
                                             verbose_name="sich oft Sorgen macht.",
                                             widget=widgets.RadioSelect())
    big_five_6 = models.PositiveIntegerField(initial=None,
                                             choices=range(1,8),
                                             verbose_name="zurückhaltend ist.",
                                             widget=widgets.RadioSelect())
    big_five_7 = models.PositiveIntegerField(initial=None,
                                             choices=range(1,8),
                                             verbose_name="verzeihen kann.",
                                             widget=widgets.RadioSelect())
    big_five_8 = models.PositiveIntegerField(initial=None,
                                             choices=range(1,8),
                                             verbose_name="eher faul ist.",
                                             widget=widgets.RadioSelect())
    big_five_9 = models.PositiveIntegerField(initial=None,
                                             choices=range(1,8),
                                             verbose_name="aus sich herausgehen kann, gesellig ist.",
                                             widget=widgets.RadioSelect())
    big_five_10 = models.PositiveIntegerField(initial=None,
                                              choices=range(1,8),
                                              verbose_name="künstlerische Erfahrungen schätzt.",
                                              widget=widgets.RadioSelect())
    big_five_11 = models.PositiveIntegerField(initial=None,
                                              choices=range(1,8),
                                              verbose_name="leicht nervös wird.",
                                              widget=widgets.RadioSelect())
    big_five_12 = models.PositiveIntegerField(initial=None,
                                              choices=range(1,8),
                                              verbose_name="Aufgaben wirksam und effizient erledigt.",
                                              widget=widgets.RadioSelect())
    big_five_13 = models.PositiveIntegerField(initial=None,
                                              choices=range(1,8),
                                              verbose_name="rücksichtsvoll und freundlich mit anderen umgeht.",
                                              widget=widgets.RadioSelect())
    big_five_14 = models.PositiveIntegerField(initial=None,
                                              choices=range(1,8),
                                              verbose_name="eine lebhafte Phantasie, Vorstellungen hat.",
                                              widget=widgets.RadioSelect())
    big_five_15 = models.PositiveIntegerField(initial=None,
                                              choices=range(1,8),
                                              verbose_name="entspannt ist, mit Stress gut umgehen kann.",
                                              widget=widgets.RadioSelect())
