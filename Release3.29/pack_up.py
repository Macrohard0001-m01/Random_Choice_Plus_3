# pack_up.py
def pack_up():
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
        
    
    if sys.platform == "win32":
        try:
            import win32gui
            import win32con
            hwnd = pygame.display.get_wm_info()["window"]
            
            # 检查并保存窗口状态
            placement = win32gui.GetWindowPlacement(hwnd)
            was_maximized = (placement[1] == win32con.SW_SHOWMAXIMIZED)
            globals()['window_was_maximized'] = was_maximized
            
            if was_maximized:
                # 如果是最大化状态，先恢复窗口以获取正确位置
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                pygame.time.wait(50)  # 短暂等待窗口恢复
            
            rect = win32gui.GetWindowRect(hwnd)
            globals()['window_position'] = (rect[0], rect[1])
            print(f"窗口位置: {window_position}, 最大化状态: {was_maximized}")
            
        except Exception as e:
            print(f"获取窗口信息失败: {e}")
            # 设置默认位置和状态
            if 'window_position' not in globals():
                globals()['window_position'] = (100, 100)
            globals()['window_was_maximized'] = False
        
    """打包程序为悬浮按钮"""
    global currentpage, screen
    
    print("正在打包为悬浮按钮...")
    
    # 关闭Pygame窗口
    pygame.display.quit()
    
    # 设置当前页面状态
    currentpage = 'packed'
    
    # 在同一线程中直接启动悬浮按钮
    try:
        # 直接从 floatingbutton 模块导入
        from floatingbutton import show_floating_button
        show_floating_button(titleofprogramme)
        print("悬浮按钮已显示")
        
    except Exception as e:
        print(f"启动悬浮按钮失败: {e}")
        screen = pygame.display.set_mode(screensize, RESIZABLE | HWSURFACE | DOUBLEBUF | SRCALPHA)
        currentpage = 'rootmainloop'
        return
    
    # 重新初始化PyGame
    if 'window_position' in globals() and window_position:
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_position[0]},{window_position[1]}"
    
    pygame.init()
    
    # 根据之前的状态设置窗口
    if 'window_was_maximized' in globals() and window_was_maximized:
        # 如果之前是最大化，创建窗口后最大化
        globals()['screen'] = pygame.display.set_mode(screensize, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.RESIZABLE)
        if sys.platform == "win32":
            try:
                hwnd = pygame.display.get_wm_info()["window"]
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            except Exception as e:
                print(f"最大化窗口失败: {e}")
    else:
        globals()['screen'] = pygame.display.set_mode(screensize, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.RESIZABLE)
    
    pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
    pygame.display.set_caption(titleofprogramme)#标题
    
    # 恢复界面
    redraw_mainpage()
    return