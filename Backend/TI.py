import math

txt=100
txt2=600
txt3=5
txt4=20
txt5=50
txt6=0.96
txt7=1
txt8=200
txt9=600
txt10=0.8
txt11=120
txt12=70


senphi=(math.sin(math.acos(txt10)))
txt9irasteoricas=txt2/txt3
DiamInt=int(txt8-(2*(math.ceil(txt9irasteoricas/txt9/int(txt8*3.14/(txt7+0.5)))*(txt7+0.5))))


Diamext=int(txt8+(2*txt12)+(2*(math.ceil(txt9irasteoricas/txt9/int(txt8*3.14/(txt7+0.5)))*(txt7+0.5))))

diametromedionucleo=txt8+(0.7+txt7+0.12+0.5)*2+txt12

longitud=diametromedionucleo*3.14159/1000

desarrollomedioalambre=(txt11+txt12)*2+0.7*4+(txt7+0.12)*2

seccionalambre=(txt7**2)*3.14159/4

resistenciaconductor=0.0172*desarrollomedioalambre*txt9irasteoricas/txt9/seccionalambre/1000
carga=1


tensionsecundaria=txt/txt3

areanucleocm2=(txt11*txt12*txt6)*10**(-2)
Induccion=0.00000000
Induccion=(tensionsecundaria/txt9irasteoricas/txt9/4.44/txt5/areanucleocm2*10**4)

if Induccion>0.5:
	H=11.852*Induccion**2 - 4.026*Induccion + 9.1573
else:
	H=15.49*Induccion**0.6309


if tensionsecundaria<0.163:
	ctecorr=794.39*Induccion*4 - 566.01*Induccion*3 + 138.27*Induccion*2 - 13.63*Induccion + 1.7174
elif tensionsecundaria<1.0977:
		ctecorr=1.279
else:
		ctecorr=-62.4817*Induccion**6 + 482.9707*Induccion**5 - 1523.8608*Induccion**4 + 2512.1181*Induccion**3 - 2284.8936*Induccion**2 + 1088.765*Induccion - 211.3421


Io=H*longitud/txt9irasteoricas/txt9/ctecorr

errorimag=Io/txt3*100
vecesacodosaturacion=1.35/Induccion
areanucleom2=txt11*txt12*txt6*10**(-6)
pesochapa=areanucleom2*longitud*7.65*1000

if Induccion>0.15:
	corrientedeperdidas=((0.1429*Induccion*6-0.4415*Induccion**5+0.4754*Induccion**4-0.1727*Induccion**3+0.2914*Induccion**2+0.0652*Induccion-0.006)*pesochapa/tensionsecundaria)
else:
	corrientedeperdidas=0

erroripderdidas=corrientedeperdidas/txt3*100

corrientetotalcircmag=(Io**2+corrientedeperdidas**2)**0.5

errordemoduloA=(-(errorimag*senphi+erroripderdidas*txt10))+(txt9irasteoricas/txt9/txt9irasteoricas/txt9-1)*100

errordeAngulo=(ctecorr*txt10-corrientetotalcircmag*senphi)*20

Induccionatxt4 =tensionsecundaria*txt4/txt9irasteoricas/txt9/4.44/txt5/areanucleocm2*10**4

ConsumoInterno=(txt3**2)*resistenciaconductor


print(pesochapa)
