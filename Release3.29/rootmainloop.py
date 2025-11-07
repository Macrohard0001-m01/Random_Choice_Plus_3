# 在 rootmainloop.py 中的 rootmainloop 函数开头添加
def rootmainloop():
    global lastmessage, dpup, name, buttonx, buttony, sizex, sizey, k, window_width, window_height, lastname, bg, background_image
    global reset_namelist, message_time, ww, wh, animation, fullscreensurface, clocksurface, namesurface, buttonsurface, barsurface, screen, is_fullscreen
    
    # 检查是否从悬浮按钮恢复
    if hasattr(globals(), 'load') and globals().get('load') == 1:
        print("从悬浮按钮恢复窗口")
        # 恢复窗口显示
        window_width, window_height = screensize
        screen = pygame.display.set_mode(screensize, RESIZABLE | HWSURFACE | DOUBLEBUF | SRCALPHA)
        pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
        # 重置标志
        globals()['load'] = 0
    
    # 原有的初始化代码...
    window_width, window_height = pygame.display.get_surface().get_size()
    name = copy.deepcopy(_name_)
    # ... 其余原有代码
    proportional_scale(background_image, window_width, window_height)
    lastname=firstdraw_lastname
    k=_k_()
    namesurface=pygame.Surface((4.5*150*k+30*k,150*k+60*k),SRCALPHA | HWSURFACE )
    pygame.draw.rect(namesurface, (0,0,0,155), (0,0,4.5*150*k+30*k,150*k+60*k), border_radius=int(33*k))
    background()
    draw_lastname(flush=False)
    fullscreenbutton(flush=False)
    settingsbutton(flush=False )
    pygame.display.flip()
    if used_times==0:
        lastmessage=welcomemessage
        message_time = time.time()
        message(lastmessage)
    globals()['currentpage']='rootmainloop'
    while 1:
        background()
        showclock()
        if time.time()-message_time>=message_time_length and message_time!=0:
            lastmessage=''
            message(lastmessage)
            message_time=0
        if reset_namelist==1:
            if pygame.mouse.get_pos()[0] in range(buttonx,buttonx+sizex) and pygame.mouse.get_pos()[1] in range(buttony,buttony+sizey):
                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(63,63,63),_alpha_=180)
            else:
                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180)
        else:
            if pygame.mouse.get_pos()[0] in range(buttonx,buttonx+sizex) and pygame.mouse.get_pos()[1] in range(buttony,buttony+sizey):
                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(63,63,63),_alpha_=180)
            else:
                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
        pygame.display.update((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k),100*k,30*k))
        if pygame.mouse.get_pos()[0] in range(int(window_width-36*k),window_width) and pygame.mouse.get_pos()[1] in range(int(window_height-36*k),window_height):
            fullscreenbutton('puton')
        else:
            fullscreenbutton()
        if pygame.mouse.get_pos()[0] in range(0,int(36*k)) and pygame.mouse.get_pos()[1] in range(int(window_height-36*k),window_height):
            settingsbutton('puton')
        else:
            settingsbutton()
        if time.time()-dpup>=0.01 and time.time()-dpup<=1 :
            screen.fill((0,0,0))
            background()
            buttonx=int((window_width-100*k)/2)
            buttony=int((window_height-30*k)/2+200*k)
            sizex=int(100*k)
            sizey=int(30*k) 
            draw_lastname(flush=False )
            global fullscreensurface,exitfullscreenbutton_img,fullscreenbutton_img
            fullscreensurface=pygame.Surface((36*k,36*k) ,SRCALPHA)
            fullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
            exitfullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
            globals()['settingsurface']=pygame.Surface((36*k,36*k),SRCALPHA)
            globals()['settingbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\settings.png'),(int(36*k), int(36*k)))
            message(lastmessage)
            showclock(flush=False )
            if reset_namelist==1:
                if pygame.mouse.get_pos()[0] in range(buttonx,buttonx+sizex) and pygame.mouse.get_pos()[1] in range(buttony,buttony+sizey):
                    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(63,63,63),_alpha_=180)
                else:
                    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180)
            else:
                if pygame.mouse.get_pos()[0] in range(buttonx,buttonx+sizex) and pygame.mouse.get_pos()[1] in range(buttony,buttony+sizey):
                    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(63,63,63),_alpha_=180)
                else:
                    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
            if pygame.mouse.get_pos()[0] in range(int(window_width-36*k),window_width) and pygame.mouse.get_pos()[1] in range(int(window_height-36*k),window_height):
                fullscreenbutton('puton')
            else:
                fullscreenbutton()
            if pygame.mouse.get_pos()[0] in range(0,int(36*k)) and pygame.mouse.get_pos()[1] in range(int(window_height-36*k),window_height):
                settingsbutton('puton')
            else:
                settingsbutton()
            pygame.display.flip()
            dpup=0
        event_listening(['button'])
        pygame.time.Clock().tick(fps)