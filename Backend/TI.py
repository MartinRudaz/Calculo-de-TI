import math


def calculate_transformer_values(
    prestacion_va: float,
    corriente_primaria_a: float,
    corriente_secundaria_a: float,
    factor_seguridad_fs: float,
    frecuencia_hz: float,
    factor_apilado: float,
    diametro_conductor_mm: float,
    diametro_interno_mm: float,
    espiras_nucleo: float,
    factor_potencia: float,
    ancho_fleje_mm: float,
    apilado_mm: float,
) -> dict:
    if not -1 <= factor_potencia <= 1:
        raise ValueError("El factor de potencia debe estar entre -1 y 1")
    if corriente_secundaria_a == 0 or frecuencia_hz == 0 or espiras_nucleo == 0:
        raise ValueError("Corriente secundaria, frecuencia y espiras deben ser distintas de 0")

    seno_phi = math.sin(math.acos(factor_potencia))
    espiras_teoricas = corriente_primaria_a / corriente_secundaria_a

    vueltas_por_capa = int(diametro_interno_mm * 3.14 / (diametro_conductor_mm + 0.5))
    if vueltas_por_capa <= 0:
        raise ValueError("La geometría produce 0 vueltas por capa")

    cantidad_capas = math.ceil(espiras_teoricas / espiras_nucleo / vueltas_por_capa)

    diametro_interno_resultado = int(diametro_interno_mm - (2 * (cantidad_capas * (diametro_conductor_mm + 0.5))))
    diametro_externo_resultado = int(diametro_interno_mm + (2 * apilado_mm) + (2 * (cantidad_capas * (diametro_conductor_mm + 0.5))))
    diametro_medio_nucleo = diametro_interno_mm + (0.7 + diametro_conductor_mm + 0.12 + 0.5) * 2 + apilado_mm
    longitud_medio_nucleo_m = diametro_medio_nucleo * 3.14159 / 1000
    desarrollo_medio_alambre_mm = (ancho_fleje_mm + apilado_mm) * 2 + 0.7 * 4 + (diametro_conductor_mm + 0.12) * 2
    seccion_alambre_mm2 = (diametro_conductor_mm**2) * 3.14159 / 4
    resistencia_conductor_ohm = (
        0.0172 * desarrollo_medio_alambre_mm * espiras_teoricas / espiras_nucleo / seccion_alambre_mm2 / 1000
    )

    tension_secundaria_v = prestacion_va / corriente_secundaria_a
    area_nucleo_cm2 = (ancho_fleje_mm * apilado_mm * factor_apilado) * 10 ** (-2)
    induccion_tesla = tension_secundaria_v / espiras_nucleo / 4.44 / frecuencia_hz / area_nucleo_cm2 * 10**4

    if induccion_tesla > 0.5:
        intensidad_campo_h = 11.852 * induccion_tesla**2 - 4.026 * induccion_tesla + 9.1573
    else:
        intensidad_campo_h = 15.49 * induccion_tesla**0.6309

    if induccion_tesla < 0.163:
        constante_correccion = (
            794.39 * induccion_tesla**4
            - 566.01 * induccion_tesla**3
            + 138.27 * induccion_tesla**2
            - 13.63 * induccion_tesla
            + 1.7174
        )
    elif induccion_tesla < 1.0977:
        constante_correccion = 1.279
    else:
        constante_correccion = (
            -62.4817 * induccion_tesla**6
            + 482.9707 * induccion_tesla**5
            - 1523.8608 * induccion_tesla**4
            + 2512.1181 * induccion_tesla**3
            - 2284.8936 * induccion_tesla**2
            + 1088.765 * induccion_tesla
            - 211.3421
        )

    corriente_magnetizacion_a = intensidad_campo_h * longitud_medio_nucleo_m / espiras_teoricas / constante_correccion * 1.1
    error_imaginario_pct = corriente_magnetizacion_a / corriente_secundaria_a * 100
    area_nucleo_m2 = ancho_fleje_mm * apilado_mm * factor_apilado * 10 ** (-6)
    peso_chapa_kg = area_nucleo_m2 * longitud_medio_nucleo_m * 7.65 * 1000

    if induccion_tesla > 0.15:
        corriente_perdidas_a = (
            (
                0.1429 * induccion_tesla**6
                - 0.4415 * induccion_tesla**5
                + 0.4754 * induccion_tesla**4
                - 0.1727 * induccion_tesla**3
                + 0.2914 * induccion_tesla**2
                + 0.0652 * induccion_tesla
                - 0.006
            )
            * peso_chapa_kg
            / tension_secundaria_v
        )
    else:
        corriente_perdidas_a = 0

    error_perdidas_pct = corriente_perdidas_a / corriente_secundaria_a * 100
    corriente_total_circuito_magnetico_a = (corriente_magnetizacion_a**2 + corriente_perdidas_a**2) ** 0.5
    error_modulo_pct = (
        -(error_imaginario_pct * seno_phi + error_perdidas_pct * factor_potencia)
        + (espiras_teoricas / espiras_nucleo - 1) * 100
    )
    error_angulo_min = (constante_correccion * factor_potencia - corriente_total_circuito_magnetico_a * seno_phi) * 20
    induccion_a_fs_tesla = (
        tension_secundaria_v
        * factor_seguridad_fs
        / espiras_teoricas
        / espiras_nucleo
        / 4.44
        / frecuencia_hz
        / area_nucleo_cm2
        * 10**4
    )
    consumo_interno_va = (corriente_secundaria_a**2) * resistencia_conductor_ohm

    return {
        "pesochapa": peso_chapa_kg,
        "Induccion": induccion_tesla,
        "Io": corriente_magnetizacion_a,
        "errorimag": error_imaginario_pct,
        "errordemoduloA": error_modulo_pct,
        "errordeAngulo": error_angulo_min,
        "ConsumoInterno": consumo_interno_va,
        "H": intensidad_campo_h,
        "Longitud": longitud_medio_nucleo_m,
        "ctecorr": constante_correccion,
        "DiamInt": diametro_interno_resultado,
        "Diamext": diametro_externo_resultado,
        "Induccionatxt4": induccion_a_fs_tesla,
    }
