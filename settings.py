import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings
import dill as pickle                     # for pickling functions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# don't share this with anybody.
SECRET_KEY = 'm632ehh7x5avbjql)hdtfx5=b#bsflz9-dtmmw$b$t%l6s8-yt'

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False


# e.g. en, de, fr, it, ja, zh-hans
# see: https./docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'de'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# Static files
STATIC_URL = '/static/'


# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
oTree games
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http./docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24,  # 7 days
    # 'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

# TEMPLATES = [
# {
#     'DIRS': [(os.path.join(BASE_DIR, 'templates')),],
# }


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.000,
    'participation_fee': 4.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'lts1',
        'szenario': 1,
        'display_name': "Lead Time Syndrome Szenario 1 (KoKoNoRo)",
        'num_demo_participants': 1,
        'app_sequence': ['pre',
                         'lts',
                         'survey',
                         'payment_info'
        ],
        'file_dem': "./doc/data/KoKoNoRo.csv",
        'start_flow_time': 6.75,
        'flow_time_last_year': 6.75,
        'start_wip_count': 2,

        'payment_fun': pickle.dumps(lambda csts: 4+10*20/(20+csts)),
        'benchmark': 0,

        # Starting information before intro
        'intro_beg_csts_wip': 0,
        'intro_beg_csts_fgi': 0,
        'intro_beg_csts_bo':0,
        'intro_beg_flow_time': 6.75,

        # Information at end of intro (intro_end_flow_time = intro_flow_time)!
        'intro_end_csts_wip': 0,
        'intro_end_csts_fgi': 0,
        'intro_end_csts_bo':0,

        'costs_lastweek': 0,

        # test setup
        'num_test_orders': 12,  # nr of test orders taken from end of demand stream
        'test_date_arr_move': 220, # nr of days to substract from arr date for test
        'test_date_due_move': 270, # nr of days to substract from due date for test
        'test_date_due_rush_move': 220, # nr of days to subtract for rush order
                                         # from due date

    },
    {
        'name': 'lts2',
        'szenario': 2,
        'display_name': "Lead Time Syndrome Szenario 2 (KoVarNoRo)",
        'num_demo_participants': 1,
        'app_sequence': ['pre',
                         'lts',
                         'survey',
                         'payment_info'
        ],
        'file_dem': "./doc/data/KoVarNoRo.csv",
        'start_flow_time': 8.10,
        'flow_time_last_year': 13.49,
        'start_wip_count': 4,
        'payment_fun': pickle.dumps(lambda csts: 4+10*(490+20)/(csts-10+20)),
        'costs_lastweek': 10,
        'benchmark': 490,

        # Starting information before intro
        'intro_beg_csts_wip': 0,
        'intro_beg_csts_fgi': 0,
        'intro_beg_csts_bo':0,
        'intro_beg_flow_time': 7.05,

        # Information at end of intro (intro_end_flow_time = intro_flow_time)!
        'intro_end_csts_wip': 10,
        'intro_end_csts_fgi': 0,
        'intro_end_csts_bo':0,


        # test setup
        'num_test_orders': 12,  # nr of test orders taken from end of demand stream
        'test_date_arr_move': 220, # nr of days to substract from arr date for test
        'test_date_due_move': 270, # nr of days to substract from due date for test
        'test_date_due_rush_move': 220, # nr of days to subtract for rush order
                                         # from due date

    },
    {
        'name': 'lts3',
        'szenario': 3,
        'display_name': "Lead Time Syndrome Szenario 3 (KoKoRo)",
        'num_demo_participants': 1,
        'app_sequence': ['pre',
                         'lts',
                         'survey',
                         'payment_info'],
        'file_dem': "./doc/data/KoKoRo.csv",
        'start_flow_time': 6.75,
        'flow_time_last_year': 13.01,
        'start_wip_count': 4,

        'payment_fun': pickle.dumps(lambda csts: 4+10*(440+20)/(csts-10+20)),
        'costs_lastweek': 10,
        'benchmark': 440,

        # Starting information before intro
        'intro_beg_csts_wip': 0,
        'intro_beg_csts_fgi': 0,
        'intro_beg_csts_bo':0,
        'intro_beg_flow_time': 9.75,

        # Information at end of intro (intro_end_flow_time = intro_flow_time)!
        'intro_end_csts_wip': 10,
        'intro_end_csts_fgi': 0,
        'intro_end_csts_bo':0,


        # test setup
        'num_test_orders': 12,  # nr of test orders taken from end of demand stream
        'test_date_arr_move': 220, # nr of days to substract from arr date for test
        'test_date_due_move': 270, # nr of days to substract from due date for test
        'test_date_due_rush_move': 220, # nr of days to subtract for rush order
                                         # from due date

    },
    {
        'name': 'lts4',
        'szenario': 4,
        'display_name': "Lead Time Syndrome Szenario 4 (SaiKonNoRo)",
        'num_demo_participants': 1,
        'app_sequence': ['pre',
                         'lts',
                         'survey',
                         'payment_info'],
        'file_dem': "./doc/data/SaiKonNoRo.csv",
        'start_flow_time': 6.75,
        'flow_time_last_year': 17.11,
        'start_wip_count': 3,
        'payment_fun': pickle.dumps(lambda csts: 4+10*(845+20)/(csts-5+20)),
        'costs_lastweek': 5,
        'benchmark': 845,

        # Starting information before intro
        'intro_beg_csts_wip': 0,
        'intro_beg_csts_fgi': 0,
        'intro_beg_csts_bo':0,
        'intro_beg_flow_time': 26.25,

        # Information at end of intro (intro_end_flow_time = intro_flow_time)!
        'intro_end_csts_wip': 5,
        'intro_end_csts_fgi': 0,
        'intro_end_csts_bo':0,


        # test setup
        'num_test_orders': 11,  # nr of test orders taken from end of demand stream
        'test_date_arr_move': 210, # nr of days to substract from arr date for test
        'test_date_due_move': 250, # nr of days to substract from due date for test
        'test_date_due_rush_move': 220, # nr of days to subtract for rush order
                                         # from due date


    },


]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
