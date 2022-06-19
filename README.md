# AnimalChess_3x4-Alphazero
使用alphazero架構訓練AI遊玩動物將棋
# 大二下python期末專題
組員:蔡旺霖  
專題名稱:以AlphaZero實作賽局遊戲AI 
# 程式碼大略介紹  
## game.py
定義動物將棋遊戲規則，棋盤大小為3*4，有[獅子](https://github.com/Stanley-Lius/AnimalChess_3x4-Alphazero/blob/main/piece4.png)、[小雞](https://github.com/Stanley-Lius/AnimalChess_3x4-Alphazero/blob/main/piece1.png)、[鹿](https://github.com/Stanley-Lius/AnimalChess_3x4-Alphazero/blob/main/piece3.png)和[象](https://github.com/Stanley-Lius/AnimalChess_3x4-Alphazero/blob/main/piece2.png)四種動物  
小雞只能往前走；鹿可以往前後左右四個方向走；象則是可以往對角線方向走  
獅子則是總和以上三種，八個方位都可以走
