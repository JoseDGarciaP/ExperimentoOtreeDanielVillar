from otree.api import *


author = 'Felix Holzmeister'

doc = """
Staircase risk elicitation task as proposed by Falk et al. (2016), Working Paper.
Adaptado a oTree 5 (formato __init__.py) a partir de la versión anterior con models.py / pages.py.
Requiere que eet1 se haya jugado antes (usa participant.vars['eet_round_to_pay']).
"""


# ******************************************************************************************************************** #
# *** CONSTANTES (antes config.py)
# ******************************************************************************************************************** #
class C(BaseConstants):
    NUM_CHOICES = 3

    OPTION_B = 50000
    OTHER_A_2 = 35000
    PROBABILITY = 100

    PAYOFF_A = 50000
    DELTA_2 = -10000

    INDIFFERENCE = False
    BUTTONS = True
    PROGRESS_BAR = True
    INSTRUCTIONS = False
    RESULTS = True

    NAME_IN_URL = 'eet2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = NUM_CHOICES


# ******************************************************************************************************************** #
# *** SUBSESSION
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.vars['icl_payoffA_2'] = [C.PAYOFF_A]
            p.participant.vars['icl_switching_row_2'] = 2 ** C.NUM_CHOICES


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
    payoff_s = models.CurrencyField()
    payoff_r = models.CurrencyField()
    choice = models.StringField()
    switching_row_2 = models.IntegerField()
    situation = models.IntegerField()
    payoff_total = models.CurrencyField()
    payoff_resignation = models.IntegerField(min=0)
    payoff_otherPlayer = models.IntegerField(min=0)


# ******************************************************************************************************************** #
# *** FUNCIONES (antes métodos de Player / Subsession)
# ******************************************************************************************************************** #
def fmt(value):
    """Formato de dinero igual al original: $ 35,000"""
    return "$ " + format(int(value), ',d')


def set_choice_eet(player: Player):
    player.situation = player.round_number + 3
    if player.situation == player.participant.vars['eet_round_to_pay']:
        player.participant.vars['eet_choice'] = player.choice


def set_payoffA_eet(player: Player):
    player.situation = player.round_number + 3
    if player.situation == player.participant.vars['eet_round_to_pay']:
        player.participant.vars['eet_payoffA'] = player.payoffA


def set_eet(player: Player):
    set_choice_eet(player)
    set_payoffA_eet(player)


def set_payoffA(player: Player):
    pv = player.participant.vars

    player.payoffA = pv['icl_payoffA_2'][player.round_number - 1]

    if not player.round_number == C.NUM_CHOICES:
        if player.choice == 'A':
            pv['icl_payoffA_2'].append(
                pv['icl_payoffA_2'][player.round_number - 1] + C.DELTA_2 / 2 ** (player.round_number - 1)
            )
        elif player.choice == 'B':
            pv['icl_payoffA_2'].append(
                pv['icl_payoffA_2'][player.round_number - 1] - C.DELTA_2 / 2 ** (player.round_number - 1)
            )


def update_switching_row(player: Player):
    if player.choice == 'B':
        player.participant.vars['icl_switching_row_2'] -= 2 ** (C.NUM_CHOICES - player.round_number)
    elif player.choice == 'I':
        player.participant.vars['icl_switching_row_2'] /= 2


def set_payoffs(player: Player):
    pv = player.participant.vars
    current_round = player.round_number
    current_choice = player.choice

    # se calcula al terminar todas las elecciones (o si eligió "indiferente")
    if current_round == C.NUM_ROUNDS or current_choice == 'I':
        if pv['eet_choice'] == 'A':
            player.payoff_s = pv['eet_payoffA']
            if pv['eet_round_to_pay'] < 4:
                player.payoff_r = 65000
            else:
                player.payoff_r = 35000
        elif pv['eet_choice'] == 'B':
            player.payoff_s = C.OPTION_B
            player.payoff_r = C.OPTION_B
        pv['pagototal'] = int(player.payoff_s) + 15000

        # fila de cambio implícita
        player.in_round(3).switching_row_2 = int(pv['icl_switching_row_2'])

        player.payoff_total = player.payoff_r + player.payoff_s


def common_vars():
    return {
        'optionB': fmt(C.OPTION_B),
        'otherA_2': fmt(C.OTHER_A_2),
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
            page=page + 3,
            total=total,
            progress=progress,
            payoffA=fmt(player.participant.vars['icl_payoffA_2'][page - 1]),
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoffA(player)
        update_switching_row(player)
        set_eet(player)
        set_payoffs(player)


class Results(Page):
    form_model = 'player'
    form_fields = ['payoff_total', 'payoff_resignation', 'payoff_otherPlayer']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        pv = player.participant.vars
        choice_to_pay = pv['eet_round_to_pay']
        total = int(player.payoff_r + player.payoff_s)
        return dict(
            common_vars(),
            payoffA=fmt(pv['eet_payoffA']),
            choice_to_pay=choice_to_pay,
            option_to_pay=pv['eet_choice'],
            payoff_relevant=pv['eet_choice'],
            # lo que recibe la otra persona en la Opción A (antes: if choice_to_pay < 4 en la plantilla)
            other_A_paid='$65,000' if choice_to_pay < 4 else '$35,000',
            payoff_s=fmt(player.payoff_s),
            payoff_r=fmt(player.payoff_r),
            payoff_total=fmt(total),
            payoff_total_int=total,
        )


page_sequence = [Decision]

if C.INSTRUCTIONS:
    page_sequence.insert(0, Instructions)

if C.RESULTS:
    page_sequence.append(Results)
