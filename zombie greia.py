from pylab import *

innvandring = 0.1
death = 0.03
medisiner = 0.9 #medisiner sinker dødsraten med 10%
t0 = 0
start_mennesker = 500
start_zombie = 100
vekst = innvandring - death 
hyppigheten = 0.0004
sjanse_død = 0.2 #0.2 fordi det er 20% sjanse på at et menneske dør når den møter på en zombie
sjanse_smitta = 0.3 # 0.3 fordi man har 30% sjanser på at man blir smitta når man møter på en zombie
sjanse_drap = 0.1  #sjanse for å drepe zombie 
antall_forsterkninger = 250
befolknings_grense = 1000 #Hvis befolkningen dropper under 1000 sa kommer forstarkninger
antall = 0
trening = 0.1

N = 100000
tid = 100
dt = tid/(N-1)

t = zeros(N)
P = zeros(N)
Z = zeros(N)
Pder = zeros(N)
Zder = zeros(N)
D = zeros(N) #Møter mellom mennesker og Zombie
Pu = zeros(N) #Populasjon av menneseker uten zombie
PuDer = zeros(N) 
# Dder = zeros(N)

def forsterkninger():
    global sjanse_død
    global sjanse_drap
    global death
    sjanse_død = sjanse_død * 0.5
    sjanse_drap = sjanse_drap * 1.5
    death = death * medisiner
    vekst = innvandring - death 
    
t[0] = t0
P[0] = start_mennesker
Z[0] = start_zombie
D[0] = 0 #Hvor mange som dør pga. Zombie  
Pu[0] = start_mennesker 
# Dder[0] = 0
for i in range (N-1):
    Pder[i] = vekst * P[i] * (1-P[i]/20000) - (hyppigheten * P[i] * Z[i])*sjanse_død 
    Zder[i] = (D[i] * sjanse_smitta) - (D[i] * (sjanse_drap + trening))
    PuDer[i] = vekst * P[i] * (1-P[i]/20000)
    # Dder[i+1] = (D[i+1] - D[i]) / (t[i+1] - t[i])
    D[i+1] =  (Pu[i] + PuDer[i] * dt) - (P[i] + Pder[i] * dt)
    Pu[i+1] = Pu[i] + PuDer[i] * dt 
    P[i+1] = P[i] + Pder[i] * dt
    
    if P[i+1] < P[i] and P[i] <= 1000 and antall < 2 : #Forsterkninger kan komme max to ganger 
        P[i+1] = P[i] + antall_forsterkninger
        forsterkninger()
        antall += 1
        
    Z[i+1] = Z[i] + Zder[i]*dt 
    t[i+1] = t[i] + dt
    
    if Z[i] <= 0:
        Z[i+1] = (Z[i] + Zder[i]*dt) * 0
    
    if death < 0.03:
        medisiner = medisiner * 1.001
    
        
#Plotter befolkningsvekst
plot(t,P, label='Mennesker')
plot(t,Z, label='Zombie')     
grid()
legend()
title("Populasjon")
xlabel("År")
ylabel("Populasjon")
show()

#Plotter hvor mange som dør pga. Zombie
plot(t,M)
grid()
title("Død pga. Zombie")
xlabel("År")
ylabel("Populasjon")
show()


