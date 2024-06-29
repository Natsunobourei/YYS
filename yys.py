import cv2,time,random,os,datetime
import os,sys,traceback
import numpy as np
import mss
import action

#检测系统
print('操作系统:', sys.platform)
if sys.platform=='darwin':
    scalar=True
else:
    scalar=False
action.startup()
# 读取文件 精度控制   显示名字
imgs = action.load_imgs()
#pyautogui.PAUSE = 0.05
#pyautogui.FAILSAFE=False

start_time = time.time()
#print('程序启动，现在时间', time.ctime())

#截屏，并裁剪以加速
upleft = (0, 0)
if scalar==True:
    downright = (1136,750)
else:
    downright = (1136, 700)
a,b = upleft
c,d = downright
monitor = {"top": b, "left": a, "width": c, "height": d}
start = time.time()

#constants
last_click=None

#以上启动，载入设置
##########################################################
def select_mode():
    global start
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("运行时间：{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
    print (datetime.datetime.now())

    print('''\n菜单：  按下CTRL+C停止，0退出
        1 结界突破
        2 御魂(司机)
        3 御魂(打手)
        4 御魂/御灵/契灵探查(单刷)
        5 探索(司机)
        6 探索(打手)
        7 探索(单刷)
        8 百鬼夜行
        9 自动斗技
        10 当前活动
        11 结界自动合卡（太阴和伞室内）
        12 厕纸抽卡
        13 蓝蛋升级
        14 秘境召唤
        15 妖气封印/秘闻
        16 契灵boss（单刷）
        17 Debug模式
        ''')
    action.alarm(1)
    raw = input("选择功能模式：")
    try:
        index = int(raw)
    except:
        print('请输入数字')
        select_mode()

    mode = [0, tupo, yuhun, yuhun2, yuhundanren,\
            gouliang, gouliang2, gouliang3,\
            baigui, douji, huodong,\
            card, chouka, shengxing, mijing, yaoqi,\
            qilingdanren, debug]
    try:
        command = mode[index]
    except:
        print('数字超出范围')
        select_mode()

    if index==0:
        action.reset_resolution()
        quit()
    else:
        start = time.time()
        try:
            command()
        except KeyboardInterrupt:
            print('已停止！')
            select_mode()

##########################################################
#结节突破
def tupo():
    last_click=''
    count=0 #总次数
    cishu = 0
    refresh=0
    liaotu=None
    while True :   #直到取消，或者出错
        #截屏
        #im = np.array(mss.mss().grab(monitor))
        #screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        screen=action.screenshot(monitor)
        #cv2.imshow("Image", screen)
        #cv2.waitKey(0)

        #寮突破判断
        if liaotu==None:
            want = imgs['liaotupo']
            size = want[0].shape
            h, w , ___ = size
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                liaotu=True
                print('寮突破')

            want = imgs['gerentupo']
            size = want[0].shape
            h, w , ___ = size
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                liaotu=False
                print('个人突破')

            
        if liaotu==False:
            if cishu >= 31:
                print('进攻次数上限: ',cishu)
                select_mode()

        
        #奖励
        for i in ['jujue','queding',\
                  'shibai','ying','jiangli','jixu',\
                  'jingong','jingong2','jingong3',\
                  'lingxunzhang','lingxunzhang2','lingxunzhang4',\
                  'shuaxin','zhunbei']:
            #print(i)
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target=screen
            pts=action.locate(target,want,0)
            if not len(pts)==0:
                #print('debug: ', last_click,', ', i)
                if last_click==i:
                    if ('jingong' in i or 'lingxunzhang' in i) and liaotu:
                        refresh=refresh+1
                        print('进攻CD，暂停5分钟')
                        t=60*5
                        time.sleep(t)
                        last_click=''
                        continue
                    else:
                        refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                t = random.randint(15,50) / 100
                if i == 'shibai':
                    if cishu>0:
                        cishu = cishu - 1
                    if count>0:
                        count = count - 1
                    print('进攻总次数：',count)
                    t = random.randint(50,100) / 100
                elif 'jingong' in i:
                    if refresh==0:
                        cishu = cishu + 1
                        count=count+1
                    print('进攻总次数。。。：',i,count)
                    t = random.randint(500,800) / 100
                elif 'lingxunzhang' in i:
                    print('选择结界。。。',i)
                    t = random.randint(50,150) / 100
                else:
                    print('突破中。。。',i)
                time.sleep(t)
                break
 

########################################################
#御魂司机
def yuhun():
    last_click=''
    cishu=0
    refresh=0
    while True :
        #鼠标移到最右侧中止    
        

        #截屏
        screen=action.screenshot(monitor)
        
        #print('screen shot ok',time.ctime())
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

        #自动点击通关结束后的页面
        for i in ['jujue','tiaozhan','tiaozhan2',\
                  'moren','queding','querenyuhun','ying',\
                  'jiangli','jiangli2',\
                  'jixu','shibai']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                elif i=='querenyuhun':
                    refresh=refresh+2
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6 or cishu>200:
                    print('进攻次数上限')
                    select_mode()
                
                if i == 'tiaozhan' or i=='tiaozhan2':
                    if refresh==0:
                        cishu=cishu+1
                    print('挑战次数：',cishu)
                    t = random.randint(500,750) / 100
                else:
                    print('挑战中。。。',i)
                    t = random.randint(50,100) / 100
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                time.sleep(t)
                break
    
########################################################
#御魂打手
def yuhun2():
    last_click=''
    cishu=0
    refresh=0
    while True :
        #鼠标移到最右侧中止    
        

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

        #如果队友推出则自己也退出
        want = imgs['tiaozhanhuise']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('队友已退出')
            want = imgs['likaiduiwu']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                
        
        #自动点击通关结束后的页面
        for i in ['jujue','moren','queding','querenyuhun',\
                  'ying','jiangli','jiangli2','jixu',\
                  'jieshou2','jieshou','shibai']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                elif i=='querenyuhun':
                    refresh=refresh+2
                else:
                    refresh=0
                
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                elif refresh==0 and 'jiangli' in i and not last_click=='querenyuhun':
                    #print('last',last_click)
                    cishu=cishu+1
                    print('挑战次数：',cishu)
                print('挑战中。。。',i)
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                last_click=i
                t = random.randint(15,30) / 100
                time.sleep(t)
                break
            

########################################################
#御魂单人
def yuhundanren():
    last_click=''
    cishu=0
    refresh=0
    while True :   #直到取消，或者出错
        

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

        for i in ['jujue','querenyuhun','ying','jiangli','jiangli2','jixu','zhunbei',\
                  'tiaozhan','tiaozhan2','tiaozhan3','queding','tancha','shibai']:
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target=screen
            pts=action.locate(target,want,0)
            if not len(pts)==0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('挑战中。。。',i)
                if i == 'tiaozhan' or i=='tiaozhan2' or i=='tiaozhan3' or i=='tancha':
                    if refresh==0:
                        cishu=cishu+1
                    print('挑战次数：',cishu)
                    if cishu>200:
                        select_mode()
                    t = random.randint(500,800) / 100
                else:
                    t = random.randint(15,30) / 100
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                time.sleep(t)
                break

########################################################
#探索司机
def gouliang():
    last_click=''
    count=0
    refresh=0
    while True:   #直到取消，或者出错
        

        #截屏
        screen=action.screenshot(monitor)

        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足 ')
            select_mode()

        want = imgs['queren']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('确认退出')
            try:
                queding = pts[1]
            except:
                queding = pts[0]
            xy = action.cheat(queding, w, h)
            action.touch(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)

        
        #设定目标，开始查找
        #进入后
        want=imgs['guding']

        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['left']
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('向右走')
                right = (854, 527)
                right = action.cheat(right, 10, 10)
                action.touch(right)
                t = random.randint(50,80) / 100
                time.sleep(t)
                continue

            for i in ['boss', 'jian']:
                want = imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #print('重复次数：',refresh)
                    if refresh>6:
                        print('进攻次数上限')
                        select_mode()
                    
                    if refresh==0:
                        count=count+1
                    print('点击小怪',i)
                    print('探索次数：',count)
                    xx = action.cheat(pts[0], w, h)        
                    action.touch(xx)
                    time.sleep(0.5)
                    break

            if i=='jian' and len(pts)==0:
                for i in ['queren', 'tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    #x1,x2 = upleft, (965, 522)
                    #target = action.cut(screen, x1, x2)
                    target = screen
                    pts = action.locate(target,want,0)
                    if not len(pts) == 0:
                        print('退出中',i)
                        try:
                            queding = pts[1]
                        except:
                            queding = pts[0]
                        queding = action.cheat(queding, w, h)
                        action.touch(queding)
                        t = random.randint(50,80) / 100
                        time.sleep(t)
                        break
                continue

        for i in ['jujue','queding','ying','querenyuhun',\
                  'jiangli','jixu',\
                  'tiaozhan','ditu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                    
                print('领取奖励',i)
                xy = action.cheat(pts[0], w, h )
                action.touch(xy)
                if i=='queding':
                    t = random.randint(150,200) / 100
                else:
                    t = random.randint(15,30) / 100
                time.sleep(t)
                break

########################################################
#探索打手
def gouliang2():
    last_click=''
    refresh=0
    while True:   #直到取消，或者出错
        

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足 ')
            select_mode()
        
        #进入后
        want = imgs['guding']
        pts = action.locate(screen,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['xiao']
            pts = action.locate(screen,want,0)
            
            if not len(pts) == 0:
                print('组队状态中')
            else:
                print('退出重新组队')
                
                for i in ['queren', 'queren2','tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    pts = action.locate(screen,want,0)
                    
                    if not len(pts) == 0:
                        if last_click==i:
                            refresh=refresh+1
                        else:
                            refresh=0
                        last_click=i
                        #print('重复次数：',refresh)
                        if refresh>6:
                            print('进攻次数上限')
                            select_mode()
                        
                        print('退出中',i)
                        try:
                            queding = pts[1]
                        except:
                            queding = pts[0]
                        queding = action.cheat(queding, w, h)
                        action.touch(queding)
                        t = random.randint(50,80) / 100
                        time.sleep(t)
                        break
                continue

        for i in ['jujue','jieshou','querenyuhun','ying',\
                  'jiangli','jixu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if i=='jieshou':
                    a,b=pts[0]
                    if a<50:
                        break
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                    
                print('领取奖励',i)
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                if i=='jieshou' or i=='jieshou1':
                    t = random.randint(15,30) / 100
                else:
                    t = random.randint(15,30) / 100
                time.sleep(t)
                break
            
########################################################
#探索单人
def gouliang3():
    last_click=''
    count=0
    refresh=0
    while True:   #直到取消，或者出错
        

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足 ')
            select_mode()

        want = imgs['queren']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        #x1,x2 = upleft, (965, 522)
        #target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('确认退出')
            try:
                queding = pts[1]
            except:
                queding = pts[0]
            xy = action.cheat(queding, w, h)
            action.touch(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)

        
        #设定目标，开始查找
        #进入后
        want=imgs['guding']

        pts = action.locate(screen,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['left']
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('向右走')
                right = (854, 527)
                right = action.cheat(right, 10, 10)
                action.touch(right)
                t = random.randint(50,80) / 100
                time.sleep(t)
                continue

            for i in ['boss', 'jian']:
                want = imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #print('重复次数：',refresh)
                    if refresh>6:
                        print('进攻次数上限')
                        select_mode()
                    
                    if refresh==0:
                        count=count+1
                    print('点击小怪',i)
                    print('探索次数：',count)
                    if count>500:
                        print('次数上限')
                        select_mode()
                    xx = action.cheat(pts[0], w, h)        
                    action.touch(xx)
                    time.sleep(0.5)
                    break

            if len(pts)==0:
                for i in ['queren','queren2','tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    pts = action.locate(screen,want,0)
                    if not len(pts) == 0:
                        if last_click==i:
                            refresh=refresh+1
                        else:
                            refresh=0
                        last_click=i
                        #print('重复次数：',refresh)
                        if refresh>6:
                            print('进攻次数上限')
                            select_mode()
                    
                        print('退出中',i)
                        try:
                            queding = pts[1]
                        except:
                            queding = pts[0]
                        queding = action.cheat(queding, w, h)
                        action.touch(queding)
                        t = random.randint(50,80) / 100
                        time.sleep(t)
                        break
                continue

        for i in ['jujue','querenyuhun',\
                  'tansuo','ying','jiangli','jixu','c28','ditu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('领取奖励',i)
                xy = action.cheat(pts[0], w, h )
                action.touch(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                break

########################################################
#百鬼
def baigui():
    last_click=''
    refresh=0
    cishu=0
    while True:   #直到取消，或者出错
        

        #截屏
        screen=action.screenshot(monitor)

        #设定目标，开始查找
        #进入后
        for i in ['baigui','gailv','douzihuoqu','miaozhun','baiguijieshu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                refresh=0
                print('点击',i)
                xy = action.cheat(pts[0], w, h )
                action.touch(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                continue

        want=imgs['inbaigui']
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            #print('正在百鬼中')
            want = imgs['blank']
            target = screen
            pts = action.locate(target,want,0)
            if len(pts) == 0:
                refresh=0
                #小怪出现！
                print('点击小怪')
                pts2 = (640, 450)
                xx = action.cheat(pts2, 100, 80)        
                action.touch(xx)
                time.sleep(0.5)
                continue

        i='jinru'
        want = imgs[i]
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            if last_click==i:
                refresh=refresh+1
            else:
                refresh=0
                last_click=i
            print('重复次数：',refresh)
            if refresh>6:
                print('进攻次数上限')
                select_mode()
            cishu=cishu+1
            print('进入百鬼:',cishu)
            xy = action.cheat(pts[0], w, h-10 )
            action.touch(xy)
            t = random.randint(10,20) / 100
            time.sleep(t)

        

        i='kaishi'
        want = imgs[i]
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            refresh=0
            print('选择押注界面')
            i='ya'
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts2 = action.locate(target,want,0)
            if not len(pts2) == 0:
                print('点击开始: ',pts[0])
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
            else:
                #选择押注
                index=random.randint(0,2)
                pts2 = (300+index*340, 500)
                print('选择押注: ',index)
                
                xy = action.cheat(pts2, w, h-10 )
                action.touch(xy)
                t = random.randint(50,100) / 100
                time.sleep(t)

                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)


########################################################
#斗技
def douji():
    last_click=''
    doujipaidui=0
    refresh=0
    cishu=0
    while True:   #直到取消，或者出错
        
        #截屏
        screen=action.screenshot(monitor)

        for i in ['jujue','shoudong','zidong','queren',\
                  'douji','douji2','douji3','douji4','doujilianxi',\
                  'doujiqueren','doujiend','ying','jixu',\
                  'zhunbei','zhunbei2',\
                  'doujiquxiao']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                #print(i)
                if i in ['douji','douji2','douji3','douji4']:
                    i='douji'
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                if i=='douji':
                    if cishu>30:
                        print('斗技次数上限')
                        select_mode()
                    if refresh==0:
                        cishu=cishu+1
                    print('斗技次数：',cishu)
                    xy = action.cheat(pts[0], w, h-10 )
                    action.touch(xy)
                    t = random.randint(150,300) / 100
                    time.sleep(t)
                    break
                elif i=='doujiquxiao':
                    refresh=0
                    doujipaidui=doujipaidui+1
                    print('斗技搜索:',doujipaidui)
                    if doujipaidui>5:
                        doujipaidui=0
                        print('取消搜索')
                        cishu=cishu-1
                        xy = action.cheat(pts[0], w, h-10 )
                        action.touch(xy)
                        t = random.randint(15,30) / 100
                        time.sleep(t)
                        break
                else:
                    print('斗技中。。。',i)
                    xy = action.cheat(pts[0], w, h-10 )
                    action.touch(xy)
                    t = random.randint(50,100) / 100
                    time.sleep(t)
                    break

########################################################
#当前活动
def huodong():
    last_click=''
    count=0
    refresh=0
    while True:   #直到取消，或者出错
        

        #截屏
        screen=action.screenshot(monitor)

        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足 ')
            select_mode()
        
        for i in ['jujue','querenyuhun','queding','hdend',\
                  'hdtiaozhan','hdtiaozhan2','ying','hdsousuo','zhunbei',\
                  'shibai','jixu','liaotianguanbi']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if i=='hdjiacheng':
                    refresh=0
                elif last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                print('活动中',i)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()

                t = 1
                if 'hdtiaozhan' in i:
                    if refresh==0:
                        count=count+1
                    print('挑战次数：',count)
                    t=5
                if i=='hdsousuo':
                    t=5
                if i=='hdend' and False:
                    if refresh==0:
                        print('疲劳度满，休息10分钟')
                        t = 10*60
                        time.sleep(t)
                xy = action.cheat(pts[0], w, h)
                action.touch(xy)
                time.sleep(t)

##########################################################
#合成结界卡
def card():
    last_click=''
    refresh=0
    while True:
        #鼠标移到右侧中止    
        

        #截屏
        screen=action.screenshot(monitor)
        
        for i in ['taiyin2','sanshinei','taiyin3']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('结界卡*',i)
                xy = action.cheat(pts[0], w/2, h-10)
                action.touch(xy)
                break
        if len(pts) == 0:
                print('结界卡不足')
                select_mode()
        

        for i in range(2):
            #截屏
            im = np.array(mss.mss().grab(monitor))
            screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

            want = imgs['taiyin']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if len(pts) == 0:
                print('结界卡不足')
                select_mode()
            else:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click='taiyin'
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('结界卡',i)
                xy = action.cheat(pts[0], w/2, h-10 )
                action.touch(xy)

        #截屏
        screen=action.screenshot(monitor)

        want = imgs['hecheng']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            if last_click==i:
                refresh=refresh+1
            else:
                refresh=0
            last_click='hecheng'
            #print('重复次数：',refresh)
            if refresh>6:
                print('进攻次数上限')
                select_mode()
            
            print('合成中。。。')
            xy = action.cheat(pts[0], w, h-10 )
            action.touch(xy)

        time.sleep(1)

##########################################################
#抽卡
def chouka():
    last_click=''
    count=0
    while True:
        #鼠标移到右侧中止    
        

        #截屏
        screen=action.screenshot(monitor)
        
        want = imgs['zaicizhaohuan']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            if count>200:
                print('次数上限')
                select_mode()
            count=count+1
            print('抽卡中。。。',count)
            xy = action.cheat(pts[0], w, h-10 )
            action.touch(xy)
            #t = random.randint(1,3) / 100
            #time.sleep(t)

##########################################################
#蓝蛋升级
def shengxing():
    last_click=''
    count=0
    refresh=0
    while True:
        #鼠标移到右侧中止    
        

        #截屏
        screen=action.screenshot(monitor)
            
        for i in ['jineng','jixushengxing',\
                  'jixuyucheng','querenshengxing']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('升级中。。。',i)
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                if i=='querenshengxing':
                    if refresh==0:
                        count=count+1
                    print('升级个数：',count)
                    t = random.randint(250,350) / 100
                else:
                    t = random.randint(20,100) / 100
                    
                time.sleep(t)
                
##########################################################
#秘境召唤
def mijing():
    last_click=''
    refresh=0
    while True:
        #鼠标移到右侧中止    
        

        #截屏
        screen=action.screenshot(monitor)
        
        #检测聊天界面
        want = imgs['liaotianguanbi']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            #print('搜索秘境车中。。。')

            for i in ['jujue','mijingzhaohuan','mijingzhaohuan2']:
                want = imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #print('重复次数：',refresh)
                    if refresh>6:
                        print('进攻次数上限')
                        select_mode()
                    
                    print('秘境召唤。。。',i)
                    xy = action.cheat(pts[0], w, h-10 )
                    action.touch(xy)
                    #t = random.randint(10,100) / 100
                    #time.sleep(t)
                    break
        else:
            for i in ['jujue','canjia','liaotian']:
                want = imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #print('重复次数：',refresh)
                    if refresh>6:
                        print('进攻次数上限')
                        select_mode()
                    
                    if i=='canjia':
                        print('加入秘境召唤！',i)
                    xy = action.cheat(pts[0], w, h-10 )
                    action.touch(xy)
                    t = random.randint(10,30) / 100
                    time.sleep(t)
                    break

########################################################
#妖气封印和秘闻
def yaoqi():
    last_click=''
    count=0
    refresh=0
    while True:   #直到取消，或者出错
        

        #截屏
        screen=action.screenshot(monitor)
        
        #委派任务
        for i in ['jujue','jiangli','jixu','zhunbei',\
                  'shibai','zidongpipei','zudui2',\
                  'ying','tiaozhan3','tiaozhan4']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                    
                if i=='zidongpipei' or i=='tiaozhan3' or i=='tiaozhan4':
                    if refresh==0:
                        count=count+1
                    print('次数：',count)
                    t=100/100
                elif i=='shibai':
                    print('自动结束')
                    select_mode()
                else:
                    print('活动中。。。',i)
                    t = random.randint(30,80) / 100
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                time.sleep(t)
                break
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

########################################################
#契灵单人
def qilingdanren():
    last_click=''
    cishu=0
    refresh=0
    while True :   #直到取消，或者出错
        

        #截屏
        screen=action.screenshot(monitor)
        
        #体力不足
        want = imgs['notili']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('体力不足')
            select_mode()

        for i in ['jujue','ying','jiangli','jixu','queding',\
                  'qiling1','mingqi','queren3',\
                  'tiaozhan5','shibai','xiaozhiren']:
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target=screen
            pts=action.locate(target,want,0)
            if not len(pts)==0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click=i
                #print('重复次数：',refresh)
                if refresh>6:
                    print('进攻次数上限')
                    select_mode()
                
                print('挑战中。。。',i)
                if i=='tancha' or i=='tiaozhan5':
                    if refresh==0:
                        cishu=cishu+1
                    print('挑战次数：',cishu)
                    t = random.randint(50,150) / 100
                elif i=='queren3':
                    t = random.randint(350,450) / 100
                else:
                    t = random.randint(15,30) / 100
                xy = action.cheat(pts[0], w, h-10 )
                action.touch(xy)
                time.sleep(t)
                break


##################################################################
def debug():
    #截屏
    #screen=action_adb.screenshot()
    screen=action.screenshot(monitor)
    print('screen: ',screen.shape[1],screen.shape[0])
    cv2.imshow("", screen)
    print('screen: ',screen.shape[1],screen.shape[0])
    print('点击截图，按任意键返回')
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    select_mode()
####################################################
if __name__ == '__main__':
    select_mode()

