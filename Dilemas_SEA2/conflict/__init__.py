from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'PD_Chat'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4
    
    MUTUAL_COOPERATE = 16000
    MUTUAL_DEFECT = 4000
    X_VALUES = [8000, 8000, 24000, 24000]
    Y_VALUES = [8000, 0, 8000, 0]
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

def creating_session(self):
    for group in self.get_groups():
        group.selected_round = random.randint(1, C.NUM_ROUNDS)
        r_list = random.sample(C.ORDER, len(C.ORDER))
        group.levels = ",".join(map(str, r_list))

def set_payoffs(group: Group):
        for p in group.get_players():
            set_payoff(p)

def get_payoff_for_round(player: Player, other_player_choice: bool):
    round_number = player.round_number
    level_index = round_number - 1 
    
    if player.cooperate and other_player_choice:
        return C.MUTUAL_COOPERATE
    elif not player.cooperate and not other_player_choice:
        return C.MUTUAL_DEFECT
    elif player.cooperate and not other_player_choice:
        return C.Y_VALUES[level_index]
    else:
        return C.X_VALUES[level_index]

def other_player(player: Player):
    return player.get_others_in_group()[0]

def set_payoff(player: Player):
    other = other_player(player)
    player.payoff = get_payoff_for_round(player, other.cooperate)

### Pages ###
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    def before_next_page(player:Player, timeout_happened):
        player.participant.vars['levels'] = player.group.levels
        player.participant.vars['selected_round'] = player.group.selected_round

class Decision(Page):
    form_model = 'player'
    form_fields = ['cooperate']

    @staticmethod
    def vars_for_template(player: Player):
        level = player.participant.vars['levels']
        level = level.split(",")
        level = level[player.round_number - 1]
        level = int(level)
        return {
            'level_number': player.round_number,
            'x_value': C.X_VALUES[level],
            'y_value': C.Y_VALUES[level],
            'my_nickname': "Participante {}".format(player.id_in_group)
        }

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class TotalResult(Page):
    form_model = 'player'
    form_fields = ['descrip_cooperate']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        selected_round = player.participant.vars['selected_round']
        selected_round_payoff = player.in_round(selected_round).payoff
        
        return {
            "selected_round": selected_round,
            "final_payoff": selected_round_payoff
        }
    
    def before_next_page(player: Player, timeout_happened):
        
        player.participant.vars['final_payoff'] = player.in_round(player.participant.vars['selected_round']).payoff

page_sequence = [Introduction, Decision, ResultsWaitPage, TotalResult]