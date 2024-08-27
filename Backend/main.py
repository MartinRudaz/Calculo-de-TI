from fastapi import FastAPI
from pydantic import BaseModel
import math
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O restringe a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],  # O restringe a métodos específicos (GET, POST, etc.)
    allow_headers=["*"],  # O restringe a encabezados específicos
)

class TransformerInput(BaseModel):
    txt: float
    txt2: float
    txt3: float
    txt4: float
    txt5: float
    txt6: float
    txt7: float
    txt8: float
    txt9: float
    txt10: float
    txt11: float
    txt12: float

@app.post("/calculate")
async def calculate_transformer(input: TransformerInput):
    senphi = math.sin(math.acos(input.txt10))
    txt9irasteoricas = input.txt2 / input.txt3
    DiamInt = int(input.txt8 - (2 * (math.ceil(txt9irasteoricas / input.txt9 / int(input.txt8 * 3.14 / (input.txt7 + 0.5))) * (input.txt7 + 0.5))))
    Diamext = int(input.txt8 + (2 * input.txt12) + (2 * (math.ceil(txt9irasteoricas / input.txt9 / int(input.txt8 * 3.14 / (input.txt7 + 0.5))) * (input.txt7 + 0.5))))
    diametromedionucleo = input.txt8 + (0.7 + input.txt7 + 0.12 + 0.5) * 2 + input.txt12
    longitud = diametromedionucleo * 3.14159 / 1000
    desarrollomedioalambre = (input.txt11 + input.txt12) * 2 + 0.7 * 4 + (input.txt7 + 0.12) * 2
    seccionalambre = (input.txt7 ** 2) * 3.14159 / 4
    resistenciaconductor = 0.0172 * desarrollomedioalambre * txt9irasteoricas / input.txt9 / seccionalambre / 1000
    carga = 1
    tensionsecundaria = input.txt / input.txt3
    areanucleocm2 = (input.txt11 * input.txt12 * input.txt6) * 10 ** (-2)
    Induccion = tensionsecundaria / input.txt9 / 4.44 / input.txt5 / areanucleocm2 * 10 ** 4

    if Induccion > 0.5:
        H = 11.852 * Induccion ** 2 - 4.026 * Induccion + 9.1573
    else:
        H = 15.49 * Induccion ** 0.6309

    if Induccion < 0.163:
        ctecorr = 794.39 * Induccion ** 4 - 566.01 * Induccion ** 3 + 138.27 * Induccion ** 2 - 13.63 * Induccion + 1.7174
    elif Induccion < 1.0977:
        ctecorr = 1.279
    else:
        ctecorr = -62.4817 * Induccion ** 6 + 482.9707 * Induccion ** 5 - 1523.8608 * Induccion ** 4 + 2512.1181 * Induccion ** 3 - 2284.8936 * Induccion ** 2 + 1088.765 * Induccion - 211.3421

    Io = H * longitud / txt9irasteoricas / ctecorr * 1.1
    errorimag = Io / input.txt3 * 100
    vecesacodosaturacion = 1.35 / Induccion
    areanucleom2 = input.txt11 * input.txt12 * input.txt6 * 10 ** (-6)
    pesochapa = areanucleom2 * longitud * 7.65 * 1000

    if Induccion > 0.15:
        corrientedeperdidas = (0.1429 * Induccion ** 6 - 0.4415 * Induccion ** 5 + 0.4754 * Induccion ** 4 - 0.1727 * Induccion ** 3 + 0.2914 * Induccion ** 2 + 0.0652 * Induccion - 0.006) * pesochapa / tensionsecundaria
    else:
        corrientedeperdidas = 0

    erroripderdidas = corrientedeperdidas / input.txt3 * 100
    corrientetotalcircmag = (Io ** 2 + corrientedeperdidas ** 2) ** 0.5
    errordemoduloA = (-(errorimag * senphi + erroripderdidas * input.txt10)) + (txt9irasteoricas / input.txt9 - 1) * 100
    errordeAngulo = (ctecorr * input.txt10 - corrientetotalcircmag * senphi) * 20
    Induccionatxt4 = tensionsecundaria * input.txt4 / txt9irasteoricas / input.txt9 / 4.44 / input.txt5 / areanucleocm2 * 10 ** 4
    ConsumoInterno = (input.txt3 ** 2) * resistenciaconductor

    return {
        "pesochapa": pesochapa,
        "Induccion": Induccion,
        "Io": Io,
        "errorimag": errorimag,
        "errordemoduloA": errordemoduloA,
        "errordeAngulo": errordeAngulo,
        "ConsumoInterno": ConsumoInterno,
        "H":H,
        "Longitud":longitud,
        "ctecorr":ctecorr
    }
pass