import math


def calculate_transformer_values(
    txt: float,
    txt2: float,
    txt3: float,
    txt4: float,
    txt5: float,
    txt6: float,
    txt7: float,
    txt8: float,
    txt9: float,
    txt10: float,
    txt11: float,
    txt12: float,
) -> dict:
    if not -1 <= txt10 <= 1:
        raise ValueError("PF (txt10) debe estar entre -1 y 1")
    if txt3 == 0 or txt5 == 0 or txt9 == 0:
        raise ValueError("txt3, txt5 y txt9 deben ser distintos de 0")

    senphi = math.sin(math.acos(txt10))
    txt9irasteoricas = txt2 / txt3

    vueltas_por_capa = int(txt8 * 3.14 / (txt7 + 0.5))
    if vueltas_por_capa <= 0:
        raise ValueError("La geometría produce 0 vueltas por capa")

    capas = math.ceil(txt9irasteoricas / txt9 / vueltas_por_capa)

    diam_int = int(txt8 - (2 * (capas * (txt7 + 0.5))))
    diam_ext = int(txt8 + (2 * txt12) + (2 * (capas * (txt7 + 0.5))))
    diametro_medio_nucleo = txt8 + (0.7 + txt7 + 0.12 + 0.5) * 2 + txt12
    longitud = diametro_medio_nucleo * 3.14159 / 1000
    desarrollo_medio_alambre = (txt11 + txt12) * 2 + 0.7 * 4 + (txt7 + 0.12) * 2
    seccion_alambre = (txt7**2) * 3.14159 / 4
    resistenciaconductor = 0.0172 * desarrollo_medio_alambre * txt9irasteoricas / txt9 / seccion_alambre / 1000

    tension_secundaria = txt / txt3
    area_nucleo_cm2 = (txt11 * txt12 * txt6) * 10 ** (-2)
    induccion = tension_secundaria / txt9 / 4.44 / txt5 / area_nucleo_cm2 * 10**4

    if induccion > 0.5:
        h = 11.852 * induccion**2 - 4.026 * induccion + 9.1573
    else:
        h = 15.49 * induccion**0.6309

    if induccion < 0.163:
        ctecorr = 794.39 * induccion**4 - 566.01 * induccion**3 + 138.27 * induccion**2 - 13.63 * induccion + 1.7174
    elif induccion < 1.0977:
        ctecorr = 1.279
    else:
        ctecorr = (
            -62.4817 * induccion**6
            + 482.9707 * induccion**5
            - 1523.8608 * induccion**4
            + 2512.1181 * induccion**3
            - 2284.8936 * induccion**2
            + 1088.765 * induccion
            - 211.3421
        )

    io = h * longitud / txt9irasteoricas / ctecorr * 1.1
    errorimag = io / txt3 * 100
    area_nucleo_m2 = txt11 * txt12 * txt6 * 10 ** (-6)
    peso_chapa = area_nucleo_m2 * longitud * 7.65 * 1000

    if induccion > 0.15:
        corrientedeperdidas = (
            (
                0.1429 * induccion**6
                - 0.4415 * induccion**5
                + 0.4754 * induccion**4
                - 0.1727 * induccion**3
                + 0.2914 * induccion**2
                + 0.0652 * induccion
                - 0.006
            )
            * peso_chapa
            / tension_secundaria
        )
    else:
        corrientedeperdidas = 0

    erroripderdidas = corrientedeperdidas / txt3 * 100
    corrientetotalcircmag = (io**2 + corrientedeperdidas**2) ** 0.5
    errordemodulo_a = (-(errorimag * senphi + erroripderdidas * txt10)) + (txt9irasteoricas / txt9 - 1) * 100
    errorde_angulo = (ctecorr * txt10 - corrientetotalcircmag * senphi) * 20
    induccion_a_txt4 = tension_secundaria * txt4 / txt9irasteoricas / txt9 / 4.44 / txt5 / area_nucleo_cm2 * 10**4
    consumo_interno = (txt3**2) * resistenciaconductor

    return {
        "pesochapa": peso_chapa,
        "Induccion": induccion,
        "Io": io,
        "errorimag": errorimag,
        "errordemoduloA": errordemodulo_a,
        "errordeAngulo": errorde_angulo,
        "ConsumoInterno": consumo_interno,
        "H": h,
        "Longitud": longitud,
        "ctecorr": ctecorr,
        "DiamInt": diam_int,
        "Diamext": diam_ext,
        "Induccionatxt4": induccion_a_txt4,
    }
