def draw_lastname(flush=True,temp=False):
    global tempsurface_2,namesurface,k
    text=pygame.font.SysFont("MicrosoftYaHei UI",size=int(150*k)).render(lastname,True,(255,255,255))
    if temp:
        k=_k_()
        namesurface=pygame.Surface((4.5*150*k+30*k,150*k+60*k),SRCALPHA | HWSURFACE )
        pygame.draw.rect(namesurface, (0,0,0,155), (0,0,4.5*150*k+30*k,150*k+60*k), border_radius=int(33*k))
        tempsurface_2.blit(namesurface,((window_width-4.5*150*k)/2+8*k,(window_height-150*k)/2-30*k))
        tempsurface_2.blit(text, ((4.5*150*k+30*k-text.get_width())/2-2*k+(window_width-4.5*150*k)/2+8*k,(150*k+60*k-text.get_height())/2-10*k+(window_height-150*k)/2-30*k))
        return 
    screen.blit(namesurface,((window_width-4.5*150*k)/2+8*k,(window_height-150*k)/2-30*k))
    screen.blit(text, ((4.5*150*k+30*k-text.get_width())/2-2*k+(window_width-4.5*150*k)/2+8*k,(150*k+60*k-text.get_height())/2-10*k+(window_height-150*k)/2-30*k))
    if flush:
        pygame.display.update(((window_width-4.5*150*k)/2+8*k,(window_height-150*k)/2-30*k,4.5*150*k+30*k,150*k+60*k))