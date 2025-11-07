def sleep():
    global window_width, window_height 
    def draw():
        screen.blit(sleep_bg,((window_width-sleep_bg.get_width())/2,(window_height-sleep_bg.get_height())/2))
        screen.blit(mask,(0,0))
        screen.blit(sleeptext1,((window_width-sleeptext1.get_width())/2,(window_height-sleeptext1.get_height())/3-10*k))
        screen.blit(sleeptext2,((window_width-sleeptext2.get_width())/2,(window_height-sleeptext2.get_height())/3+sleeptext1.get_height()+5*k))
        screen.blit(adtext,((window_width-adtext.get_width())/2,(window_height-adtext.get_height())-5*k))
        pygame.display.flip()
    def scale_bg():
        global window_width, window_height, sleep_bg_original ,sleep_bg
        ratio = max(window_width/sleep_bg_original.get_width(), window_height/sleep_bg_original.get_height())
        bg= pygame.transform.smoothscale(sleep_bg_original, (int(sleep_bg_original.get_width()*ratio), int(sleep_bg_original.get_height()*ratio)))
        sleep_bg=bg
    def redraw_mainpage():
        global lastmessage,dpup,name,buttonx,buttony,sizex,sizey,k,window_width, window_height,lastname,bg,background_image,reset_namelist,message_time,ww,wh,animation,fullscreensurface,clocksurface,namesurface,buttonsurface,barsurface,screen,is_fullscreen
        
        pygame.display.set_caption(titleofprogramme)#标题
        pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
        
        window_width, window_height = pygame.display.get_surface().get_size()
        k=_k_()
        proportional_scale(background_image, window_width, window_height)
        clocksurface=pygame.Surface((140*k,40*k),SRCALPHA | HWSURFACE )
        clocksurface.fill((0,0,0,0))
        pygame.draw.rect(clocksurface, (0,0,0,100), (0,0,130*k,40*k), border_radius=int(5*k))
        buttonsurface=pygame.Surface((100*k,30*k),SRCALPHA | HWSURFACE )
        namesurface=pygame.Surface((4.5*150*k+30*k,150*k+60*k),SRCALPHA | HWSURFACE )
        pygame.draw.rect(namesurface, (0,0,0,155), (0,0,4.5*150*k+30*k,150*k+60*k), border_radius=int(33*k))
        buttonx=int((window_width-100*k)/2)
        buttony=int((window_height-30*k)/2+200*k)
        sizex=int(100*k)
        sizey=int(30*k)
        background()
        showclock(flush=False)
        draw_lastname(flush=False)
        fullscreenbutton(flush=False )
        settingsbutton(flush=False )
        if time.time()-message_time>=message_time_length and message_time!=0:
            lastmessage=''
            message(lastmessage)
            message_time=0
        if reset_namelist==1:
            draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180) 
        else:
            draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
        dpup=time.time()
        pygame.display.flip()
        
    
    global sleep_bg_directory,k
    globals()['currentpage']='sleep'
    if random_sleep_bg:
        globals()['sleep_bg_path']=get_random_image_from_directory(sleep_bg_directory)
        print(f"随机选择的休眠界面背景: {sleep_bg_path}")
    else :
        globals()['sleep_bg_path'] = init_background
        print(f"使用指定的背景：{ {sleep_bg_path}}")
    globals()['sleep_bg_original'] = pygame.image.load(sleep_bg_path).convert_alpha()
    scale_bg()
    mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    mask.fill((0,0,0,sleep_background_alpha))
    sleeptext1=pygame.font.SysFont("SIMHEI",int(48*k)).render("系统已进入休眠模式",True,(255,255,255))
    sleeptext2=pygame.font.SysFont("Kaiti",int(36*k)).render("点击任意位置唤醒",True,(255,255,255))
    adtext=pygame.font.SysFont("SIMSUN",int(24*k)).render("广告位招租，有意者联系Macrohard0001_m01@outlook.com",True,(255,255,255))
    sleep_control=True
    draw()
    keep=0
    while sleep_control:
        if keep-time.time()>=touch_delay:
            keep=0
        globals()['sleep_time']=time.time()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT :
                    draw()
                    exitwindow()
                    _k_()
                    scale_bg()
                    mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
                    mask.fill((0,0,0,sleep_background_alpha))
                    draw()
                    keep=time.time()
                    break
                case pygame.MOUSEBUTTONDOWN | pygame.FINGERDOWN :
                    if keep!=0:
                        keep=0
                    else :
                        globals()['sleep_time']=time.time()
                        redraw_mainpage()
                        sleep_control = False
                case pygame.VIDEORESIZE  | pygame.ACTIVEEVENT :
                    window_width, window_height = pygame.display.get_surface().get_size()
                    _k_()
                    scale_bg()
                    mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
                    mask.fill((0,0,0,sleep_background_alpha))
                    draw()
        pygame.time.Clock().tick(sleepfps)
    globals()['currentpage']='rootmainloop'
    globals()['sleep_time']=time.time()
                    
                    