# ====================
# 自我對弈模組
# ====================

# 匯入套件
from game import State
from pv_mcts import pv_mcts_scores
from dual_network import DN_OUTPUT_SIZE
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
import numpy as np
import pickle
import os

# 設定參數
SP_GAME_COUNT = 500 # 進行自我對弈的遊戲局數（原版為25000）
SP_TEMPERATURE = 1.0 # 波茲曼分布的溫度參數

# 計算先手的局勢價值
def first_player_value(ended_state):
    if ended_state.is_lose():
        return -1 if ended_state.is_first_player() else 1
    return 0

# 儲存訓練資料
def write_data(history):
    now = datetime.now()
    os.makedirs('./data/', exist_ok=True)
    path = './data/{:04}{:02}{:02}{:02}{:02}{:02}.history'.format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    with open(path, mode='wb') as f:
        pickle.dump(history, f)

# 進行 1 次完整對戰
def play(model):

    history = []

    state = State()

    while True:
        if state.is_done():
            break

        scores = pv_mcts_scores(model, state, SP_TEMPERATURE)

        policies = [0] * DN_OUTPUT_SIZE
        for action, policy in zip(state.legal_actions(), scores):
            policies[action] = policy
        history.append([state.pieces_array(), policies, None])

        action = np.random.choice(state.legal_actions(), p=scores)

        state = state.next(action)

    # 在訓練資料中增加價值
    value = first_player_value(state)
    for i in range(len(history)):
        history[i][2] = value
        value = -value
    return history

# 自我對弈
def self_play():
    history = []

    # 載入最佳玩家的模型
    model = load_model('./model/best.h5')

    for i in range(SP_GAME_COUNT):
        h = play(model)
        history.extend(h)

        # 輸出
        print('\rSelfPlay {}/{}'.format(i+1, SP_GAME_COUNT), end='')
    print('')

    # 儲存訓練資料
    write_data(history)

    K.clear_session()
    del model

# 單獨測試
if __name__ == '__main__':
    self_play()
