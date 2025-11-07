def init():
    global MHicon,initbarsurface,screen,lastlength,init_background,mask,currentamount
    global choose_manager, drop_rate_manager, choose_mode, balance_weight, smart_sensitivity, enable_drop_rate
    
    # 第一次加载配置（不加载图片）
    load_config_to_globals('config.ini')

    if is_already_running():
        sys.exit()
    if startwindowpositioncontrol:
        try:
            os.environ['SDL_VIDEO_WINDOW_POS'] = startwindowposition
        except:
            pass
    
    pygame.init()    #初始化pygame
    screen = pygame.display.set_mode((960,540),RESIZABLE | HWSURFACE | DOUBLEBUF | SRCALPHA | NOFRAME )      #界面大小
    pygame.display.set_caption(titleofprogramme)#标题
    pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
    
    itemscount=7          #要加载的项数

    try:
        # 随机选择背景图片
        init_bg_dir = globals().get('init_bg_directory', './images/backgrounds/init_bg')
        main_bg_dir = globals().get('main_bg_directory', './images/backgrounds/main_bg')
        use_random_bg = globals().get('use_random_bg', True)

        if use_random_bg:
            random_init_bg = get_random_image_from_directory(init_bg_dir)
            random_main_bg = get_random_image_from_directory(main_bg_dir)

            if random_init_bg:
                print(f"随机选择的载入界面背景: {random_init_bg}")
                globals()['init_background_path'] = random_init_bg
            else:
                globals()['init_background_path'] = init_background
                print("未找到随机载入界面背景，使用默认")

            if random_main_bg:
                print(f"随机选择的主界面背景: {random_main_bg}")
                globals()['background_img_path'] = random_main_bg
            else:
                globals()['background_img_path'] = background_img
                print("未找到随机主界面背景，使用默认")
        else:
            globals()['init_background_path'] = init_background
            globals()['background_img_path'] = background_img

        # 加载为pygame Surface对象
        globals()['init_background'] = pygame.image.load(init_background_path).convert_alpha()
        globals()['background_image'] = pygame.image.load(background_img_path).convert_alpha()
        globals()['MHicon'] = pygame.image.load(MHicon)

    except Exception as e:
        print(f"加载图片时出错: {e}")
    
    # 缩放初始化背景
    init_background = pygame.transform.smoothscale(
        init_background,
        (int(init_background.get_width()*max(screen.get_width()/init_background.get_width(), screen.get_height()/init_background.get_height())), 
         int(init_background.get_height()*max(screen.get_width()/init_background.get_width(), screen.get_height()/init_background.get_height())))
    )
    
    # ... 其余代码保持不变 ...
    
    screen.blit(init_background,(0,0))
    mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    mask.fill((0,0,0,init_background_alpha))
    
    # 缩放MHicon
    MHicon = pygame.transform.smoothscale(MHicon,(int(MHicon.get_width()*0.08), int(MHicon.get_height()*0.08)))
    
    mask.blit(MHicon,((mask.get_width()-MHicon.get_width())/2,0))
    MHtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(33)).render('Macrohard®',True,(255,255,255))
    mask.blit(MHtext,((mask.get_width()-MHtext.get_width())/2+10,MHicon.get_height()-25))
    screen.blit(mask,(0,0))
    pygame.display.flip()
    pygame.time.Clock().tick(1)
    
    # ... 其余代码保持不变 ...
    screen.blit(init_background,(0,0))
    softwaretext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(40),bold=True ).render(packagename,True,(255,255,255))
    mask.blit(softwaretext,((mask.get_width()-softwaretext.get_width())/2,MHicon.get_height()+MHtext.get_height()-25))
    versiontext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(20),bold=True ).render(version,True,(255,255,255))
    mask.blit(versiontext,((mask.get_width()-softwaretext.get_width())/2+softwaretext.get_width()+10,MHicon.get_height()+MHtext.get_height()-25+softwaretext.get_height()-versiontext.get_height()))
    screen.blit(mask,(0,0))
    pygame.display.flip()
    pygame.time.Clock().tick(30)
    screen.blit(init_background,(0,0))
    initbarsurface=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    pygame.draw.rect(mask, (127,127,127,180), ((screen.get_width()-720)/2,screen.get_height()/2+150,720,5), border_radius=2)
    screen.blit(mask,(0,0))
    pygame.display.flip()
    lastlength=0
    currentamount=0
    globals()['init_fpsk']=init_fps/360
    for i in range(itemscount):       #载入内容的循环
        init_items(i,itemscount,100,animation)   #加载的某一项
        pygame.event.get()
    screen.blit(init_background,(0,0))
    screen.blit(mask,(0,0))
    loadingpercent=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(('100.00%'),True,(255,255,255))
    screen.blit(loadingpercent,((screen.get_width()-720)/2+730,screen.get_height()/2+140))
    ldtext='已完成！正在载入……'
    loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
    screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
    if animation:
        for i in range(int(63*init_fpsk)):
            pygame.draw.rect(initbarsurface, (0,191,0,int(4/init_fpsk)), ((screen.get_width()-720)/2,screen.get_height()/2+150,720,5), border_radius=2)
            screen.blit(initbarsurface,(0,0))
            pygame.display.flip()
            pygame.time.Clock().tick(init_fps)
    else:
        pygame.draw.rect(screen, (0,191,0,255), ((screen.get_width()-720)/2,screen.get_height()/2+150,720,5), border_radius=2)
        pygame.display.flip()
        pygame.time.Clock().tick(init_fps)
    tempsurface=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    pygame.draw.rect(tempsurface,(0,0,0,int(10/init_fpsk)),(0,0,tempsurface.get_width(),tempsurface.get_height()))
    for i in range(int(63*init_fpsk)):
        screen.blit(tempsurface,(0,0))
        pygame.display.flip()
        pygame.time.Clock().tick(init_fps)
    screen = pygame.display.set_mode(screensize,RESIZABLE | HWSURFACE | DOUBLEBUF | SRCALPHA)
    pygame.time.Clock().tick(init_fps)
    backgroundimage=proportional_scale(background_image, window_width, window_height)
    global tempsurface_2
    tempsurface_2=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    tempsurface_2.blit(backgroundimage,(0,0))
    global lastname
    lastname=firstdraw_lastname
    draw_lastname(flush=False,temp=True)
    lastmessage=welcomemessage
    message(lastmessage,flush=False,temp=True)
    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180,temp=True)  
    fullscreenbutton(flush=False,temp=True)
    settingsbutton(flush=False,temp=True)
    for i in range(int(63*init_fpsk)):
        tempsurface.fill((0,0,0,0))
        screen.blit(tempsurface_2,(0,0))
        showclock(flush=False)
        pygame.draw.rect(tempsurface,(0,0,0,int(255-4*i/init_fpsk)),(0,0,tempsurface.get_width(),tempsurface.get_height()))
        screen.blit(tempsurface,(0,0))
        pygame.display.flip()
        pygame.time.Clock().tick(init_fps)
    
    # 初始化点名管理器
    try:
        from choose_manager import choose_manager
        print("✅ 点名管理器初始化成功")
    except Exception as e:
        print(f"❌ 点名管理器初始化失败: {e}")
        # 创建临时的空管理器
        class DummyManager:
            def __init__(self):
                self.history_data = {}
                self.today_data = {}
            def record_choice(self, name): pass
            def get_choice_count(self, name, mode): return 0
            def clear_history(self): pass
            def clear_today(self): pass
        choose_manager = DummyManager()
    
    # 初始化爆率管理器 - 修复这里！
    try:
        from drop_rate_manager import drop_rate_manager
        # drop_rate_manager 在初始化时已经自动加载数据，不需要再次调用
        print("✅ 爆率管理器初始化成功")
    except Exception as e:
        print(f"❌ 爆率管理器初始化失败: {e}")
        # 创建临时的空管理器 - 修复这个类！
        class DummyDropManager:
            def __init__(self):
                self.auto_rates = {}
                self.manual_rates = {}
            def get_drop_rate(self, name, use_manual_override=True): 
                return 1.0
            def set_drop_rate(self, name, rate, is_manual=True): 
                return True
            def update_from_list(self, name_list):
                return False, []
            def reset_drop_rate(self, name):
                return True
            def reset_all_drop_rates(self):
                return True
        drop_rate_manager = DummyDropManager()
    
    print(f"📝 点名模式: {choose_mode}, 平衡权重: {balance_weight}, 智能敏感度: {smart_sensitivity}, 启用爆率: {enable_drop_rate}")
    
    # 根据初始名单更新爆率配置
    if enable_drop_rate and _name_:
        drop_rate_manager.update_from_list(_name_)
        print("✅ 爆率配置已根据名单更新")
    
    globals()['sleep_time']=time.time()
    rootmainloop()