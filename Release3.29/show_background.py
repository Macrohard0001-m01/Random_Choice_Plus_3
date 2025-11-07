def proportional_scale(img, max_width, max_height):
    global window_width, window_height, bg
    ratio = max(window_width/img.get_width(), window_height/img.get_height())
    bg= pygame.transform.smoothscale(img, 
        (int(img.get_width()*ratio), int(img.get_height()*ratio)))
    return bg

def background():
    global window_width, window_height,background_image,bg
    try:
        screen.blit(bg,((window_width-bg.get_width())/2,(window_height-bg.get_height())/2))
    except :
        screen.fill((0,0,0))
        errorbackground=pygame.font.SysFont("MicrosoftYaHei UI",int(20*k)).render("加载背景失败，已使用黑色背景",True,(255,255,255))
        screen.blit(errorbackground,(0,0))
        pygame.display.update((0,0,errorbackground.get_width(),errorbackground.get_height()))