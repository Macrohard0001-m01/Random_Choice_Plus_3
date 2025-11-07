def init_items(num,total,totalamount,animation):
    global initbarsurface,lastlength,currentamount,namelist,_name_,init_fpsk
    currentlength=lastlength
    match num:
        case 0:
            global except_name,time,threading,random,copy,datetime,tk,buttonx,buttony,sizex,sizey,fps,used_times,screen,is_fullscreen,barsurface,buttonsurface,window_width, window_height,k,version,screen,clock,settings_img,bar_screen,background_img,name,clocksurface,namesurface
            globals()['reset_namelist']=0
            globals()['message_time']=0
            globals()['dpup']=0
            globals()['used_times']=0
            globals()['sleep_time']=0
            currentamount+=5
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='载入全局变量……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 1:
            import time,threading,random,copy,datetime
            used_times=0
            is_fullscreen=False
            # 删除这里的背景加载代码，因为已经在 config_loader 中加载了
            # try:
            #     globals()['background_image']=pygame.image.load(background_img).convert_alpha()
            # except:
            #     pass
            currentamount+=33
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='读取背景……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 2:
            pygame.display.set_caption(titleofprogramme)#标题
            try:
                pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
            except:
                pass
            currentamount+=3
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='设定窗口……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 3:
            window_width, window_height = pygame.display.get_surface().get_size()
            _k_()
            global fullscreensurface,exitfullscreenbutton_img,fullscreenbutton_img
            fullscreensurface=pygame.Surface((36*k,36*k) ,SRCALPHA)
            fullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
            exitfullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
            globals()['settingbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\settings.png'),(int(36*k), int(36*k)))
            currentamount+=7
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='计算比例系数……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 4:
            namesurface=pygame.Surface((4.5*150*k+30*k,150*k+60*k),SRCALPHA | HWSURFACE )
            pygame.draw.rect(namesurface, (0,0,0,155), (0,0,4.5*150*k+30*k,150*k+60*k), border_radius=int(33*k))
            clocksurface=pygame.Surface((140*k,40*k),SRCALPHA | HWSURFACE )
            buttonsurface=pygame.Surface((100*k,30*k),SRCALPHA | HWSURFACE )
            globals()['settingsurface']=pygame.Surface((36*k,36*k),SRCALPHA | HWSURFACE )
            barsurface=pygame.Surface((0,0),SRCALPHA | HWSURFACE )
            pygame.draw.rect(clocksurface, (0,0,0,100), (0,0,130*k,40*k), border_radius=int(5*k))
            currentamount+=32
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='创建表面……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 5:
            buttonx=int((window_width-100*k)/2)
            buttony=int((window_height-30*k)/2+200*k)
            sizex=int(100*k)
            sizey=int(30*k)
            currentamount+=6
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='创建变量……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 6:
            try:
                with open(name_text,'r') as namelist:
                    _name_ = [line.strip() for line in namelist if line.strip()]
            except:
                _name_=['error0001']
                print("主名单加载错误")  # 防止崩溃
            try:
                with open(except_names,'r') as exceptnamelist:
                    except_name = [line.strip() for line in exceptnamelist if line.strip()]
            except:
                globals()['except_name'] = ['error0002']
                print("排除名单加载错误")  # 防止崩溃
            currentamount+=14
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='读取名单……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
    if animation:
        if currentlength<4:
            currentlength=4
        screen.blit(init_background,(0,0))
        screen.blit(mask,(0,0))
        loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
        screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        pygame.draw.rect(screen, (255,255,255,255), ((screen.get_width()-720)/2,screen.get_height()/2+150,currentlength,5), border_radius=2)
        loadingpercent=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render((str("%.2f"%(currentlength*100/720))+'%'),True,(255,255,255))
        screen.blit(loadingpercent,((screen.get_width()-720)/2+730,screen.get_height()/2+140))
        pygame.display.flip()
        while currentlength<720*(currentamount)/totalamount:
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            pygame.draw.rect(screen, (255,255,255,255), ((screen.get_width()-720)/2,screen.get_height()/2+150,currentlength,5), border_radius=2)
            loadingpercent=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render((str("%.2f"%(currentlength*100/720))+'%'),True,(255,255,255))
            screen.blit(loadingpercent,((screen.get_width()-720)/2+730,screen.get_height()/2+140))
            currentlength+=int(animationspeed/init_fpsk)
            pygame.display.update((0,415,960,15))
            pygame.time.Clock().tick(init_fps)
        lastlength=currentlength
    else :
        screen.blit(init_background,(0,0))
        screen.blit(mask,(0,0))
        loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
        screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        pygame.draw.rect(screen, (255,255,255,255), ((screen.get_width()-720)/2,screen.get_height()/2+150,currentlength,5), border_radius=2)
        loadingpercent=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render((str("%.2f"%(currentlength*100/720))+'%'),True,(255,255,255))
        screen.blit(loadingpercent,((screen.get_width()-720)/2+730,screen.get_height()/2+140))
        pygame.draw.rect(screen, (255,255,255,255), ((screen.get_width()-720)/2,screen.get_height()/2+150,720/totalamount*(currentamount),5), border_radius=2)
        pygame.display.flip()
    if 720/total*(num+1)<720:
        pygame.time.Clock().tick(15)
    else:
        pygame.time.Clock().tick(init_fps)