# ====================
# 人類與 AI 的對戰
# ====================

# 匯入套件
from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk
from PIL import Image, ImageTk

# 載入最佳玩家模型
model = load_model('./model/best.h5')

# 初始化GameUI
class GameUI(tk.Frame):
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title('動物棋')

        self.state = State()
        self.select = -1 # 選擇游標（－1：無、0～11：格子、12～14：持駒）

        # 方向常數
        self.dxy = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))

        self.next_action = pv_mcts_action(model, 0.0)

        # 準備圖片作為動物棋
        self.images = [(None, None, None, None)]
        for i in range(1, 5):
            image = Image.open('piece{}.png'.format(i))
            self.images.append((
                ImageTk.PhotoImage(image),
                ImageTk.PhotoImage(image.rotate(180)),
                ImageTk.PhotoImage(image.resize((40, 40))),
                ImageTk.PhotoImage(image.resize((40, 40)).rotate(180))))

        # 產生新的畫布元件
        self.c = tk.Canvas(self, width = 240, height = 400, highlightthickness = 0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        # 更新盤面的UI
        self.on_draw()

    # 輪到人類下棋
    def turn_of_human(self, event):
        # Step01 判斷遊戲是否結束
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return

        # Step02 判斷是否輪到人類下棋
        if not self.state.is_first_player():
            return

        # Step03 利用 state.pieces 取得持駒的種類
        captures = []
        for i in range(3):
            if self.state.pieces[12+i] >= 2: captures.append(1+i)
            if self.state.pieces[12+i] >= 1: captures.append(1+i)

        # Step04 計算選擇的棋子與移動的位置
        p = int(event.x/80) + int((event.y-40)/80) * 3
        if 40 <= event.y and event.y <= 360:
            select = p
        elif event.x < len(captures) * 40 and event.y > 360:
            select = 12 + int(event.x/40)
        else:
            return

        # 選擇棋子 (select < 0 才要做的處理)
        if self.select < 0:
            self.select = select
            self.on_draw()
            return

        # Step05 將選擇的棋子與移動的位置轉換成動作
        action = -1
        if select < 12:
            # 移動棋子時
            if self.select < 12:
                action = self.state.position_to_action(p, self.position_to_direction(self.select, p))
            # 放回持駒時
            else:
                action = self.state.position_to_action(p, 8-1+captures[self.select-12])

        # Step06 當下棋非合法棋步時
        if not (action in self.state.legal_actions()):
            self.select = -1
            self.on_draw()
            return

        # Step07 取得下一個局勢 (盤面)
        self.state = self.state.next(action)
        self.select = -1
        self.on_draw()

        # Step08 轉由 AI 進行下棋 (編註：攻守交換)
        self.master.after(1, self.turn_of_ai)

    # 輪到 AI 下棋
    def turn_of_ai(self):
        # Step01 判斷遊戲是否結束
        if self.state.is_done():
            return

        # Step02 取得動作
        action = self.next_action(self.state)

        # Step03 取得下一個局勢 (盤面)
        self.state = self.state.next(action)
        self.on_draw()

    # 計算並傳回棋子移動方向
    def position_to_direction(self, position_src, position_dst):
        dx = position_dst%3-position_src%3
        dy = int(position_dst/3)-int(position_src/3)
        for i in range(8):
            if self.dxy[i][0] == dx and self.dxy[i][1] == dy: return i
        return 0

    # 繪製棋子
    def draw_piece(self, index, first_player, piece_type):
        x = (index%3)*80
        y = int(index/3)*80+40
        index = 0 if first_player else 1
        self.c.create_image(x, y, image=self.images[piece_type][index],  anchor=tk.NW)

    # 繪製持駒
    def draw_capture(self, first_player, pieces):
        index, x, dx, y = (2, 0, 40, 360) if first_player else (3, 200, -40, 0)
        captures = []
        for i in range(3):
            if pieces[12+i] >= 2: captures.append(1+i)
            if pieces[12+i] >= 1: captures.append(1+i)
        for i in range(len(captures)):
            self.c.create_image(x+dx*i, y, image=self.images[captures[i]][index],  anchor=tk.NW)

    # 繪製游標
    def draw_cursor(self, x, y, size):
        self.c.create_line(x+1, y+1, x+size-1, y+1, width = 4.0, fill = '#FF0000')
        self.c.create_line(x+1, y+size-1, x+size-1, y+size-1, width = 4.0, fill = '#FF0000')
        self.c.create_line(x+1, y+1, x+1, y+size-1, width = 4.0, fill = '#FF0000')
        self.c.create_line(x+size-1, y+1, x+size-1, y+size-1, width = 4.0, fill = '#FF0000')

    # 更新盤面的 UI
    def on_draw(self):
        # 繪製棋盤
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 240, 400, width = 0.0, fill = '#EDAA56')
        for i in range(1,3):
            self.c.create_line(i*80+1, 40, i*80, 360, width = 2.0, fill = '#000000')
        for i in range(5):
            self.c.create_line(0, 40+i*80, 240, 40+i*80,  width = 2.0, fill = '#000000')

        # 棋子
        for p in range(12):
            p0, p1 = (p, 11-p) if self.state.is_first_player() else (11-p, p)
            if self.state.pieces[p0] != 0:
                self.draw_piece(p, self.state.is_first_player(), self.state.pieces[p0])
            if self.state.enemy_pieces[p1] != 0:
                self.draw_piece(p, not self.state.is_first_player(), self.state.enemy_pieces[p1])

        # 持駒
        self.draw_capture(self.state.is_first_player(), self.state.pieces)
        self.draw_capture(not self.state.is_first_player(), self.state.enemy_pieces)

        # 游標
        if 0 <= self.select and self.select < 12:
            self.draw_cursor(int(self.select%3)*80, int(self.select/3)*80+40, 80)
        elif 12 <= self.select:
            self.draw_cursor((self.select-12)*40, 360, 40)

# 顯示視窗
f = GameUI(model = model)
f.pack()
f.mainloop()