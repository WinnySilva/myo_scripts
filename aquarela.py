#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Winny S"
__date__ = "$17/10/2016 17:51:43$"
import pygame
import random
import pyaudio
import math
import struct
import threading
import thread
tones2 = [440, 1661]
w = 800
h = 600
vermelhos = [(255,0,0),(255,99,71),(255,127,80),(233,150,122),(165,42,42),(178,34,34),(128,0,0)]
cores = [(255,0,0), (255,69,0),(255,255,0),(0,255,0),(0,128,128),(106,90,205),(128,0,128)]
notas =[]
recs = []
elips = []
p = pyaudio.PyAudio()
fs=15000
stream = p.open(format=pyaudio.paFloat32,channels=1,rate=fs,output=True)
posAtual = (0,0) #PRECISA DE LOCKS
lock = threading.Lock()
cond = threading.Condition()
evt = False
def play_tone(frequency, amplitude, duration, fs, stream):
    N = int(fs / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 5* 1.0 / fs
    tone = (amplitude*
    (2*math.sin(math.pi * frequency * n*dt )
    /float(math.sqrt( (n*5/3.0) ) ) ) 
    for n in range(1,N))
    data = ''.join(struct.pack('f', samp) for samp in tone)
    for n in xrange(T):
        stream.write(data)
def notasonscreen(id,id2):
    while True:
        
        lock.acquire()
        while(evt==False):
            cond.wait()
        
        nota = (float(posAtual[1])/float(h)) * (tones2[1]-tones2[0]) + tones2[0]
        lock.release() 
        amplitude = 1#float(posAtual[0]/w)
        duration = 1
        #print nota
        play_tone(nota, amplitude, duration, fs, stream)
    
def cenario(tela):
    tela.fill([0, 0, 0])
    print "huehuehu"
    for i in range(0,7):    
        pygame.draw.rect(tela, cores[i], recs[i])
        pygame.draw.ellipse(tela, cores[i], elips[i])
        pygame.draw.circle(tela, cor, pos, 50)
        
def carreganotas():
    pygame.mixer.init()
    piano=[]
    for i in range(1,12):
        filename = "sound/piano/"+str(i)+".wav"
        #print filename
        piano.append(pygame.mixer.Sound(filename))
    notas.append(piano)
    
def tocarnotas(pos, instrumento):
    auxRect = pygame.Rect(pos[0], pos[1], 1, 1)
    recNum=-1
    #print len(recs)
    for i in range(0,len(recs)):
        #print i,recs[i],pos
        if recs[i].contains(auxRect):
            recNum = i
            break
    if(recNum !=-1):
        notas[instrumento][recNum].play()
        #print recNum,pos
    
def main():
    tela = pygame.display.set_mode((w,h))
    pygame.display.set_caption('Aquarela Musical')
    #for i in range(0,7):    
     #   recs.append( pygame.Rect((i)*(w/7), 0, w/7, h-1) )
      #  elips.append( (i*(w/7), 0, 50, 50) )
    #carregaNotas()
    cenario(tela)
    asurf = pygame.image.load(os.path.join('images', 'path3.png'))
    
    thread.start_new_thread(notasonscreen, (1,2))
    try:
        while True:
            # um handler para qualquer evento do pygame 
            e = pygame.event.wait()
            #print e
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEMOTION:
                cor_al = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
                pygame.draw.circle(tela, cor_al, e.pos, 5)
                #tocarNotas(e.pos,0)
                lock.acquire() 
                posAtual = e.pos
                cond.notify()
                lock.release()
                #notasonscreen(e.pos)
#           tela.blit(asurf,(w/2,h/2))
            cenario(tela)
            pygame.display.flip()
            print " hsuaha "
            
    except StopIteration:
        pass
    pygame.quit()


if __name__ == "__main__":
    main()
