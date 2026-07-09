from otree.api import *
import random
import json
from collections import Counter

c = cu

doc = 'Etapa inicial donde toma lugar un debate entre dos participantes'

class C(BaseConstants):
    NAME_IN_URL = 'debate'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10000)
    FAVOR = 'A FAVOR DE DENUNCIAR'
    CONTRA = 'EN CONTRA DE DENUNCIAR'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    treatment = models.BooleanField()
    has_arrived = models.BooleanField(initial=False)
    arg_a_favor = models.LongStringField(label='Escriba su argumento, debe escribir como mínimo 5 palabras:')
    arg_en_contra = models.LongStringField(label='Escriba su argumento, debe escribir como mínimo 5 palabras:')
    rep_a_favor = models.LongStringField(label='Escriba su respuesta, debe escribir como mínimo 5 palabras:')
    rep_en_contra = models.LongStringField(label='Escriba su respuesta, debe escribir como mínimo 5 palabras:')
    arg_cal_afavor = models.LongStringField()
    arg_cal_contra = models.LongStringField()

class Player(BasePlayer):
    agree = models.BooleanField()
    
    consentimiento = models.BooleanField(
        choices=[
            [True, 'Sí acepto participar.'], 
            [False, 'No acepto participar.']
            ],
        label='¿Aceptar términos?', widget=widgets.RadioSelect)
    
    posicion_afin = models.BooleanField(
        choices=[[True, 'A favor'], [False, 'En contra']],
        label='¿Deberían los estudiantes seguir denunciando las actividades ilegales que están contaminando la Ciénaga?', widget=widgets.RadioSelect)
    
    exp_emp = models.IntegerField(
        choices=[
            [1, 'Consideré las consecuencias que puede tener esta situación para los estudiantes.'], 
            [2, 'Imaginé cómo me sentiría si estuviera en el lugar de los estudiantes.'],
            [3, 'Pensé en cómo pueden sentirse los estudiantes y los demás afectados por esta situación.'],
            [4, 'Me sentí incómodo al pensar en los riesgos que enfrentan los estudiantes al denunciar.']
            ],
        label='¿Cómo eligió su posición?', widget=widgets.RadioSelect)
    
    posicion_final = models.IntegerField(
        choices=[[1, 'Muy socialmente inapropiada'], [2, 'Socialmente inapropiada'], [3, 'Socialmente apropiada'], [4, 'Muy socialmente apropiada']],
        label='¿Qué tan socialmente apropiado cree que es la decisión de los estudiantes de seguir denunciando las actividades ilegales que están contaminando la Ciénaga?', 
        widget=widgets.RadioSelect)
    
    calificacion_usted = models.IntegerField()
    calificacion_pareja = models.IntegerField()
    calificacion_jugador_afavor = models.IntegerField()
    calificacion_jugador_encontra = models.IntegerField()
    calificacion_otros = models.IntegerField()
    pago_cal_usted = models.IntegerField()
    pago_aprobacion_social = models.IntegerField()
    descrip_calificacion = models.LongStringField(label="Describa cómo valoró la calidad de su argumentación y la de su pareja")

### Functions ###
def creating_session(self):
    num_grupos = len(self.get_groups())
    treatments = [1]*(num_grupos // 2) + [0]*(num_grupos // 2)
    random.shuffle(treatments)
    for grupo, treatment in zip(self.get_groups(), treatments):
        grupo.treatment = treatment
    for group in self.get_groups():
        for player in group.get_players():
            if (player.id_in_group == 1):
                player.agree = random.choice([True, False])
            else:
                player.agree = not player.get_others_in_group()[0].agree

def set_argumento(self:Subsession):
    groups = self.get_groups() # Obtiene todos los grupos
    num_groups = len(groups)  # Número total de grupos
    # Para los tratados
    for i in range(0, num_groups, 2):  # Recorre los grupos de 2 en 2
        if i + 1 < num_groups:  # Verifica que haya un grupo para intercambiar
            group1 = groups[i]  # Primer grupo
            group2 = groups[i + 1]  # Segundo grupo
                
                # Jugador 1 del primer grupo recibe el argumento a favor del jugador 1 del segundo grupo
            group1.arg_cal_afavor = group2.arg_a_favor
                # Jugador 1 del segundo grupo recibe el argumento a favor del jugador 1 del primer grupo
            group2.arg_cal_afavor = group1.arg_a_favor

                # Jugador 2 del primer grupo recibe el argumento en contra del jugador 2 del segundo grupo
            group1.arg_cal_contra = group2.arg_en_contra
                # Jugador 2 del segundo grupo recibe el argumento en contra del jugador 2 del primer grupo
            group2.arg_cal_contra = group1.arg_en_contra

def set_pagocalificacion(player:Subsession):
    groups = player.get_groups() # Obtiene todos los grupos
    num_groups = len(groups)  # Número total de grupos
    # Para los tratados
    for i in range(0, num_groups, 2):  # Recorre los grupos de 2 en 2
        if i + 1 < num_groups:  # Verifica que haya un grupo para intercambiar
            group1 = groups[i]  # Primer grupo
            group2 = groups[i + 1]  # Segundo grupo
            g1p1 = group1.get_player_by_id(1)
            g1p2 = group1.get_player_by_id(2)
            g2p1 = group2.get_player_by_id(1)
            g2p2 = group2.get_player_by_id(2)
            if g1p1.agree == 1:
                ### Definir pagos del jugador 1 y 2 del primer grupo
                g1p1.calificacion_otros = g2p1.calificacion_jugador_afavor + g2p2.calificacion_jugador_afavor
                g1p1.pago_cal_usted = g1p1.calificacion_usted + g1p2.calificacion_pareja + g1p1.calificacion_otros
                g1p2.calificacion_otros = g2p1.calificacion_jugador_encontra + g2p2.calificacion_jugador_encontra
                g1p2.pago_cal_usted = g1p2.calificacion_usted + g1p1.calificacion_pareja + g1p2.calificacion_otros
                ### Definir pagos del jugador 1 y 2 del segundo grupo
                g2p1.calificacion_otros = g1p1.calificacion_jugador_afavor + g1p2.calificacion_jugador_afavor
                g2p1.pago_cal_usted = g2p1.calificacion_usted + g2p2.calificacion_pareja + g2p1.calificacion_otros
                g2p2.calificacion_otros = g1p1.calificacion_jugador_encontra + g1p2.calificacion_jugador_encontra
                g2p2.pago_cal_usted = g2p2.calificacion_usted + g2p1.calificacion_pareja + g2p2.calificacion_otros
            else:
                g1p1.calificacion_otros = g2p1.calificacion_jugador_encontra + g2p2.calificacion_jugador_encontra
                g1p1.pago_cal_usted = g1p1.calificacion_usted + g1p2.calificacion_pareja + g1p1.calificacion_otros
                g1p2.calificacion_otros = g2p1.calificacion_jugador_afavor + g2p2.calificacion_jugador_afavor
                g1p2.pago_cal_usted = g1p2.calificacion_usted + g1p1.calificacion_pareja + g1p2.calificacion_otros
                ### Definir pagos del jugador 1 y 2 del segundo grupo
                g2p1.calificacion_otros = g1p1.calificacion_jugador_encontra + g1p2.calificacion_jugador_encontra
                g2p1.pago_cal_usted = g2p1.calificacion_usted + g2p2.calificacion_pareja + g2p1.calificacion_otros
                g2p2.calificacion_otros = g1p1.calificacion_jugador_afavor + g1p2.calificacion_jugador_afavor
                g2p2.pago_cal_usted = g2p2.calificacion_usted + g2p1.calificacion_pareja + g2p2.calificacion_otros       

def set_calcular_moda_global(self:Subsession):
        # Obtiene todas las respuestas de todos los jugadores en la subsesión
        respuestas = [p.posicion_final for p in self.get_players()]
        # Cuenta las ocurrencias de cada respuesta
        conteo_respuestas = Counter(respuestas)
        # Obtiene la respuesta con mayor frecuencia (moda)
        moda = conteo_respuestas.most_common(1)[0][0]
        return moda

### Pages ###
class Bienvenida(Page):
    pass

class Consentimiento(Page):
    form_model = 'player'
    form_fields = ['consentimiento']
    @staticmethod
    # Método para personalizar el flujo de avance
    def before_next_page(self:Player, timeout_happened):
        # Si el jugador responde "No", lo mantenemos en la misma página
        if not self.consentimiento:
            self._is_displayed = True  # Mantener en la misma página
    
    # Condición para mostrar el mensaje en la página
    def error_message(self, values):
        if values['consentimiento'] is False:
            return "Por favor levante su mano y espere las indicaciones de los encargados."

class Inst_iniciales(Page):    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento

class Lectura_Dilema(Page):
    form_model = 'player'
    form_fields = ['posicion_afin', 'exp_emp']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento

class Inicio_debate(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento

class Afavor(Page):
    form_model = 'group'
    form_fields = ['arg_a_favor']
    timeout_seconds = 5*60

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.agree == 1
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['argumento_a_favor'] = player.group.arg_a_favor

class Encontra(Page):
    form_model = 'group'
    form_fields = ['arg_en_contra']
    timeout_seconds = 5*60
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.agree == 0
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['argumento_en_contra'] = player.group.arg_en_contra
    
class WaitForPostura(WaitPage):
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento

class Leer_argumento(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento

class Replica_afavor(Page):
    form_model = 'group'
    form_fields = ['rep_a_favor']
    timeout_seconds = 5*60
    
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        if player.consentimiento and group.treatment == 1 and player.agree == 0:
            return True
        elif player.consentimiento and group.treatment == 0 and player.agree == 1:
            return True
        else:
            return False

class Replica_encontra(Page):
    form_model = 'group'
    form_fields = ['rep_en_contra']
    timeout_seconds = 5*60
    
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        if player.consentimiento and group.treatment == 1 and player.agree == 1:
            return True
        elif player.consentimiento and group.treatment == 0 and player.agree == 0:
            return True
        else:
            return False

class WaitForPostura2(WaitPage):
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento
    
class Leer_argumento_replica(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento

class Espera_Argumentos_a_calificar(WaitPage):
    body_text = 'Por favor espera a que los demás participantes terminen para continuar con la etapa'
    wait_for_all_groups = True

    def is_displayed(player: Player):
        return player.consentimiento

class Posicion_final(Page):
    form_model = 'player'
    form_fields = ['posicion_final']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento
    
    def before_next_page(player:Player, timeout_happened):
        return set_argumento(player.subsession)

class Instr_calificacion(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento
    
class Calificacion(Page):
    form_model = 'player'
    form_fields = ['calificacion_usted', 'calificacion_pareja', 
                'calificacion_jugador_afavor', 'calificacion_jugador_encontra']
    
    def is_displayed(player: Player):
        return player.consentimiento

    def vars_for_template(player: Player):
        group = player.group
        agree = player.agree
        if agree == 1:
            argumento_usted = group.arg_a_favor
            argumento_pareja = group.arg_en_contra
        else:
            argumento_usted = group.arg_en_contra
            argumento_pareja = group.arg_a_favor
        return dict(
            argumento_usted = argumento_usted,
            argumento_pareja = argumento_pareja,
            arg_otro_afavor = group.arg_cal_afavor,
            arg_otro_encontra = group.arg_cal_contra, 
        )
    
class Espera_Argumentos_a_calificar2(WaitPage):
    body_text = 'Por favor espera a que los demás participantes terminen para continuar con la etapa'
    wait_for_all_groups = True

    def is_displayed(player: Player):
        return player.consentimiento

class Siguiente_etapa(Page):
    form_model = 'player'
    form_fields = ['descrip_calificacion']
    @staticmethod
    def vars_for_template(player: Player):
        set_pagocalificacion(player.subsession)
        otro = player.get_others_in_group()[0]
        pago_jugador = player.pago_cal_usted
        return dict(
            otro = otro,
            su_calif = player.calificacion_usted,
            calif_pareja = otro.calificacion_pareja,
            calif_otros = player.calificacion_otros,
            pago_jugador = pago_jugador
        )
    
    def is_displayed(player: Player):
        return player.consentimiento
    
    def before_next_page(player:Player, timeout_happened):
        moda_respuestas = set_calcular_moda_global(player.subsession)
        if moda_respuestas == player.posicion_final:
            player.pago_aprobacion_social = 4000
        else:
            player.pago_aprobacion_social = 0
        player.participant.vars['pago_aprobacion_social'] = player.pago_aprobacion_social
        player.participant.vars['pago_cal_usted'] = player.pago_cal_usted
             
class Agradecimiento(Page):
    
    @staticmethod
    def is_displayed(player: Player):
        return not player.consentimiento
    
    @staticmethod
    def vars_for_template(player: Player):
        return { 
            'mensaje_agradecimiento': 'Gracias por tu tiempo. Lamentamos que no puedas continuar con el experimento.'
        }

page_sequence = [
    Bienvenida, 
    Consentimiento, 
    Inst_iniciales, 
    Lectura_Dilema, 
    Inicio_debate, 
    Afavor,
    Encontra, 
    WaitForPostura, 
    Leer_argumento, 
    Replica_afavor, 
    Replica_encontra,
    WaitForPostura2,
    Leer_argumento_replica,
    Espera_Argumentos_a_calificar,
    Posicion_final,
    Instr_calificacion,
    Calificacion,
    Espera_Argumentos_a_calificar2,
    Siguiente_etapa,
    Agradecimiento
]
