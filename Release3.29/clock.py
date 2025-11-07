def showclock(flush=True):
    global screen,k,window_width, window_height,clocksurface
    clock_time=pygame.font.SysFont("MicrosoftYaHei UI",int(30*k)).render(datetime.datetime.now().strftime("%H:%M:%S"),True,(255,255,255))
    screen.blit(clocksurface,((window_width-130*k),0))
    screen.blit(clock_time,((130*k-clock_time.get_width())/2-2*k+(window_width-130*k),(40*k-clock_time.get_height())/2))
    if flush:
        pygame.display.update(((window_width-130*k),0,140*k,40*k))