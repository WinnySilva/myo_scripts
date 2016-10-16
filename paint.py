# Autor: Gustavo Santos, Wine Silva
# Email: gfdsantos@inf.ufpel.edu.br, wdssilva@inf.ufpel.edu.br

import pygame, random, pyaudio,math
import struct
import thread, threading
tones=[ 
[ 440  , 493  , 523  , 587  , 659  , 739  , 783  , 783  , 739  , 659  , 587  , 523  , 493  , 440   ],
[ 493  , 523  , 587  , 659  , 739  , 783  , 783  , 739  , 659  , 587  , 523  , 493  , 440  , 440   ],
[ 523  , 587  , 659  , 739  , 783  , 783  , 739  , 659  , 587  , 523  , 493  , 440  , 440  , 493   ],
[ 587  , 659  , 739  , 783  , 783  , 739  , 659  , 587  , 523  , 493  , 440  , 440  , 493  , 523   ],
[ 659  , 739  , 783  , 783  , 739  , 659  , 587  , 523  , 493  , 440  , 440  , 493  , 523  , 587   ],
[ 739  , 783  , 783  , 739  , 659  , 587  , 523  , 493  , 440  , 440  , 493  , 523  , 587  , 659   ],
[ 783  , 783  , 739  , 659  , 587  , 523  , 493  , 440  , 440  , 493  , 523  , 587  , 659  , 739   ],
[ 783  , 739  , 659  , 587  , 523  , 493  , 440  , 440  , 493  , 523  , 587  , 659  , 739  , 783   ],
[ 739  , 659  , 587  , 523  , 493  , 440  , 440  , 493  , 523  , 587  , 659  , 739  , 783  , 783   ],
[ 659  , 587  , 523  , 493  , 440  , 440  , 493  , 523  , 587  , 659  , 739  , 783  , 783  , 739   ],
[ 587  , 523  , 493  , 440  , 440  , 493  , 523  , 587  , 659  , 739  , 783  , 783  , 739  , 659   ],
[ 523  , 493  , 440  , 440  , 493  , 523  , 587  , 659  , 739  , 783  , 783  , 739  , 659  , 587   ],
[ 493  , 440  , 440  , 493  , 523  , 587  , 659  , 739  , 783  , 783  , 739  , 659  , 587  , 523  ],
[ 440  , 440  , 493  , 523  , 587  , 659  , 739  , 783  , 783  , 739  , 659  , 587  , 523  , 493   ]
]
tones_=[ 
[ "A"  , "B"  , "C"  , "D"  , "E"  , "F"  , "G"  , "G"  , "F"  , "E"  , "D"  , "C"  , "B"  , "A"   ],
[ "B"  , "C"  , "D"  , "E"  , "F"  , "G"  , "G"  , "F"  , "E"  , "D"  , "C"  , "B"  , "A"  , "A"   ],
[ "C"  , "D"  , "E"  , "F"  , "G"  , "G"  , "F"  , "E"  , "D"  , "C"  , "B"  , "A"  , "A"  , "B"   ],
[ "D"  , "E"  , "F"  , "G"  , "G"  , "F"  , "E"  , "D"  , "C"  , "B"  , "A"  , "A"  , "B"  , "C"   ],
[ "E"  , "F"  , "G"  , "G"  , "F"  , "E"  , "D"  , "C"  , "B"  , "A"  , "A"  , "B"  , "C"  , "D"   ],
[ "F"  , "G"  , "G"  , "F"  , "E"  , "D"  , "C"  , "B"  , "A"  , "A"  , "B"  , "C"  , "D"  , "E"   ],
[ "G"  , "G"  , "F"  , "E"  , "D"  , "C"  , "B"  , "A"  , "A"  , "B"  , "C"  , "D"  , "E"  , "F"   ],
[ "G"  , "F"  , "E"  , "D"  , "C"  , "B"  , "A"  , "A"  , "B"  , "C"  , "D"  , "E"  , "F"  , "G"   ],
[ "F"  , "E"  , "D"  , "C"  , "B"  , "A"  , "A"  , "B"  , "C"  , "D"  , "E"  , "F"  , "G"  , "G"   ],
[ "E"  , "D"  , "C"  , "B"  , "A"  , "A"  , "B"  , "C"  , "D"  , "E"  , "F"  , "G"  , "G"  , "F"   ],
[ "D"  , "C"  , "B"  , "A"  , "A"  , "B"  , "C"  , "D"  , "E"  , "F"  , "G"  , "G"  , "F"  , "E"   ],
[ "C"  , "B"  , "A"  , "A"  , "B"  , "C"  , "D"  , "E"  , "F"  , "G"  , "G"  , "F"  , "E"  , "D"   ],
[ "B"  , "A"  , "A"  , "B"  , "C"  , "D"  , "E"  , "F"  , "G"  , "G"  , "F"  , "E"  , "D"  , "C"  ],
[ "A"  , "A"  , "B"  , "C"  , "D"  , "E"  , "F"  , "G"  , "G"  , "F"  , "E"  , "D"  , "C"  , "B"   ]
]
tones1 = {
        'A': 440,
        'A#': 466,
        'B': 493,
        'C': 523,
        'C#': 554,
        'D': 587,
        'D#': 622,
        'E': 659,
        'F': 698,
        'F#': 739,
        'G': 783,
        'G#': 830,
        'a': 880,
        'a#': 932,
        'b': 987,
        'c': 1046,
        'c#': 1108,
        'd': 1174,
        'd#': 1244,
        'e': 1318,
        'f': 1396,
        'f#': 1479,
        'g': 1567,
        'g#': 1661
    }
escala_menor=[
["C","D","D#","F","G","G#","B"],
["C#","D#","E","F#","G#","A","C"],
["D","E","F","G","A","A#","C#"],
["D#","F","F#","G#","A#","B","D"],
["E","F#","G","A","B","C","D#"],
["F","G","G#","A#","C","C#","E"],
["F#","G#","A","B","C#","D","F"],
["G","A","A#","C","D","D#","F#"],
["G#","A#","B","C#","D#","E","G"],
["A","B","C","D","E","F","G#"],
["A#","C","C#","D#","F","F#","A"],
["B","C#","D","E","F#","G","A#"]
]
escala_pentatonica_maior={
"C":["C","D","E","G","A"],
"C#":["C#","D#","F","G#","A#"],
"D":["D","E","F#","A","B"],
"D#": ["D#","F","G","A#","C"],
"E":["E","F#","G#","B","C#"],
"F": ["F","G","A","C","D"],
"F#": ["F#","G#","A#","C#","D"],
"G":["G","A","B","D","E"],
"G#":["G#","A#","C","D#","F"],
"A":["A","B","C#","E","F#"],
"A#":["A#","C","D","F","G"],
"B":["B","C#","D#","F#","G#"]
}

global cont_escala
cont_escala= 0
global escala_atual
escala_atual= []
global cor
global lock
lock =  threading.Lock()
def play_tone(frequency, amplitude, duration, fs, stream):
    N = int(fs / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 1.0/ fs
   
    # 1 cycle
    tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt)
            for n in xrange(N))
    # todo: get the format from the stream; this assumes Float32
    data = ''.join(struct.pack('f', samp) for samp in tone)
    for n in xrange(T):
        stream.write(data)
        
def desenhar(srf, inicio, fim, raio=1):
    '''
    Desenha uma linha de uma determinada cor, com um determinado
    raio de "inicio" ate "fim"
    '''
    global cor
    aux = cor
    dx = fim[0]-inicio[0]
    dy = fim[1]-inicio[1]
    distancia = max(abs(dx), abs(dy))
    novaCor= (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    random.seed(random.randint(0, 255))
    for i in range(distancia):    
        x = int(inicio[0]+float(i)/distancia*dx)
        y = int(inicio[1]+float(i)/distancia*dy)
        corMedia =((aux[0]* (float(i)/distancia) + novaCor[0]*(1-float(i)/distancia)  ),(aux[1]* (float(i)/distancia) + novaCor[1]*(1-float(i)/distancia)  ),(aux[2]* (float(i)/distancia) + novaCor[2]*(1-float(i)/distancia)  ) )
        pygame.display.update(pygame.draw.circle(srf, corMedia , (x, y), raio))
   
    cor= novaCor    
    #thread.start_new_thread( tocar, (inicio,fim ) )
    tocar(inicio,fim )
  
def tocar(inicio, fim):
    print "playing"
    
    dx = fim[0]-inicio[0]
    dy = fim[1]-inicio[1]
    distancia = max(abs(dx), abs(dy))
    toneInit = tones[inicio[0]%14 ][inicio[1]%14]
    toneFim =  tones[fim[0]%14 ][fim[1]%14]
    #for i in range(0,(distancia/10) ):
    #    play_tone((toneInit *(float(alfa)/distancia) + toneFim * (1-float(alfa)/distancia) ), 1, 0.7, fs, stream);
    #    play_tone( (tones[int(inicio[0]+float(i)/distancia*dx)%14][int(inicio[1]+float(i)/distancia*dy)%14]) , 1, 0.09, fs, stream)    
    a = float(random.randint(0, distancia))+0.2
    t = 0.5
    
    #t = 0.5 * (1/distancia)
    lock.acquire()
    #for i in (0,4):
    #    print escal[i],t
        #t=float(random.randint(0, distancia))+0.2
    global cont_escala
    if cont_escala==0:
        global escala_atual
        escala_atual = escala_pentatonica_maior[tones_[inicio[0]%14][inicio[1]%14]]
        
    play_tone( tones1[escala_atual[cont_escala]] , a, t, fs, stream)
    print cont_escala,escala_atual[cont_escala]
    cont_escala = (cont_escala+1)%5
    lock.release() 
    #stream.close()
    #p.terminate()
def main():
    
    tela = pygame.display.set_mode((800,600))
    cores = [(255, 60, 60), (0, 220, 0), (30, 60, 255), (240, 0, 130), (230, 220, 50)]
    borracha = (0, 0 ,0)
    usando_borracha = False

    desenhando = False
    last_pos = (0, 0)
    global cor
    cor =(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)) #random.choice(cores)
    raio_desenho = 10
    raio_borracha = 20
    raio = 10

    try:
        while True:
            # um handler para qualquer evento do pygame 
            e = pygame.event.wait()
            # debug dos eventos capturados
            print(e)
       	    # se o tipo do evento de uma tecla pressionada
            if e.type == pygame.KEYDOWN:
                if e.key == 98: # letra B
                    if not usando_borracha:
                        global cor
                        cor = borracha
                        usando_borracha = True
                        raio = raio_borracha
                    else:
                        #cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                        usando_borracha = False
                        raio = raio_desenho
                    if desenhando == True:
                        #global cor
                    	pygame.draw.circle(tela, cor, last_pos, raio)
            if e.type == pygame.KEYUP:
                #cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                if desenhando == True:
                	pygame.draw.circle(tela, cor, last_pos, raio)
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 3:
                    global cor
                    cor = borracha
                    usando_borracha = True
                    raio = raio_borracha
                else:
                 #   cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                    raio = raio_desenho
                global cor
                pygame.draw.circle(tela, cor, e.pos, raio)
                desenhando = True
            if e.type == pygame.MOUSEBUTTONUP:
               # cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                desenhando = False
                usando_borracha = False
            if e.type == pygame.MOUSEMOTION:
                if desenhando:
                    global cor
                    pygame.draw.circle(tela, cor, e.pos, raio)
                    desenhar(tela, e.pos, last_pos,  raio)
                last_pos = e.pos
            pygame.display.flip()
    except StopIteration:
        pass
    pygame.quit()
fs = 10000
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,channels=1,rate=fs,output=True)

if __name__ == '__main__':
    main()
    stream.close()
    p.terminate()