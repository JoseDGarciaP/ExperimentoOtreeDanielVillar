from otree.api import *
import json

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'results'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    SHOWFEE = 10000

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    p_selection_1 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Sueño y fantaseo, con cierta regularidad, acerca de las cosas que me podrían suceder."
    )
    p_selection_2 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="A menudo tengo sentimientos tiernos y de preocupación hacia la gente menos afortunada que yo."
    )
    p_selection_3 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="A menudo me cuesta ver las cosas desde el punto de vista de otras personas."
    )
    p_selection_4 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="A veces no me siento muy preocupado por otras personas cuando tienen problemas."
    )
    p_selection_5 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Verdaderamente me identifico con los sentimientos de los personajes de una novela."
    )
    p_selection_6 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="En situaciones de emergencia me siento aprensivo e incómodo."
    )
    p_selection_7 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Normalmente soy objetivo cuando veo una película u obra de teatro y no me involucro completamente."
    )
    p_selection_8 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Intento tener en cuenta cada una de las partes (opiniones) en un conflicto antes de tomar una decisión."
    )
    p_selection_9 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Cuando veo que a alguien se le toma el pelo, tiendo a protegerlo."
    )
    p_selection_10 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Normalmente siento desesperanza cuando estoy en medio de una situación muy emotiva."
    )
    p_selection_11 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="A menudo intento comprender mejor a mis amigos imaginándome cómo ven ellos las cosas (poniéndome en su lugar)."
    )
    p_selection_12 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Me resulta raro implicarme completamente en un buen libro o película."
    )
    p_selection_13 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Cuando veo a alguien herido, tiendo a permanecer calmado."
    )
    p_selection_14 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Las desgracias de otros normalmente no me molestan mucho."
    )
    p_selection_15 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Si estoy seguro de que tengo la razón en algo, no pierdo tiempo escuchando los argumentos de los demás."
    )
    p_selection_16 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Después de ver una obra de teatro o cine, me he sentido como si fuera uno de los personajes."
    )
    p_selection_17 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Cuando estoy en una situación emocionalmente tensa, me asusto."
    )
    p_selection_18 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Cuando veo a alguien que está siendo tratado injustamente, a veces no siento ninguna compasión por él."
    )
    p_selection_19 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Normalmente soy bastante eficaz al ocuparme de emergencias."
    )
    p_selection_20 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="A menudo estoy bastante afectado emocionalmente por cosas que veo que ocurren."
    )
    p_selection_21 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Pienso que hay dos partes para cada cuestión e intento tener en cuenta ambas partes."
    )
    p_selection_22 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Me describiría como una persona bastante sensible."
    )
    p_selection_23 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Cuando veo una buena película, puedo muy fácilmente situarme en el lugar del protagonista."
    )
    p_selection_24 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="A menudo pierdo el control durante las emergencias."
    )
    p_selection_25 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Cuando estoy disgustado con alguien, normalmente intento ponerme en su lugar por un momento."
    )
    p_selection_26 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Cuando estoy leyendo una historia interesante o una novela, imagino cómo me sentiría si los acontecimientos de la historia me sucedieran a mí."
    )
    p_selection_27 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Cuando veo a alguien que necesita urgentemente ayuda en una emergencia, me derrumbo."
    )
    p_selection_28 = models.PositiveIntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Antes de criticar a alguien, intento imaginar cómo me sentiría si estuviera en su lugar."
    )
    age = models.IntegerField()
    gender_sex = models.IntegerField(choices=[[0, "Masculino"], [1, "Femenino"], [2, "Otro"]])
    major = models.IntegerField(
        choices=[
            [1, "Administración de Empresas"],
            [2, "Administración de Negocios Internacionales"],
            [3, "Administración en Logística y Producción"],
            [4, "Antropología"],
            [5, "Arquitectura"],
            [6, "Artes"],
            [7, "Artes Liberales en Ciencias Sociales"],
            [8, "Biología"],
            [9, "Ciencia Política y Gobierno"],
            [10, "Ciencias del Sistema Tierra"],
            [11, "Creación"],
            [12, "Diseño"],
            [13, "Economía"],
            [14, "Enfermería"],
            [15, "Emprendimiento"],
            [16, "Filosofía"],
            [17, "Finanzas y Comercio Internacional"],
            [18, "Fisioterapia"],
            [19, "Fonoaudiología"],
            [20, "Gestión y Desarrollo Urbanos"],
            [21, "Historia"],
            [22, "Ingeniería Biomédica"],
            [23, "Ingeniería Industrial"],
            [24, "Ingeniería Electrónica"],
            [25, "Ingeniería de Sistemas"],
            [26, "Jurisprudencia"],
            [27, "Licenciatura en Filosofía"],
            [28, "Marketing y Negocios Digitales"],
            [29, "Medicina"],
            [30, "Periodismo y Opinión Pública"],
            [31, "Psicología"],
            [32, "Relaciones Internacionales"],
            [33, "Sociología"],
            [34, "Teatro Musical"],
            [35, "Terapia Ocupacional"],
            [36, "Lenguas Modernas"],
            [37, "Narrativas Digitales"],
            [38, "Ingeniería Mecánica"],
            [39, "Ingeniería Química"],
            [40, "Química"],
            [41, "Física"],
            [42, "Medicina Veterinaria"],
            [43, "Geología"],
            [44, "Filología"],
            [45, "Estudios Globales"],
            [46, "Ciencias de la computación"],
            [47, "Cine y televisión"],
            [48, "Trabajo social"],
            [49, "Nutrición"],
            [50, "Zootecnia"],
            [51, "Ingeniería sanitaria"],
            [52, "Ingeniería Ambiental"],
            [53, "Administración Ambiental"],
            [54, "Comunicación Social"],
            [55, "Ingeniería catastral"],
            [56, "Ingeniería civil"],
            [57, "Ingeniería eléctrica"],
            [58, "Ingeniería mecatrónica"],
            [59, "Ingeniería forestal"],
            [60, "Matemáticas aplicadas y computación"],
            [61, "Matemáticas"],
            [62, "Contaduría"],
            [63, "Otra"]
        ]
    )
    semester = models.IntegerField(
        choices=[
            [0, "Egresado"],
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4],
            [5, 5],
            [6, 6],
            [7, 7],
            [8, 8],
            [9, 9],
            [10, 10],
            [11, 11],
            [12, 12],
            [13, "más de 12"],
        ]
    )
    stratum = models.IntegerField(
        choices=[[0, "No estratificado"], [1, "1"], [2, "2"], [3, "3"], [4, "4"], [5, "5"], [6, "6"]]
    )
    experiments = models.IntegerField(choices=[[0, "No"], [1, "Sí"]])
    income = models.IntegerField(
        min=1000,
    )
    mother_educ = models.IntegerField(
        choices=[[1, "Ninguno"],
                [2, "Primaria"],
                [3, "Secundaria/Bachillerato"],
                [4, "Educación universitaria/tecnológica"],
                [5, "Posgrado"],
                [0, "No sabe"]]
    )
    father_educ = models.IntegerField(
        choices=[[1, "Ninguno"],
                [2, "Primaria"],
                [3, "Secundaria/Bachillerato"],
                [4, "Educación universitaria/tecnológica"],
                [5, "Posgrado"],
                [0, "No sabe"]]
    )
    income_stair = models.IntegerField(widget=widgets.RadioSelect,
                                        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
    )
    risk_measure = models.IntegerField(widget=widgets.RadioSelect,
                                        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
    )
    G_trust = models.IntegerField(widget=widgets.RadioSelect,
                                    choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    patience = models.IntegerField(widget=widgets.RadioSelect,
                                        choices=[1, 2, 3, 4, 5]
    )
    punish_justice = models.IntegerField(
        choices=[[4, "Mucho"],
                [3, "Algo"],
                [2, "Poco"],
                [1, "Nada"]]
    )
    payoff_complete = models.IntegerField()

# PAGES

class Survey(Page):
    form_model = 'player'
    form_fields = [
        'p_selection_1', 'p_selection_2', 'p_selection_3', 'p_selection_4', 'p_selection_5', 
        'p_selection_6', 'p_selection_7', 'p_selection_8', 'p_selection_9', 'p_selection_10', 
        'p_selection_11', 'p_selection_12', 'p_selection_13', 'p_selection_14', 'p_selection_15', 
        'p_selection_16', 'p_selection_17', 'p_selection_18', 'p_selection_19', 'p_selection_20', 
        'p_selection_21', 'p_selection_22', 'p_selection_23', 'p_selection_24', 'p_selection_25', 
        'p_selection_26', 'p_selection_27', 'p_selection_28'
    ]

    def vars_for_template(self:Player):
        return {
            'descriptions': [
                "No me describe bien",
                "Me describe un poco",
                "Me describe bien",
                "Me describe bastante bien",
                "Me describe muy bien"
            ]
        }

class Survey_2(Page):
    form_model = 'player'
    form_fields = ["age", "gender_sex", "major", "semester", "stratum", "experiments", "income",
                    "mother_educ", "father_educ", "income_stair", "risk_measure", "G_trust", 
                    "patience", "punish_justice"
    ]
    
    def before_next_page(player:Player, timeout_happened):
        pago_aprobacion_social = player.participant.vars.get('pago_aprobacion_social', 0)
        pago_cal_usted = player.participant.vars.get('pago_cal_usted', 0)
        final_payoff = player.participant.vars.get('final_payoff', 0)
        player.payoff_complete = C.SHOWFEE + int(final_payoff) + pago_cal_usted + pago_aprobacion_social

class Final(Page):
    form_model = 'player'
    
    @staticmethod
    def vars_for_template(player: Player):
        pago_aprobacion_social = player.participant.vars.get('pago_aprobacion_social', 0)
        pago_cal_usted = player.participant.vars.get('pago_cal_usted', 0)
        final_payoff = player.participant.vars.get('final_payoff', 0)
        selected_round = player.participant.vars.get('selected_round', 0)
        payoff_complete = player.payoff_complete
        return{
            'pago_aprobacion_social': pago_aprobacion_social,
            'pago_cal_usted':pago_cal_usted,
            'final_payoff':final_payoff,
            'selected_round':selected_round,
            'payoff_complete': payoff_complete
            
        }

page_sequence = [
    Survey,
    Survey_2, 
    Final
]
