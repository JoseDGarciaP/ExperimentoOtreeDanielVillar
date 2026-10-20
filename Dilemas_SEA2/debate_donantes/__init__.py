from otree.api import *
import random
from collections import Counter

import donantes

doc = """
Versión de la etapa de debate para participantes sobrantes (no completan un grupo de 4).
Cada participante juega solo: el argumento y la réplica de su "pareja", y los argumentos
de la "otra pareja" que debe calificar, vienen de perfiles_donantes.csv.
Usa las mismas plantillas de la app 'debate' (template_name), así que lo que vea el
participante es idéntico a la sesión normal.
"""


class C(BaseConstants):
    NAME_IN_URL = 'debate_d'
    PLAYERS_PER_GROUP = None   # cada participante juega solo; ver creating_session
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
            [True, 'Sí. He leído y entendido la información contenida en este documento; por lo tanto, voluntariamente acepto participar en esta investigación.'],
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

    # Trazabilidad: qué donantes se usaron con este participante (participant.code del CSV)
    donante_pareja = models.StringField()
    donante_gemelo = models.StringField()
    calif_recibida_pareja = models.IntegerField(doc='Calificación que el donante-pareja dio a su pareja original')


### Funciones ###
def creating_session(subsession: Subsession):
    players = subsession.get_players()
    # Cada participante en su propio grupo de 1
    subsession.set_group_matrix([[p] for p in players])

    # Tratamientos lo más balanceados posible (con 3 personas: 2 de uno y 1 del otro, al azar)
    tratamientos = ([0, 1] * len(players))[:len(players)]
    random.shuffle(tratamientos)

    for p, t in zip(players, tratamientos):
        g = p.group
        g.treatment = bool(t)
        p.agree = random.choice([True, False])

        par = donantes.pareja(t, p.agree)
        gem = donantes.gemelo(t, p.agree)
        p.donante_pareja = par['codigo']
        p.donante_gemelo = gem['codigo']
        p.participant.vars['donante_pareja'] = par['codigo']

        # Se llenan SOLO los textos que escribió la "pareja"; los del participante quedan vacíos
        # para que su formulario aparezca en blanco.
        if p.agree:
            g.arg_en_contra = par['arg_en_contra']
        else:
            g.arg_a_favor = par['arg_a_favor']
        if campo_replica_propia(p) == 'rep_a_favor':
            g.rep_en_contra = par['rep_en_contra']
        else:
            g.rep_a_favor = par['rep_a_favor']

        # Argumentos de la "otra pareja" a calificar: los mismos que calificó la pareja donante
        g.arg_cal_afavor = par['arg_cal_afavor']
        g.arg_cal_contra = par['arg_cal_contra']


def campo_replica_propia(player: Player):
    """Igual que en 'debate': quién escribe la réplica a favor o en contra según tratamiento y posición."""
    t = 1 if player.group.treatment else 0
    if (t == 1 and not player.agree) or (t == 0 and player.agree):
        return 'rep_a_favor'
    return 'rep_en_contra'


def set_pagocalificacion(player: Player):
    """
    Pago por calificaciones = su propia calificación
                            + la que su pareja (donante) dio a su pareja original
                            + las que recibió de la otra pareja el donante que estuvo en su mismo rol.
    """
    par = donantes.pareja(player.group.treatment, player.agree)
    gem = donantes.gemelo(player.group.treatment, player.agree)
    player.calif_recibida_pareja = par['calificacion_pareja']
    player.calificacion_otros = gem['calificacion_otros']
    player.pago_cal_usted = player.calificacion_usted + par['calificacion_pareja'] + player.calificacion_otros


def moda_posicion_final(player: Player):
    """Moda entre las posiciones finales de los 4 donantes y la del propio participante."""
    respuestas = [d['posicion_final'] for d in donantes.todos()] + [player.posicion_final]
    return Counter(respuestas).most_common(1)[0][0]


def minimo_cinco_palabras(texto):
    if texto is None or len(texto.split()) < 5:
        return "Debe escribir como mínimo 5 palabras."


### Páginas (mismas plantillas que la app 'debate') ###
class Bienvenida(Page):
    template_name = 'debate/Bienvenida.html'


class Consentimiento(Page):
    template_name = 'debate/Consentimiento.html'
    form_model = 'player'
    form_fields = ['consentimiento']

    @staticmethod
    def error_message(player: Player, values):
        if values['consentimiento'] is False:
            return "Por favor levante su mano y espere las indicaciones de los encargados."


class Inst_iniciales(Page):
    template_name = 'debate/Inst_iniciales.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Lectura_Dilema(Page):
    template_name = 'debate/Lectura_Dilema.html'
    form_model = 'player'
    form_fields = ['posicion_afin']

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Exp_emp(Page):
    template_name = 'debate/Exp_emp.html'
    form_model = 'player'
    form_fields = ['exp_emp']

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Inicio_debate(Page):
    template_name = 'debate/Inicio_debate.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Afavor(Page):
    template_name = 'debate/Afavor.html'
    form_model = 'group'
    form_fields = ['arg_a_favor']
    timeout_seconds = 5*60

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.agree == 1

    @staticmethod
    def error_message(player: Player, values):
        return minimo_cinco_palabras(values['arg_a_favor'])

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['argumento_a_favor'] = player.group.field_maybe_none('arg_a_favor')


class Encontra(Page):
    template_name = 'debate/Encontra.html'
    form_model = 'group'
    form_fields = ['arg_en_contra']
    timeout_seconds = 5*60

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.agree == 0

    @staticmethod
    def error_message(player: Player, values):
        return minimo_cinco_palabras(values['arg_en_contra'])

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['argumento_en_contra'] = player.group.field_maybe_none('arg_en_contra')


class Leer_argumento(Page):
    template_name = 'debate/Leer_argumento.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Replica_afavor(Page):
    template_name = 'debate/Replica_afavor.html'
    form_model = 'group'
    form_fields = ['rep_a_favor']
    timeout_seconds = 5*60

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and campo_replica_propia(player) == 'rep_a_favor'

    @staticmethod
    def error_message(player: Player, values):
        return minimo_cinco_palabras(values['rep_a_favor'])


class Replica_encontra(Page):
    template_name = 'debate/Replica_encontra.html'
    form_model = 'group'
    form_fields = ['rep_en_contra']
    timeout_seconds = 5*60

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and campo_replica_propia(player) == 'rep_en_contra'

    @staticmethod
    def error_message(player: Player, values):
        return minimo_cinco_palabras(values['rep_en_contra'])


class Leer_argumento_replica(Page):
    template_name = 'debate/Leer_argumento_replica.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Posicion_final(Page):
    template_name = 'debate/Posicion_final.html'
    form_model = 'player'
    form_fields = ['posicion_final']

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Instr_calificacion(Page):
    template_name = 'debate/Instr_calificacion.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Calificacion(Page):
    template_name = 'debate/Calificacion.html'
    form_model = 'player'
    form_fields = ['calificacion_usted', 'calificacion_pareja',
                   'calificacion_jugador_afavor', 'calificacion_jugador_encontra']

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        # Si el tiempo se acabó sin escribir, el campo queda vacío: se muestra en blanco
        a_favor = group.field_maybe_none('arg_a_favor') or ''
        en_contra = group.field_maybe_none('arg_en_contra') or ''
        if player.agree:
            argumento_usted, argumento_pareja = a_favor, en_contra
        else:
            argumento_usted, argumento_pareja = en_contra, a_favor
        return dict(
            argumento_usted=argumento_usted,
            argumento_pareja=argumento_pareja,
            arg_otro_afavor=group.arg_cal_afavor,
            arg_otro_encontra=group.arg_cal_contra,
        )


class Siguiente_etapa(Page):
    template_name = 'debate/Siguiente_etapa.html'
    form_model = 'player'
    form_fields = ['descrip_calificacion']

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento

    @staticmethod
    def vars_for_template(player: Player):
        set_pagocalificacion(player)
        return dict(
            su_calif=player.calificacion_usted,
            calif_pareja=player.calif_recibida_pareja,
            calif_otros=player.calificacion_otros,
            pago_jugador=player.pago_cal_usted,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.field_maybe_none('pago_cal_usted') is None:
            set_pagocalificacion(player)
        player.pago_aprobacion_social = 4000 if moda_posicion_final(player) == player.posicion_final else 0
        player.participant.vars['pago_aprobacion_social'] = player.pago_aprobacion_social
        player.participant.vars['pago_cal_usted'] = player.pago_cal_usted


class Agradecimiento(Page):
    template_name = 'debate/Agradecimiento.html'

    @staticmethod
    def is_displayed(player: Player):
        return not player.consentimiento


# Sin páginas de espera: nadie depende de otra persona real
page_sequence = [
    Bienvenida,
    Consentimiento,
    Inst_iniciales,
    Lectura_Dilema,
    Exp_emp,
    Inicio_debate,
    Afavor,
    Encontra,
    Leer_argumento,
    Replica_afavor,
    Replica_encontra,
    Leer_argumento_replica,
    Posicion_final,
    Instr_calificacion,
    Calificacion,
    Siguiente_etapa,
    Agradecimiento,
]
