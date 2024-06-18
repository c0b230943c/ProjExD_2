import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900
KEY_DICT = {pg.K_UP:(0,-5),pg.K_DOWN:(0,5),
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


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    enn = pg.Surface((20,20))
    pg.draw.circle(enn,(255,0,0),(10,10),10)
    enn.set_colorkey((0,0,0))
    bb_rct = enn.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = 5,5  # 爆弾の横、縦の移動速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾の衝突判定
            return  # gameover
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,v in KEY_DICT.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if InOut(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        if not InOut(bb_rct)[0]:
            vx = vx * -1
        if not InOut(bb_rct)[1]:
            vy = vy * -1
        screen.blit(enn,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
