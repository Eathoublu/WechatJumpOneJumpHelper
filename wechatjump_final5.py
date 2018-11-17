# * * *-*- coding: utf-8 -*- * * *
# * * * * EATHOUBLU STUDIO * * * *
# * * *  version : 1.2.7.0   * * *

import os
import subprocess as sb
from PIL import Image as im
import time
import random
import aircv as ac


def getscreenshot():
    ps = sb.Popen(
        '/Users/eathoublu/Desktop/brew-master/Caskroom/android-platform-tools/27.0.1/platform-tools/adb  shell screencap -p ',
        shell=True, stdout=sb.PIPE)
    ss = ps.stdout.read()
    ss = ss.replace(b'\r\n', b'\n')
    with open('autojump{}.png'.format(str(cont)), 'wb') as f:
        f.write(ss)
    # as for here,suceed.

def loadShot():
    img = im.open('autojump{}.png'.format(str(cont)))
    imgPixelMatrix = img.load()
    return imgPixelMatrix

def findLittlePeople(imgPixelMatrix):


 for h in range(1920*2//3, 1920//3, -1):
    isFindP = False
    for w in range(1080*7//8, 1080//8, -1):
        pixelPeople = imgPixelMatrix[w, h]
        if(50<pixelPeople[0])and(pixelPeople[0]<60)and(53<pixelPeople[1])and(pixelPeople[1]<63)and(95<pixelPeople[2])and(pixelPeople[2]<110)and(isFindP == False):
            pL = w
            isFindP = True
        if (50 < pixelPeople[0]) and (pixelPeople[0] < 60) and (53 < pixelPeople[1]) and (pixelPeople[1] < 63) and (
                95 < pixelPeople[2]) and (pixelPeople[2] < 110):
            pR = w
    if(isFindP == True):
        print '小人的坐标为：', (pR+pL)//2 , h
        return (pR+pL)//2 , h
 print'哎呀！死啦5555'
 exit(0)

def findUpBoard(imgPixelMatrix):


 for h in range(1920//4, 1920*3//4):
    pixel = imgPixelMatrix[1, h]
    for w in range(1080//8, 1080*7//8):
        pixel1 = imgPixelMatrix[w, h]
        if (abs(pixel[0]-pixel1[0])>10)or (abs(pixel[1]-pixel1[1])>10)or(abs(pixel[2]-pixel1[2])>10):
            print '上边界为：', w, h
            return w, h


def find_real_board(px, py):
    for h in range(1920 // 4, (py - 70)):
        pixel = imgPixelMatrix[1, h]
        for w in range(0, (px - 50)):
            pixel1 = imgPixelMatrix[w, h]
            if (abs(pixel[0] - pixel1[0]) > 10) or (abs(pixel[1] - pixel1[1]) > 10) or (abs(pixel[2] - pixel1[2]) > 10):
                print '更新后的上边界为：', w, h
                return w, h
#可以成功找到左边的点
    for h in range(1920 // 4, (py - 70)):
        pixel = imgPixelMatrix[1, h]
        for w in range((px + 50),1079):
            pixel1 = imgPixelMatrix[w, h]
            if (abs(pixel[0] - pixel1[0]) > 10) or (abs(pixel[1] - pixel1[1]) > 10) or (abs(pixel[2] - pixel1[2]) > 10):
                print '更新后的上边界为：', w, h
                return w, h
# 可以成功找到右边的点

# 不打括号，打出来是汉字，打了括号，打出来是编码。

def isThereABottle(py):
    img = im.open('autojump{}.png'.format(str(cont)))
    imgDidCut = img.crop((0, 0, 1079, py-30))
    imgDidCut.save("findBottle.png")
    Reload = ac.imread('findBottle.png')
    bottle = ac.imread('bottle.png')
    pos = ac.find_template(Reload, bottle)
    if pos['confidence']>0.98 :
        print '喵～发现一个瓶子！'
        return pos['result'][0], pos['result'][1], 1
    return 0, 0, 0

def findTargetObject(py):
    # if (cont % x == 0):
    #      print '喵～'
    #      return 0, 0, 0   #设定选择模式之后，喵机制不启用
    img = im.open('autojump{}.png'.format(str(cont)))
    imgDidCut = img.crop((0, 0, 1079, py - 80))
    imgDidCut.save("findTarget.png")
    Reload = ac.imread('findTarget.png')
    for i in range(1, 80):
     try:
      if mode == 1:   # 疯狂模式
          target = ac.imread('Targets/t{}.png'.format(str(i)))
      else : # 稳定模式
          target = ac.imread('Normal Targets/t{}.png'.format(str(i)))
      pos = ac.find_template(Reload, target)
      if pos['confidence'] > precision:
         print '喵～发现一个标志物啦！这个标志物是：t' , i
         return pos['result'][0], pos['result'][1], 1
     except:
         continue
    return 0, 0, 0



def jump(px, py, ux, uy):
    dis = ((px-ux)**2+(py-uy)**2)**0.5
    print '距离为：', dis
    if (dis<220):
        print '更新坐标中...'
        # if the people head is taller than the up board
        ux,uy = find_real_board(px, py)
        dis = ((px - ux) ** 2 + (py - uy) ** 2) ** 0.5
        print '更新后的距离为：', dis
    if(dis>600):
        ratio = 1.23
    else:
        ratio = 1.20
    if cont>40:
        ratio = 1.23
    # if cont>80:
    #     ratio = 1.35
    if cont>45 :
      newX, newY, bottle = isThereABottle(py)
      if(bottle == 1):
        print '最后更新瓶盖中心的坐标为：', newX , newY-50
        ratio = 1.35
        dis = ((px - newX) ** 2 + (py - (newY-50)) ** 2) ** 0.5
        print '最后更新瓶盖到小人的距离为：', dis
        print '使用"百发百中"一技能！啦啦啦'
        preesTime = int((dis) * ratio)  # 1.23表现不错
        data = [100 + random.random() * 500, 200 + random.random() * 800, preesTime]
        # jump command
        str_set = '/Users/eathoublu/Desktop/brew-master/Caskroom/android-platform-tools/27.0.1/platform-tools/adb shell input swipe  {d[0]} {d[1]} {d[0]} {d[1]} {d[2]}'.format(
            d=data)
        os.popen(str_set)
        return 0
    if cont>=1 :
      newX, newY, target = findTargetObject(py)
      if(target == 1):
        print '最后更新目标中心的坐标为：', newX , newY
        ratio = 1.35
        dis = ((px - newX) ** 2 + (py - newY) ** 2) ** 0.5
        print '最后更新目标到小人的距离为：', dis
        print '使用"百发百中"二技能！啦啦啦'
        preesTime = int((dis) * ratio)  # 1.23表现不错
        data = [100 + random.random() * 500, 200 + random.random() * 800, preesTime]
        # jump command
        str_set = '/Users/eathoublu/Desktop/brew-master/Caskroom/android-platform-tools/27.0.1/platform-tools/adb shell input swipe  {d[0]} {d[1]} {d[0]} {d[1]} {d[2]}'.format(
            d=data)
        os.popen(str_set)
        return 0


    preesTime = int((dis)*ratio) #1.23表现不错
    data = [100+random.random()*500, 200+random.random()*800, preesTime]
    # jump command
    str_set = '/Users/eathoublu/Desktop/brew-master/Caskroom/android-platform-tools/27.0.1/platform-tools/adb shell input swipe  {d[0]} {d[1]} {d[0]} {d[1]} {d[2]}'.format(d = data)
    os.popen(str_set)
    return 0


if __name__ == '__main__':
 print '欢迎使用EATHOUBLU️ STUDIO(艺术世界工作室)微信跳一跳作弊器 这将是一场难忘的经历'
 print '正在初始化...请稍后...'
 cont = 1
 precision = 0.91
 # 0.95也是不错的系数 0.93
 mode = input('请键入你想要的模式：1、疯狂模式（一定会被判作弊，成绩不显示）2、稳定模式（可以以十分稳定的状态拿到很高分）3、专家模式（启动稳定模式，但自定义精度）4、混合模式（coming soon...）')
 if (mode == 3):
     mode = 2
     precision = input('请输入精度:')
 # x = 3
 if (mode == 4):
     print('该模式正在建设中，自动转入稳定模式')
     mode = 2

 while True:
    getscreenshot()
    imgPixelMatrix = loadShot()
    px, py = findLittlePeople(imgPixelMatrix)
    ux, uy = findUpBoard(imgPixelMatrix)
    jump(px, py, ux, uy)
    time.sleep(1+random.random()*1.2)
    cont = cont + 1

    print '第', cont , '次迭代'