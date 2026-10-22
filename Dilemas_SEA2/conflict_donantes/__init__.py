from otree.api import *
import random

import donantes

doc = """
Versión de la etapa 2 (conflict) para participantes sobrantes.
Cada participante juega solo; la decisión de su "pareja" en cada situación es la que tomó,
en esa misma situación, el donante que fue su pareja en la etapa de debate.
Usa las mismas plantillas de la app 'conflict'.
"""


class C(BaseConstants):
    NAME_IN_URL = 'PD_Chat_d'
    PLAYERS_PER_GROUP = None   # cada participante juega solo; ver creating_session
    NUM_ROUNDS = 4

    MUTUAL_COOPERATE = 16000
    MUTUAL_DEFECT = 4000
    # Según las instrucciones: quien elige A recibe X y quien elige B recibe Y.
    X_VALUES = [8000, 0, 8000, 0]        # pago para quien elige A
    Y_VALUES = [8000, 8000, 24000, 24000]  # pago para quien elige B
    ORDER = [0, 1, 2, 3]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    levels = models.StringField()
    selected_round = models.IntegerField()


class Player(BasePlayer):
    cooperate = models.BooleanField(
        choices=[[True, 'A'], [False, 'B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    descrip_cooperate = models.LongStringField(label='Describa cómo eligió entre la Opción A y la Opción B')
    cooperate_partner = models.BooleanField(
        choices=[[True, 'A'], [False, 'B']],
        doc="""Other decision""",
        widget=widgets.RadioSelect,
        label='¿Qué crees que elige el otro participante en esta situación?'
    )
    cooperate_accuracy = models.IntegerField(min=0, max=100, label='¿Qué tan seguro está?')
    # Trazabilidad
    donante_pareja = models.StringField()
    cooperate_donante = models.BooleanField(doc='Decisión del donante-pareja en esta misma situación (True = A)')
    # Ganancia de esta ronda (igual que en 'conflict': no se usa player.payoff)
    pago_ronda = models.CurrencyField(initial=0)


def creating_session(subsession: Subsession):
    players = subsession.get_players()
    subsession.set_group_matrix([[p] for p in players])
    if subsession.round_number == 1:
        for group in subsession.get_groups():
            group.selected_round = random.randint(1, C.NUM_ROUNDS)
            group.levels = ",".join(map(str, random.sample(C.ORDER, len(C.ORDER))))
    else:
        for group in subsession.get_groups():
            group_r1 = group.in_round(1)
            group.selected_round = group_r1.selected_round
            group.levels = group_r1.levels


def get_level_index(player: Player):
    levels = player.participant.vars.get('levels', player.group.levels)
    return int(levels.split(",")[player.round_number - 1])


def donante_de(player: Player):
    """Donante-pareja asignado en debate_donantes."""
    codigo = player.participant.vars['donante_pareja']
    for d in donantes.todos():
        if d['codigo'] == codigo:
            return d
    raise ValueError(f'No se encontró el donante {codigo} en perfiles_donantes.csv')


def get_payoff_for_round(player: Player, other_player_choice: bool):
    level_index = get_level_index(player)
    if player.cooperate and other_player_choice:
        return C.MUTUAL_COOPERATE
    elif not player.cooperate and not other_player_choice:
        return C.MUTUAL_DEFECT
    elif player.cooperate and not other_player_choice:
        return C.X_VALUES[level_index]
    else:
        return C.Y_VALUES[level_index]


def set_payoff(player: Player):
    d = donante_de(player)
    player.donante_pareja = d['codigo']
    player.cooperate_donante = d['coopera_por_situacion'][get_level_index(player)]
    player.pago_ronda = get_payoff_for_round(player, player.cooperate_donante)


### Páginas (mismas plantillas que la app 'conflict') ###
class Introduction(Page):
    template_name = 'conflict/Introduction.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['levels'] = player.group.levels
        player.participant.vars['selected_round'] = player.group.selected_round


class Decision(Page):
    template_name = 'conflict/Decision.html'
    form_model = 'player'
    form_fields = ['cooperate', 'cooperate_partner', 'cooperate_accuracy']

    @staticmethod
    def vars_for_template(player: Player):
        level = get_level_index(player)
        return {
            'level_number': player.round_number,
            'x_value': C.X_VALUES[level],
            'y_value': C.Y_VALUES[level],
            'my_nickname': "Participante 1",
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoff(player)


class TotalResult(Page):
    template_name = 'conflict/TotalResult.html'
    form_model = 'player'
    form_fields = ['descrip_cooperate']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        selected_round = player.participant.vars['selected_round']
        return {
            "selected_round": selected_round,
            "final_payoff": player.in_round(selected_round).pago_ronda,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['final_payoff'] = player.in_round(player.participant.vars['selected_round']).pago_ronda


page_sequence = [Introduction, Decision, TotalResult]
