import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1600, 900
KEY_DICT = {pg.K_UP:(0,-5),pg.K_DOWN:(0,5),      # 各キーに応じた縦横の移動量の辞書。
            pg.K_LEFT:(-5,0),pg.K_RIGHT:(5,0),}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def InOut(rct:pg.Rect) -> tuple[bool,bool]:
    """"
    引数:判定したいRect(今回の場合、こうかとんRect or 爆弾Rect)
    戻り値:横、縦方向の真理値タプル(True:画面内 / False:画面外)
    Rectオブジェクトleft,right,top,bottomの値から画面内、外を判断する
    """
    yoko, tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate


def Rotate(image:pg.Surface):
    """
    引数:回転させるSurface
    戻り値:各キーの入力に応じて回転、反転したSurface
    キー入力の合計値のタプルをキーとして、回転後のSurfaceをバリューとする辞書を作る
    """
    dict = {(-5,0):pg.transform.rotozoom(image,0,1.0),
            (-5,5):pg.transform.rotozoom(image,45,1.0),
            (0,5):pg.transform.flip(pg.transform.rotozoom(image,90,1.0),True,False),
            (5,5):pg.transform.flip(pg.transform.rotozoom(image,45,1.0),True,False),
            (5,0):pg.transform.flip(pg.transform.rotozoom(image,0,1.0),True,False),
            (5,-5):pg.transform.flip(pg.transform.rotozoom(image,-45,1.0),True,False),
            (0,-5):pg.transform.flip(pg.transform.rotozoom(image,-90,1.0),True,False),
            (-5,-5):pg.transform.rotozoom(image,-45,1.0)}
    return dict


def Harder():
    """
    引数:無し
    戻り値:加速度と拡大した爆弾のSurfaceのリストを二つ合わせたタプル
    加速度と拡大したSurfaceをそれぞれリストにしたものをタプルとして合体させてreturnした
    """
    accs = [a for a in range(1,11)]
    bb_imgs = []
    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(225,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return accs, bb_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_dict = Rotate(kk_img)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = 5,5  # 爆弾の横、縦の移動速度
    clock = pg.time.Clock()
    tmr = 0
    bb_accs = Harder()[0]
    bb_imgs = Harder()[1]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾の衝突判定
            return  # gameover
        screen.blit(bg_img, [0, 0]) 

        avx = vx*bb_accs[min(tmr//500,9)]
        bb_img = bb_imgs[min(tmr//500,9)]
    
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,v in KEY_DICT.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)

        if InOut(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        for k, v in kk_dict.items():
            if k == tuple(sum_mv):
                kk_img = v
        screen.blit(kk_img, kk_rct)
        
        bb_rct.move_ip(avx,vy)
        if not InOut(bb_rct)[0]:
            vx = vx * -1
        if not InOut(bb_rct)[1]:
            vy = vy * -1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
