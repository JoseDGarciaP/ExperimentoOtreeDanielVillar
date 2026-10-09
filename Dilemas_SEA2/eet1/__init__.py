from otree.api import *
import random


author = 'Felix Holzmeister'

doc = """
Staircase risk elicitation task as proposed by Falk et al. (2016), Working Paper.
Adaptado a oTree 5 (formato __init__.py) a partir de la versión anterior con models.py / pages.py.
"""


# ******************************************************************************************************************** #
# *** CONSTANTES (antes config.py)
# ******************************************************************************************************************** #
class C(BaseConstants):
    # número de pasos del procedimiento de escalera
    NUM_CHOICES = 3

    OPTION_B = 5000
    OTHER_A_1 = 6500
    PROBABILITY = 100

    # pago inicial de la Opción A en la primera elección
    PAYOFF_A = 5000

    # aumento/disminución inicial del pago de la Opción A
    DELTA_1 = -1000

    # opciones de apariencia (iguales al código original)
    INDIFFERENCE = False
    BUTTONS = True
    PROGRESS_BAR = True
    INSTRUCTIONS = True
    RESULTS = False

    # oTree
    NAME_IN_URL = 'eet1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = NUM_CHOICES


# ******************************************************************************************************************** #
# *** SUBSESSION
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    # lista de pagos de la Opción A, fila de cambio implícita y loterías del pago adicional:
    #   - lotería de rol: se paga lo de quien envía o lo de quien recibe (50/50)
    #   - lotería de situación: cuál de las 6 situaciones (1-3 en eet1, 4-6 en eet2) se paga
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.vars['icl_payoffA_1'] = [C.PAYOFF_A]
            p.participant.vars['icl_switching_row_1'] = 2 ** C.NUM_CHOICES
            p.participant.vars['eet_rol_pagado'] = random.choice(['envia', 'recibe'])
            p.participant.vars['eet_round_to_pay'] = random.randint(1, 6)


# ******************************************************************************************************************** #
# *** GROUP
# ******************************************************************************************************************** #
class Group(BaseGroup):
    pass


# ******************************************************************************************************************** #
# *** PLAYER
# ******************************************************************************************************************** #
class Player(BasePlayer):
    payoff_relevant = models.StringField()
    payoffA = models.CurrencyField()
    choice = models.StringField()
    switching_row_1 = models.IntegerField()


# ******************************************************************************************************************** #
# *** FUNCIONES (antes métodos de Player / Subsession)
# ******************************************************************************************************************** #
def fmt(value):
    """Formato de dinero igual al original: $6,500"""
    return "$" + format(int(value), ',d')


def set_choice_eet(player: Player):
    if player.round_number == player.participant.vars['eet_round_to_pay']:
        player.participant.vars['eet_choice'] = player.choice


def set_payoffA_eet(player: Player):
    if player.round_number == player.participant.vars['eet_round_to_pay']:
        player.participant.vars['eet_payoffA'] = player.payoffA


def set_eet(player: Player):
    set_choice_eet(player)
    set_payoffA_eet(player)


def set_payoffA(player: Player):
    pv = player.participant.vars

    # pago de la Opción A de esta ronda
    player.payoffA = pv['icl_payoffA_1'][player.round_number - 1]

    # pago de la Opción A para la siguiente elección
    if not player.round_number == C.NUM_CHOICES:
        if player.choice == 'A':
            pv['icl_payoffA_1'].append(
                pv['icl_payoffA_1'][player.round_number - 1] + C.DELTA_1 / 2 ** (player.round_number - 1)
            )
        elif player.choice == 'B':
            pv['icl_payoffA_1'].append(
                pv['icl_payoffA_1'][player.round_number - 1] - C.DELTA_1 / 2 ** (player.round_number - 1)
            )

    # fila de cambio implícita
    player.in_round(3).switching_row_1 = int(pv['icl_switching_row_1'])


def update_switching_row(player: Player):
    if player.choice == 'B':
        player.participant.vars['icl_switching_row_1'] -= 2 ** (C.NUM_CHOICES - player.round_number)
    elif player.choice == 'I':
        player.participant.vars['icl_switching_row_1'] /= 2


def common_vars():
    return {
        'optionB': fmt(C.OPTION_B),
        'otherA_1': fmt(C.OTHER_A_1),
    }


# ******************************************************************************************************************** #
# *** PÁGINAS
# ******************************************************************************************************************** #
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['choice']

    @staticmethod
    def is_displayed(player: Player):
        previous_choices = [p.field_maybe_none('choice') for p in player.in_previous_rounds()]
        return 'I' not in previous_choices

    @staticmethod
    def vars_for_template(player: Player):
        total = C.NUM_CHOICES
        page = player.round_number
        progress = page / total * 100
        return dict(
            common_vars(),
            page=page,
            total=total,
            progress=progress,
            payoffA=fmt(player.participant.vars['icl_payoffA_1'][page - 1]),
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # primero se actualiza la fila de cambio y luego se guarda (set_payoffA la anota en switching_row_1),
        # para que incluya también la elección de esta ronda
        update_switching_row(player)
        set_payoffA(player)
        set_eet(player)


page_sequence = [Decision]

if C.INSTRUCTIONS:
    page_sequence.insert(0, Instructions)
