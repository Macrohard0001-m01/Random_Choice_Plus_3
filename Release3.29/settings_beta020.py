def settingsmainloop():
        def videoresize_process():
            global videoresize,surfacemixer,tempsurface,mask,setting_surface,namesurface,buttonsurface,clocksurface,window_width,window_height,screen_surface,window_width , window_height , lastmessage , k,sizex,sizey,buttonx,buttony
            for i in range(2):
                window_width, window_height = pygame.display.get_surface().get_size()
                k=_k_()
                mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA| HWSURFACE )
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
                buttonsurface=pygame.Surface((100*k,30*k),SRCALPHA| HWSURFACE )
                namesurface=pygame.Surface((4.5*150*k+30*k,150*k+60*k),SRCALPHA| HWSURFACE )
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
                screensurface=pygame.display.get_surface()
                screen_surface=pygame.Surface(pygame.display.get_surface().get_size(),SRCALPHA| HWSURFACE )
                screen_surface.blit(screensurface,(0,0))
                globals()['fullscreenbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
                globals()['exitfullscreenbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
                globals()['settingsurface']=pygame.Surface((36*k,36*k),SRCALPHA| HWSURFACE )
                globals()['settingbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\settings.png'),(int(36*k), int(36*k)))
                surfacemixer=pygame.Surface(pygame.display.get_surface().get_size(),SRCALPHA| HWSURFACE )
                #开始混合表面↓
                surfacemixer.blit(screen_surface,(0,0))
                surfacemixer.blit(mask,(0,0))
                surfacemixer.blit(setting_surface,((screen.get_width()-setting_surface.get_width())/2,(screen.get_height()-setting_surface.get_height())/2))
                videoresize=0
                pygame.time.Clock().tick(120)
        
        def wait_until_mousebuttonup():
            b=0
            while b==0:
                if not any(pygame.mouse.get_pressed()):
                    b=1
                for event in pygame.event.get():
                    match event.type:
                        case pygame.MOUSEBUTTONUP | pygame.FINGERUP:
                            if pygame.mouse.get_pos()[0] in range(int(((screen.get_width()-setting_surface.get_width())/2+760)),int(((screen.get_width()-setting_surface.get_width()+760))/2+85)) and pygame.mouse.get_pos()[1] in range(int(((screen.get_height()-setting_surface.get_height())/2+495)),int(((screen.get_height()-setting_surface.get_height())/2+495)+30)):
                                b=1
                pygame.time.Clock().tick(60)
        
        def public_press_checker():
            global settings_page
            if pygame.Rect(int(((screen.get_width()-setting_surface.get_width())/2+560)),int(((screen.get_height()-setting_surface.get_height())/2+495)),85,30).collidepoint(pygame.mouse.get_pos()) :
                animation_tempsurface.fill((0,0,0,0))
                pygame.draw.rect(animation_tempsurface, (255,255,255,100), (560,495,85,30), border_radius=3)
                screen.blit(animation_tempsurface,((screen.get_width()-animation_tempsurface.get_width())/2,(screen.get_height()-animation_tempsurface.get_height())/2))
                pygame.display.flip()
                b=0
                wait_until_mousebuttonup()
                if pygame.mouse.get_pos()[0] in range(int(((screen.get_width()-setting_surface.get_width())/2+560)),int(((screen.get_width()-setting_surface.get_width())/2+560)+85)) and pygame.mouse.get_pos()[1] in range(int(((screen.get_height()-setting_surface.get_height())/2+495)),int(((screen.get_height()-setting_surface.get_height())/2+495)+30)):
                    screen.blit(surfacemixer,(0,0))
                    screen.blit(tempsurface,((screen.get_width()-tempsurface.get_width())/2,(screen.get_height()-tempsurface.get_height())/2))
                    pygame.display.flip()
                    settings_page=None
                    return 'exit'
            elif pygame.Rect(int(((screen.get_width()-setting_surface.get_width())/2+760)),int(((screen.get_height()-setting_surface.get_height())/2+495)),85,30).collidepoint(pygame.mouse.get_pos()) :
                animation_tempsurface.fill((0,0,0,0))
                pygame.draw.rect(animation_tempsurface, (255,255,255,100), (760,495,85,30), border_radius=3)
                screen.blit(animation_tempsurface,((screen.get_width()-animation_tempsurface.get_width())/2,(screen.get_height()-animation_tempsurface.get_height())/2))
                pygame.display.flip()
                wait_until_mousebuttonup()
                if pygame.mouse.get_pos()[0] in range(int(((screen.get_width()-setting_surface.get_width())/2+760)),int(((screen.get_width()-setting_surface.get_width())/2+760)+85)) and pygame.mouse.get_pos()[1] in range(int(((screen.get_height()-setting_surface.get_height())/2+495)),int(((screen.get_height()-setting_surface.get_height())/2+495)+30)):
                    screen.blit(surfacemixer,(0,0))
                    screen.blit(tempsurface,((screen.get_width()-tempsurface.get_width())/2,(screen.get_height()-tempsurface.get_height())/2))
                    pygame.display.flip()
                    load_config_to_globals('config.ini')
                    settings_page=None
                    return  'exit'
        
        global settings_page,videoresize,surfacemixer,tempsurface,mask,setting_surface,namesurface,buttonsurface,clocksurface,window_width,window_height,screen_surface,window_width , window_height , lastmessage , k,sizex,sizey,buttonx,buttony
        videoresize=0
        draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
        fullscreenbutton(flush=False)
        screensurface=pygame.display.get_surface()
        screen_surface=pygame.Surface(pygame.display.get_surface().get_size(),SRCALPHA| HWSURFACE )
        screen_surface.blit(screensurface,(0,0))
        mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA| HWSURFACE )
        mask.fill((0,0,0,127))
        settings_page=0
        #表面混合以减少渲染开销↓
        surfacemixer=pygame.Surface(pygame.display.get_surface().get_size(),SRCALPHA| HWSURFACE )
        #设置的主表面↓
        setting_surface=pygame.Surface((960,540),SRCALPHA| HWSURFACE )
        #边框↓
        pygame.draw.rect(setting_surface, (16,16,16,200), (0,0,960,540), border_radius=8)
        pygame.draw.rect(setting_surface, (255,255,255,200), (0,0,960,540), 3, border_radius=8)
        #分割线↓
        pygame.draw.rect(setting_surface, (255,255,255,200), (150,0,2,480), border_radius=1)
        pygame.draw.rect(setting_surface, (255,255,255,200), (0,480,960,2), border_radius=1)
        #侧栏分割线↓
        pygame.draw.rect(setting_surface, (255,255,255,200), (0,60,150,2), border_radius=1)
        pygame.draw.rect(setting_surface, (255,255,255,200), (0,120,150,2), border_radius=1)
        pygame.draw.rect(setting_surface, (255,255,255,200), (0,180,150,2), border_radius=1)
        pygame.draw.rect(setting_surface, (255,255,255,200), (0,240,150,2), border_radius=1)
        pygame.draw.rect(setting_surface, (255,255,255,200), (0,300,150,2), border_radius=1)
        pygame.draw.rect(setting_surface, (255,255,255,200), (0,360,150,2), border_radius=1)
        pygame.draw.rect(setting_surface, (255,255,255,200), (0,420,150,2), border_radius=1)
        #按钮↓
        pygame.draw.rect(setting_surface, (60,60,60,180), (15,495,75,30), border_radius=3)
        pygame.draw.rect(setting_surface, (60,60,60,180), (105,495,75,30), border_radius=3)
        pygame.draw.rect(setting_surface, (60,60,60,180), (560,495,85,30), border_radius=3)
        pygame.draw.rect(setting_surface, (60,60,60,180), (660,495,85,30), border_radius=3)
        pygame.draw.rect(setting_surface, (60,60,60,180), (760,495,85,30), border_radius=3)
        pygame.draw.rect(setting_surface, (60,60,60,180), (860,495,85,30), border_radius=3)
        #按钮文字↓
        text1=pygame.font.SysFont("MicrosoftYaHei UI",22).render("导入",True,(255,255,255))
        setting_surface.blit(text1,(15+(75-text1.get_width())/2,495+(30-text1.get_height())/2-2))
        text2=pygame.font.SysFont("MicrosoftYaHei UI",22).render("导出",True,(255,255,255))
        setting_surface.blit(text2,(105+(75-text2.get_width())/2,495+(30-text2.get_height())/2-2))
        text3=pygame.font.SysFont("MicrosoftYaHei UI",22).render("仅本次",True,(255,255,255))
        setting_surface.blit(text3,(560+(85-text3.get_width())/2,495+(30-text3.get_height())/2-2))
        text4=pygame.font.SysFont("MicrosoftYaHei UI",22).render("确定",True,(255,255,255))
        setting_surface.blit(text4,(660+(85-text4.get_width())/2,495+(30-text4.get_height())/2-2))
        text5=pygame.font.SysFont("MicrosoftYaHei UI",22).render("取消",True,(255,255,255))
        setting_surface.blit(text5,(760+(85-text5.get_width())/2,495+(30-text5.get_height())/2-2))
        text6=pygame.font.SysFont("MicrosoftYaHei UI",22).render("应用",True,(255,255,255))
        setting_surface.blit(text6,(860+(85-text6.get_width())/2,495+(30-text6.get_height())/2-2))
        #侧栏文字↓
        text7=pygame.font.SysFont("MicrosoftYaHei UI",32,bold=True).render("设   置",True,(255,255,255))
        setting_surface.blit(text7,((150-text7.get_width())/2,(60-text7.get_height())/2))
        text8=pygame.font.SysFont("MicrosoftYaHei UI",24).render("基本",True,(255,255,255))
        setting_surface.blit(text8,((150-text8.get_width())/2,60+(60-text8.get_height())/2))
        text9=pygame.font.SysFont("MicrosoftYaHei UI",24).render("高级",True,(255,255,255))
        setting_surface.blit(text9,((150-text9.get_width())/2,120+(60-text9.get_height())/2))
        text10=pygame.font.SysFont("MicrosoftYaHei UI",24).render("性能",True,(255,255,255))
        setting_surface.blit(text10,((150-text10.get_width())/2,180+(60-text10.get_height())/2))
        text11=pygame.font.SysFont("MicrosoftYaHei UI",24).render("点名",True,(255,255,255))
        setting_surface.blit(text11,((150-text11.get_width())/2,240+(60-text11.get_height())/2))
        text12=pygame.font.SysFont("MicrosoftYaHei UI",24).render("名单",True,(255,255,255))
        setting_surface.blit(text12,((150-text12.get_width())/2,300+(60-text12.get_height())/2))
        text13=pygame.font.SysFont("MicrosoftYaHei UI",24).render("开发者",True,(255,255,255))
        setting_surface.blit(text13,((150-text13.get_width())/2,360+(60-text13.get_height())/2))
        text14=pygame.font.SysFont("MicrosoftYaHei UI",24).render("关于",True,(255,255,255))
        setting_surface.blit(text14,((150-text14.get_width())/2,420+(60-text14.get_height())/2))
        #临时文字↓
        text15=pygame.font.SysFont("MicrosoftYaHei UI",28).render("←在左侧选择一项以进行设置",True,(255,255,255))
        #临时表面
        tempsurface=pygame.Surface((960,540),SRCALPHA | HWSURFACE )
        tempsurface.blit(text15,(150+(810-text15.get_width())/2,(480-text15.get_height())/2))
        animation_tempsurface=pygame.Surface((960,540),SRCALPHA| HWSURFACE )
        #开始混合表面↓
        surfacemixer.blit(screen_surface,(0,0))
        surfacemixer.blit(mask,(0,0))
        surfacemixer.blit(setting_surface,((screen.get_width()-setting_surface.get_width())/2,(screen.get_height()-setting_surface.get_height())/2))
        
        while settings_page==0:
            screen.blit(surfacemixer,(0,0))
            screen.blit(tempsurface,((screen.get_width()-tempsurface.get_width())/2,(screen.get_height()-tempsurface.get_height())/2))
            pygame.display.flip()
            if videoresize==1:
                videoresize_process()
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT :
                        exitwindow()
                    case pygame.VIDEORESIZE:
                        videoresize_process()
                    case pygame.MOUSEBUTTONDOWN | pygame.FINGERDOWN :
                        x=public_press_checker()
                        if x=='exit':
                            break 
        window_width, window_height = pygame.display.get_surface().get_size()
        globals()['k']=_k_()
        proportional_scale(background_image, window_width, window_height)
        background()
        showclock(flush=False)
        draw_lastname(flush=False)
        fullscreenbutton(flush=False )
        settingsbutton(flush=False )
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
        globals()['dpup']=time.time()
   