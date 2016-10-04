# Autor: Gustavo Santos, Wine Silva
# Email: gfdsantos@inf.ufpel.edu.br, wdssilva@inf.ufpel.edu.br

import pygame, random, pyaudio,math
import struct
import thread
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
        
def desenhar(srf, cor, inicio, fim, raio=1):
    '''
    Desenha uma linha de uma determinada cor, com um determinado
    raio de "inicio" ate "fim"
    '''
    
    dx = fim[0]-inicio[0]
    dy = fim[1]-inicio[1]
    distancia = max(abs(dx), abs(dy))
    novaCor= (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    random.seed(random.randint(0, 255))
    for i in range(distancia):    
        x = int(inicio[0]+float(i)/distancia*dx)
        y = int(inicio[1]+float(i)/distancia*dy)
        corMedia =((cor[0]* (float(i)/distancia) + novaCor[0]*(1-float(i)/distancia)  ),(cor[1]* (float(i)/distancia) + novaCor[1]*(1-float(i)/distancia)  ),(cor[2]* (float(i)/distancia) + novaCor[2]*(1-float(i)/distancia)  ) )
        pygame.display.update(pygame.draw.circle(srf, corMedia , (x, y), raio))
    cor= novaCor    
    thread.start_new_thread( tocar, (inicio,fim ) )
  
def tocar(inicio, fim):
    print "playing"
    dx = fim[0]-inicio[0]
    dy = fim[1]-inicio[1]
    distancia = max(abs(dx), abs(dy))
    fs = 10000
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,channels=1,rate=fs,output=True)
    toneInit = tones[inicio[0]%14 ][inicio[1]%14]
    toneFim =  tones[fim[0]%14 ][fim[1]%14]
   
    #for i in range(0,(distancia/10) ):
    #    play_tone((toneInit *(float(alfa)/distancia) + toneFim * (1-float(alfa)/distancia) ), 1, 0.7, fs, stream);
    #    play_tone( (tones[int(inicio[0]+float(i)/distancia*dx)%14][int(inicio[1]+float(i)/distancia*dy)%14]) , 1, 0.09, fs, stream)
    play_tone( (tones[dx%14][dy%14]) , 1, 1, fs, stream)

    
    stream.close()
    p.terminate()
    
def main():
    tela = pygame.display.set_mode((800,600))

    cores = [(255, 60, 60), (0, 220, 0), (30, 60, 255), (240, 0, 130), (230, 220, 50)]
    borracha = (0, 0 ,0)
    usando_borracha = False

    desenhando = False
    last_pos = (0, 0)
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
                        cor = borracha
                        usando_borracha = True
                        raio = raio_borracha
                    else:
                        cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                        usando_borracha = False
                        raio = raio_desenho
                    if desenhando == True:
                    	pygame.draw.circle(tela, cor, last_pos, raio)
            if e.type == pygame.KEYUP:
                cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                if desenhando == True:
                	pygame.draw.circle(tela, cor, last_pos, raio)
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 3:
                    cor = borracha
                    usando_borracha = True
                    raio = raio_borracha
                else:
                    cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                    raio = raio_desenho
                pygame.draw.circle(tela, cor, e.pos, raio)
                desenhando = True
            if e.type == pygame.MOUSEBUTTONUP:
                cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                desenhando = False
                usando_borracha = False
            if e.type == pygame.MOUSEMOTION:
                if desenhando:
                    pygame.draw.circle(tela, cor, e.pos, raio)
                    desenhar(tela, cor, e.pos, last_pos,  raio)
                last_pos = e.pos
            pygame.display.flip()
    except StopIteration:
        pass
    pygame.quit()

if __name__ == '__main__':
    main()