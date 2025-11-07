def settingsbutton(style=None,flush=True,temp=False):
    global settingsurface
    settingsurface.fill((0,0,0,0))
    if temp:
        pygame.draw.rect(settingsurface, (0,0,0,100), (0,0,36*k,36*k), border_radius=int(5*k))
        tempsurface_2.blit(settingsurface,(0,540-36))
        tempsurface_2.blit(settingbutton_img,(0,540-36))
        return 
    if style=='click':
        pygame.draw.rect(settingsurface, (127,127,127,100), (0,0,36*k,36*k), border_radius=int(5*k))
    elif style=='puton':
        pygame.draw.rect(settingsurface, (63,63,63,127), (0,0,36*k,36*k), border_radius=int(5*k))
    else:
        pygame.draw.rect(settingsurface, (0,0,0,100), (0,0,36*k,36*k), border_radius=int(5*k))
    settingsurface.blit(settingbutton_img,(0,0))
    screen.blit(settingsurface,(0,window_height-36*k))
    if flush:
        pygame.display.update((0,window_height-36*k,36*k,36*k))

def fullscreenbutton(style=0,flush=True,temp=False):
    global k,fullscreensurface,is_fullscreen,window_width,window_height,tempsurface_2,fullscreenbutton_img,exitfullscreenbutton_img
    if temp:
        pygame.draw.rect(fullscreensurface, (0,0,0,100), (0,0,36*k,36*k), border_radius=int(5*k))
        tempsurface_2.blit(fullscreensurface,(960-36,540-36))
        tempsurface_2.blit(fullscreenbutton_img,(960-36,540-36))
        return 
    if is_fullscreen:
        fullscreensurface.fill((0,0,0,0))
        if style=='click':
            pygame.draw.rect(fullscreensurface, (127,127,127,100), (0,0,36*k,36*k), border_radius=int(5*k))
        elif style=='puton':
            pygame.draw.rect(fullscreensurface, (63,63,63,127), (0,0,36*k,36*k), border_radius=int(5*k))
        else:
            pygame.draw.rect(fullscreensurface, (0,0,0,100), (0,0,36*k,36*k), border_radius=int(5*k))
        fullscreensurface.blit(exitfullscreenbutton_img,(0,0))
        screen.blit(fullscreensurface,(window_width-36*k,window_height-36*k))
        if flush:
            pygame.display.update((window_width-36*k,window_height-36*k,36*k,36*k))
    else:
        fullscreensurface.fill((0,0,0,0))
        if style=='click':
            pygame.draw.rect(fullscreensurface, (127,127,127,100), (0,0,36*k,36*k), border_radius=int(5*k))
        elif style=='puton':
            pygame.draw.rect(fullscreensurface, (63,63,63,127), (0,0,36*k,36*k), border_radius=int(5*k))
        else:
            pygame.draw.rect(fullscreensurface, (0,0,0,100), (0,0,36*k,36*k), border_radius=int(5*k))
        fullscreensurface.blit(fullscreenbutton_img,(0,0))
        screen.blit(fullscreensurface,(window_width-36*k,window_height-36*k))
        if flush:
            pygame.display.update((window_width-36*k,window_height-36*k,36*k,36*k))

def draw_button(place,size,text,rad=3,color=(50,50,50),_alpha_=255,temp=False):
    global tempsurface_2,buttonsuaface
    buttonsurface.fill((0,0,0,0))
    sizeoftext=min(int(size[1]*2/3),int(size[0]/len(text)-1))
    pygame.draw.rect(buttonsurface, (*color,_alpha_), (0,0,size[0],size[1]), border_radius=rad)
    buttonsurface.blit(pygame.font.SysFont("MicrosoftYaHei UI",sizeoftext).render(text,True,(255,255,255)),((size[0]-sizeoftext*len(text))/2,((size[1]-sizeoftext*3/2)/2)))
    if temp:
        tempsurface_2.blit(buttonsurface,place)
        return 
    screen.blit(buttonsurface,place)

