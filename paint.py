# Autor: Gustavo Santos, Wine Silva
# Email: gfdsantos@inf.ufpel.edu.br, wdssilva@inf.ufpel.edu.br

import pygame, random, pyaudio,math
import struct
import thread, threading

tones = [ 440, 
        493,
         523,
         587,
         659,
        698,
        783
]
tones1 = [  523,
        554,
        587,
        622,
        659,
        698,
        739,
        783,
        830,
        440,
        466,
        493,
        1046,
        1108,
        1174,
        1244,
        1318,
         1396,
         1479,
         1567,
         1661,        
        880,
         932,
         987]


global cont_escala
cont_escala= 0
global escala_atual
escala_atual= []
global cor
global lock
global posAtual
global nota
nota=-1
posAtual=(0,0)
global desenhando
desenhando = False
lock =  threading.Lock()
fs = 5000
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,channels=1,rate=fs,output=True)
def carregarPiano():
    n = 12
    piano = []
    for i in range(1,n):
        nome ="sound/"+ i+".wav"
        sounds.append(pygame.mixer.Sound(nome))
    return piano
    
def daemon(w,j):
    global desenhando, cont_escala,escala_atual
    a = 20
    t = 0.5
    aux=2
    global posAtual
    global stream,fs,desenhando
    global nota
    
    while(1):
        
        if nota > -1:            
            if (desenhando == True):
                a=( posAtual[0]*1.0/w*1.0 ) *2
                play_tone(tones1[nota], a, 0.1, fs, stream)
                
        

def notas_Div(height):
    print height
    n_divs = len(tones1) - 1# 10
    divs = height/n_divs
    areas =[]
    area = 0;
    for i in range(0,n_divs):
        areas.append(area)
        area = area+divs
    areas.append(height)    
    return areas;
def play_tone(frequency, amplitude, duration, fs, stream):
    N = int(fs / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 1.0/ fs
    # 1 cycle
    tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt)
            for n in xrange(N))
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
    #tocar(inicio,fim )
  

def partitura(height, posY):
    divs = notas_Div(height)
    global nota
    i=0
    
    while (i< len(divs))and(posY>divs[i]) :
        i+=1        
    if(i<len(divs)):
        nota = (i-1)
    else: 
        nota = len(divs)-1
    print "pos: ", posY,len(divs)
    if(posY<100):
        print "7"
    elif(posY<120):
        print "1"
    elif(posY<140):
        print "1"
    elif(posY<240):
        print "8"
    elif(posY<260):
        print "7"
    elif(posY<360):
        print "6"
    elif(posY<380):
        print "5"
    elif(posY<478):
        print "4"
    elif(posY<490):
        print "3"
    elif(posY<600):
        print "2"
    elif(posY<640):
        print "1"
    else:
        print "0"
    print " nota ",nota    
        
def main():
    w =  1336
    h=  720
    pygame.init()
    tela = pygame.display.set_mode((w,h),pygame.FULLSCREEN)#pygame.display.set_mode((w,h))
    #pygame.display.set_mode((640,480),pygame.FULLSCREEN)
    pygame.display.set_caption('Aquarela Musical')
    tela.fill([0, 0, 0])
    borracha = (0, 0 ,0)
    usando_borracha = False
    global desenhando
    desenhando = False
    last_pos = (0, 0)
    global cor
    cor =(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)) #random.choice(cores)
    raio_desenho = 10
    raio_borracha = 20
    raio = 10
    
    clave = pygame.image.load('path3.png')
    clave = pygame.transform.scale(clave, (w/5, h))
    clave_quad = pygame.draw.rect(tela, (0,0,0),(0,0,10,10) )
    
    linhas = pygame.image.load('g4518.png')
    linhas = pygame.transform.scale(linhas, (w, h))
    linhas_quad = pygame.draw.rect(tela, (0,0,0),(0,0,w,h) )
    
    # musica_fundo = pygame.mixer.Sound('./OdetoJoy_Beethoven.mp3')
    # musica_fundo.play()
    lock.acquire()
    thread.start_new_thread( daemon, (w,0) )
    global posAtual
    try:
        while True:
            
            # um handler para qualquer evento do pygame 
            e = pygame.event.wait()
            
            # debug dos eventos capturados
    #        print(e)
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
                        global desenhando
                    if desenhando == True:
                        #global cor
                    	pygame.draw.circle(tela, cor, last_pos, raio)
                elif e.key == 102:
                  raise StopIteration
            if e.type == pygame.KEYUP:
                #cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                global desenhando
                if desenhando == True:
                	pygame.draw.circle(tela, cor, last_pos, raio)
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                posAtual = e.pos
                if e.button == 3:
                    global cor
                    cor = borracha
                    usando_borracha = True
                    raio = raio_borracha
                   
                else:
                 #   cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                    
                    partitura(h,e.pos[1])
                    raio = raio_desenho
                    
                global cor
                pygame.draw.circle(tela, cor, e.pos, raio)
                global desenhando
                desenhando = True
                
            if e.type == pygame.MOUSEBUTTONUP:
                tela.fill([0, 0, 0])
                pygame.display.flip()
                tela.blit(linhas,linhas_quad)
                tela.blit(clave,clave_quad)
            
                
                posAtual = e.pos
               # cor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#random.choice(cores)
                global desenhando
                desenhando = False
                usando_borracha = False
                nota=-1
            if e.type == pygame.MOUSEMOTION:
                posAtual = e.pos
                global desenhando
                if desenhando:
                    global cor
                    pygame.draw.circle(tela, cor, e.pos, raio)
                    desenhar(tela, e.pos, last_pos,  raio)
                    partitura(h,e.pos[1])
                last_pos = e.pos
                posAtual =  last_pos
                
            pygame.display.flip()
            tela.blit(linhas,linhas_quad)
            tela.blit(clave,clave_quad)
            
    except StopIteration:
        pass
    pygame.quit()

    


if __name__ == '__main__':
    main()
    stream.close()
    p.terminate()