"""
Perfiles donantes para la sesión de participantes sobrantes.

Cuando en la sala no se completa un grupo de 4, las personas que sobran juegan la
sesión "debate_conflict_donantes". Ahí cada una juega sola y su "pareja" y la "otra
pareja" se toman de respuestas reales de sesiones anteriores, guardadas en
perfiles_donantes.csv (export "all apps - wide" de oTree).

El archivo debe tener exactamente 2 parejas (4 filas):
  - una pareja con tratamiento 0 (mantiene la posición en la réplica)
  - una pareja con tratamiento 1 (cambia de posición en la réplica)
y en cada pareja un jugador con agree=1 (a favor) y otro con agree=0 (en contra).
"""
import csv
import os
from functools import lru_cache

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'perfiles_donantes.csv')


def _int(valor):
    return int(float(valor))


def _leer_fila(fila):
    """Convierte una fila del CSV en un diccionario con lo que usan las apps de donantes."""
    niveles = [int(x) for x in fila['conflict.1.group.levels'].split(',')]
    # En conflict, la ronda r muestra la situación niveles[r-1]. Se guarda la decisión
    # del donante por SITUACIÓN, para que coincida con la situación que ve el participante real.
    coopera_por_situacion = {}
    for ronda in range(1, 5):
        coopera_por_situacion[niveles[ronda - 1]] = fila[f'conflict.{ronda}.player.cooperate'] == '1'
    return dict(
        codigo=fila['participant.code'],
        sesion=fila['session.code'],
        grupo=fila['debate.1.group.id_in_subsession'],
        tratamiento=_int(fila['debate.1.group.treatment']),
        agree=_int(fila['debate.1.player.agree']),
        posicion_final=_int(fila['debate.1.player.posicion_final']),
        calificacion_pareja=_int(fila['debate.1.player.calificacion_pareja']),
        calificacion_otros=_int(fila['debate.1.player.calificacion_otros']),
        arg_a_favor=fila['debate.1.group.arg_a_favor'],
        arg_en_contra=fila['debate.1.group.arg_en_contra'],
        rep_a_favor=fila['debate.1.group.rep_a_favor'],
        rep_en_contra=fila['debate.1.group.rep_en_contra'],
        arg_cal_afavor=fila['debate.1.group.arg_cal_afavor'],
        arg_cal_contra=fila['debate.1.group.arg_cal_contra'],
        coopera_por_situacion=coopera_por_situacion,
    )


@lru_cache(maxsize=1)
def cargar():
    """Devuelve {(tratamiento, agree): perfil} y valida que estén las 4 combinaciones."""
    with open(ARCHIVO, encoding='utf-8-sig', newline='') as f:
        filas = [_leer_fila(fila) for fila in csv.DictReader(f)]

    perfiles = {}
    for p in filas:
        clave = (p['tratamiento'], p['agree'])
        if clave in perfiles:
            raise ValueError(f'perfiles_donantes.csv: hay más de un donante con tratamiento={clave[0]} y agree={clave[1]}.')
        perfiles[clave] = p

    faltan = [c for c in [(0, 0), (0, 1), (1, 0), (1, 1)] if c not in perfiles]
    if faltan:
        raise ValueError(f'perfiles_donantes.csv: faltan donantes con (tratamiento, agree) = {faltan}.')
    for t in (0, 1):
        if perfiles[(t, 0)]['grupo'] != perfiles[(t, 1)]['grupo'] or perfiles[(t, 0)]['sesion'] != perfiles[(t, 1)]['sesion']:
            raise ValueError(f'perfiles_donantes.csv: los dos donantes del tratamiento {t} deben ser de la misma pareja.')
    return perfiles


def pareja(tratamiento, agree):
    """Donante que hace de PAREJA: mismo tratamiento, posición contraria."""
    return cargar()[(int(tratamiento), 0 if agree else 1)]


def gemelo(tratamiento, agree):
    """Donante que estuvo en el MISMO rol que el participante (sus calificaciones recibidas se usan para el pago)."""
    return cargar()[(int(tratamiento), 1 if agree else 0)]


def todos():
    return list(cargar().values())
