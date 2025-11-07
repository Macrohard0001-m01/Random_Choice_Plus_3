def message(text,flush=True,temp=False):
    global k,size,messagesurface,pos,updatearea,tempsurface_2
    window_width, window_height = pygame.display.get_surface().get_size()
    if text!='':
        window_width, window_height = pygame.display.get_surface().get_size()
        textfont=pygame.font.SysFont("MicrosoftYaHei UI",int(20*k))
        _text_=textfont.render(text,True,(255,255,255))
        size=(_text_.get_width()+20*k,_text_.get_height()+10*k)
        messagesurface=pygame.Surface(size,SRCALPHA)
        messagesurface.fill((0,0,0,0))
        pygame.draw.rect(messagesurface, (0,0,0,127), (0,0,_text_.get_width()+20*k,_text_.get_height()+10*k), border_radius=int(5*k))
        messagesurface.blit(_text_,(10*k,5*k))
        pos=((window_width-(_text_.get_width()+20*k))/2,60*k)
        if temp:
            tempsurface_2.blit(messagesurface,pos)
        screen.blit(messagesurface,pos)
        updatearea=((window_width-(_text_.get_width()+20*k))/2,60*k,_text_.get_width()+20*k,_text_.get_height()+10*k)
    else:
        messagesurface.fill((0,0,0,0))
        screen.blit(messagesurface,pos)
    if flush:
        pygame.display.update(updatearea)