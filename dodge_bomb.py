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
    

def GameOver(screen:pg.Surface):
    """
    引数:Surface(screen)
    戻り値:なし
    画面をブラックアウトさせ
    泣いているこうかとんとGameOverの文字列を五秒間表示する
    """
    black = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(black,(0,0,0),(0,0,WIDTH,HEIGHT))
    black.set_alpha(75)
    screen.blit(black,[0,0])
    cry_k = pg.image.load("fig/8.png")
    screen.blit(cry_k,[600,HEIGHT//2])
    screen.blit(cry_k,[1050,HEIGHT//2])
    font = pg.font.Font(None,80)
    txt = font.render("Game Over",True,(255,255,255))
    screen.blit(txt,[700,HEIGHT//2])
    pg.display.update()
    time.sleep(5)
    

def Follow(kk_rct:pg.Rect,bb_rct:pg.Rect):
    """
    引数:こうかとんの座標,爆弾の座標
    戻り値:爆弾の移動すべき方向のベクトル
    こうかとんに向かって追従するように動くベクトルを返す
    ただし、こうかとんとの距離が300未満であった場合、追従せず慣性方向に進むベクトルを返す
    """
    x_dif = kk_rct.center[0] - bb_rct.center[0]
    y_dif = kk_rct.center[1] - bb_rct.center[1]
    norm = x_dif**2 + y_dif**2
    if norm < 300:
        return bb_rct  # 未完成
    else:
        norm_x_dif = x_dif * 50 / norm
        norm_y_dif = y_dif * 50 / norm
    return norm_x_dif,norm_y_dif


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
            GameOver(screen)
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
                kk_img = v  # sum_mvの値に応じて回転、反転させた画像をkk_imgに上書き
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
