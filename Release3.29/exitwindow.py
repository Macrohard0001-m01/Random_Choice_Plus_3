def exitwindow():
    global surfacemixer,tempsurface2,mask,currantpage,namesurface,buttonsurface,clocksurface,window_width,window_height,screen_surface,window_width , window_height , lastmessage , k,sizex,sizey,buttonx,buttony
    buttonalpha=245  #180
    if currentpage=='rootmainloop':
        draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
        fullscreenbutton(flush=False)
        draw_lastname(flush=False)
        settingsbutton(flush=False)
        draw_lastname(flush=False )
        try:
            message(lastmessage,flush=False)
        except :
            pass
    screensurface=pygame.display.get_surface()
    screen_surface=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    screen_surface.blit(screensurface,(0,0))
    screen.blit(screen_surface,(0,0))
    mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    mask.fill((0,0,0,150))
    screen.blit(mask,(0,0))
    exit_window=pygame.Surface((int(480*k),int(180*k)),SRCALPHA)
    pygame.draw.rect(exit_window, (31,31,31,245), (0,0,480*k,180*k), border_radius=int(8*k))
    asktext=pygame.font.SysFont("MicrosoftYaHei UI",int(36*k)).render("你真的要退出吗？",True,(255,255,255))
    exit_window.blit(asktext,(int((exit_window.get_width()-asktext.get_width())/2),int(20*k)))
    pygame.draw.rect(exit_window, (63,63,63,buttonalpha), (40*k,130*k,110*k,33*k), border_radius=int(5*k))
    text_1=pygame.font.SysFont("MicrosoftYaHei UI",int(18*k)).render("收起",True,(255,255,255))
    exit_window.blit(text_1,(int(40*k+(110*k-text_1.get_width())/2),int(130*k+(33*k-text_1.get_height())/2)))
    pygame.draw.rect(exit_window, (63,63,63,buttonalpha), (175*k,130*k,110*k,33*k), border_radius=int(5*k))
    text_2=pygame.font.SysFont("MicrosoftYaHei UI",int(18*k)).render("退出",True,(255,255,255))
    exit_window.blit(text_2,(int(175*k+(110*k-text_2.get_width())/2),int(130*k+(33*k-text_2.get_height())/2)))
    pygame.draw.rect(exit_window, (63,63,63,buttonalpha), (310*k,130*k,110*k,33*k), border_radius=int(5*k))
    text_3=pygame.font.SysFont("MicrosoftYaHei UI",int(18*k)).render("取消",True,(255,255,255))
    exit_window.blit(text_3,(int(310*k+(110*k-text_3.get_width())/2),int(130*k+(33*k-text_3.get_height())/2)))
    screen.blit(exit_window,(int((screen.get_width()-480*k)/2),int((screen.get_height()-180*k)/2)))
    pygame.display.flip()
    a=0
    while a==0:
        tempsurface2=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
        screen.blit(screen_surface,(0,0))
        screen.blit(mask,(0,0))
        screen.blit(exit_window,(int((screen.get_width()-480*k)/2),int((screen.get_height()-180*k)/2)))
        if pygame.Rect(int((screen.get_width()-480*k)/2+40*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k).collidepoint(pygame.mouse.get_pos()) :
            pygame.draw.rect(tempsurface2, (255,255,255,42), (int((screen.get_width()-480*k)/2+40*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k), border_radius=int(5*k))
        elif pygame.Rect(int((screen.get_width()-480*k)/2+40*k+135*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k).collidepoint(pygame.mouse.get_pos()) :
            pygame.draw.rect(tempsurface2, (255,255,255,42), (int((screen.get_width()-480*k)/2+40*k+135*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k), border_radius=int(5*k))
        elif pygame.Rect(int((screen.get_width()-480*k)/2+40*k+270*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k).collidepoint(pygame.mouse.get_pos()) :
            pygame.draw.rect(tempsurface2, (255,255,255,42), (int((screen.get_width()-480*k)/2+40*k+270*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k), border_radius=int(5*k))
        screen.blit(tempsurface2,(0,0))
        pygame.display.flip()
        globals()['sleep_time']=time.time()
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONDOWN | pygame.FINGERDOWN :
                    globals()['sleep_time']=time.time()
                    if pygame.Rect(int((screen.get_width()-480*k)/2+40*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k).collidepoint(pygame.mouse.get_pos()) :
                        #收起
                        b=0
                        while b==0:
                            tempsurface2=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
                            screen.blit(screen_surface,(0,0))
                            screen.blit(mask,(0,0))
                            screen.blit(exit_window,(int((screen.get_width()-480*k)/2),int((screen.get_height()-180*k)/2)))
                            pygame.draw.rect(tempsurface2, (255,255,255,84), (int((screen.get_width()-480*k)/2+40*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k), border_radius=int(5*k))
                            screen.blit(tempsurface2,(0,0))
                            if not any(pygame.mouse.get_pressed()):
                                b=1
                            for event in pygame.event.get():
                                match event.type:
                                    case pygame.MOUSEBUTTONUP | pygame.FINGERUP:
                                            b=1
                            pygame.display.flip()
                            pygame.time.Clock().tick(fps)
                        pack_up()
                        pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
                        return 
                    elif pygame.Rect(int((screen.get_width()-480*k)/2+40*k+135*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k).collidepoint(pygame.mouse.get_pos()) :
                        #退出
                        b=0
                        while b==0:
                            tempsurface2=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
                            screen.blit(screen_surface,(0,0))
                            screen.blit(mask,(0,0))
                            screen.blit(exit_window,(int((screen.get_width()-480*k)/2),int((screen.get_height()-180*k)/2)))
                            pygame.draw.rect(tempsurface2, (255,255,255,84), (int((screen.get_width()-480*k)/2+40*k+135*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k), border_radius=int(5*k))
                            screen.blit(tempsurface2,(0,0))
                            if not any(pygame.mouse.get_pressed()):
                                b=1
                            for event in pygame.event.get():
                                match event.type:
                                    case pygame.MOUSEBUTTONUP | pygame.FINGERUP:
                                            b=1
                            pygame.display.flip()
                            pygame.time.Clock().tick(fps)
                        if pygame.Rect(int((screen.get_width()-480*k)/2+40*k+135*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k).collidepoint(pygame.mouse.get_pos()) :
                            tempsurface2=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
                            screen.blit(screen_surface,(0,0))
                            screen.blit(mask,(0,0))
                            screen.blit(exit_window,(int((screen.get_width()-480*k)/2),int((screen.get_height()-180*k)/2)))
                            pygame.draw.rect(tempsurface2, (255,255,255,0), (int((screen.get_width()-480*k)/2+40*k+135*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k), border_radius=int(5*k))
                            screen.blit(tempsurface2,(0,0))
                            pygame.display.flip()
                            pygame.time.Clock().tick(5)
                            release_mutex(mutex)
                            sys.exit()
                    elif pygame.Rect(int((screen.get_width()-480*k)/2+40*k+270*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k).collidepoint(pygame.mouse.get_pos()) :
                        #取消
                        b=0
                        while b==0:
                            tempsurface2=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
                            screen.blit(screen_surface,(0,0))
                            screen.blit(mask,(0,0))
                            screen.blit(exit_window,(int((screen.get_width()-480*k)/2),int((screen.get_height()-180*k)/2)))
                            pygame.draw.rect(tempsurface2, (255,255,255,84), (int((screen.get_width()-480*k)/2+40*k+270*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k), border_radius=int(5*k))
                            screen.blit(tempsurface2,(0,0))
                            if not any(pygame.mouse.get_pressed()):
                                b=1
                            for event in pygame.event.get():
                                match event.type:
                                    case pygame.MOUSEBUTTONUP | pygame.FINGERUP:
                                            b=1
                            pygame.display.flip()
                            pygame.time.Clock().tick(fps)
                        if pygame.Rect(int((screen.get_width()-480*k)/2+40*k+270*k),int((screen.get_height()-180*k)/2+130*k),110*k,33*k).collidepoint(pygame.mouse.get_pos()) :
                            if currentpage=='rootmainloop':
                                background()
                                showclock(flush=False)
                                draw_lastname(flush=False)
                                fullscreenbutton(flush=False)
                                settingsbutton(flush=False)
                                if reset_namelist==1:
                                    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180) 
                                else:
                                    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
                                globals()['dpup']=time.time()
                                globals()['videoresize']=1
                            else:
                                pass
                            return
                case pygame.VIDEORESIZE:
                        for i in range(2):
                            window_width, window_height = pygame.display.get_surface().get_size()
                            k=_k_()
                            text=pygame.font.SysFont("MicrosoftYaHei UI",int(36*k)).render("还没做好呢……   点击任意位置返回~",True,(255,255,255))
                            mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
                            mask.fill((0,0,0,127))
                            globals()['k']=_k_()
                            proportional_scale(background_image, window_width, window_height)
                            background()
                            if reset_namelist==1:
                                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180) 
                            else:
                               draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
                            clocksurface=pygame.Surface((140*k,40*k),SRCALPHA)
                            clocksurface.fill((0,0,0,0))
                            pygame.draw.rect(clocksurface, (0,0,0,100), (0,0,130*k,40*k), border_radius=int(5*k))
                            buttonsurface=pygame.Surface((100*k,30*k),SRCALPHA)
                            namesurface=pygame.Surface((4.5*150*k+30*k,150*k+60*k),SRCALPHA)
                            pygame.draw.rect(namesurface, (0,0,0,155), (0,0,4.5*150*k+30*k,150*k+60*k), border_radius=int(33*k))
                            buttonx=int((window_width-100*k)/2)
                            buttony=int((window_height-30*k)/2+200*k)
                            sizex=int(100*k)
                            sizey=int(30*k)
                            globals()['fullscreensurface']=pygame.Surface((36*k,36*k) ,SRCALPHA)
                            showclock(flush=False)
                            draw_lastname(flush=False)
                            fullscreenbutton(flush=False )
                            settingsbutton(flush=False )
                            if currentpage=='settingsloop':
                                screensurface.blit(surfacemixer,((screen.get_width()-surfacemixer.get_width())/2,(screen.get_height()-surfacemixer.get_height())/2))
                                screensurface.blit(tempsurface2,((screen.get_width()-tempsurface2.get_width())/2,(screen.get_height()-tempsurface2.get_height())/2))
                            screensurface=pygame.display.get_surface()
                            screen_surface=pygame.Surface(pygame.display.get_surface().get_size(),SRCALPHA)
                            screen_surface.blit(screensurface,(0,0))
                            globals()['fullscreenbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
                            globals()['exitfullscreenbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
                            globals()['settingsurface']=pygame.Surface((36*k,36*k),SRCALPHA)
                            globals()['settingbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\settings.png'),(int(36*k), int(36*k)))
                            mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
                            mask.fill((0,0,0,150))
                            screen.blit(mask,(0,0))
                            exit_window=pygame.Surface((int(480*k),int(180*k)),SRCALPHA)
                            pygame.draw.rect(exit_window, (31,31,31,245), (0,0,480*k,180*k), border_radius=int(8*k))
                            asktext=pygame.font.SysFont("MicrosoftYaHei UI",int(36*k)).render("你真的要退出吗？",True,(255,255,255))
                            exit_window.blit(asktext,(int((exit_window.get_width()-asktext.get_width())/2),int(20*k)))
                            pygame.draw.rect(exit_window, (63,63,63,buttonalpha), (40*k,130*k,110*k,33*k), border_radius=int(5*k))
                            text_1=pygame.font.SysFont("MicrosoftYaHei UI",int(18*k)).render("收起",True,(255,255,255))
                            exit_window.blit(text_1,(int(40*k+(110*k-text_1.get_width())/2),int(130*k+(33*k-text_1.get_height())/2)))
                            pygame.draw.rect(exit_window, (63,63,63,buttonalpha), (175*k,130*k,110*k,33*k), border_radius=int(5*k))
                            text_2=pygame.font.SysFont("MicrosoftYaHei UI",int(18*k)).render("退出",True,(255,255,255))
                            exit_window.blit(text_2,(int(175*k+(110*k-text_2.get_width())/2),int(130*k+(33*k-text_2.get_height())/2)))
                            pygame.draw.rect(exit_window, (63,63,63,buttonalpha), (310*k,130*k,110*k,33*k), border_radius=int(5*k))
                            text_3=pygame.font.SysFont("MicrosoftYaHei UI",int(18*k)).render("取消",True,(255,255,255))
                            exit_window.blit(text_3,(int(310*k+(110*k-text_3.get_width())/2),int(130*k+(33*k-text_3.get_height())/2)))
                            pygame.time.Clock().tick(120)
        pygame.time.Clock().tick(fps)
