# AnimalChess_3x4-Alphazero
使用alphazero架構訓練AI遊玩動物將棋
# 大二下python期末專題
## 組員:  
蔡旺霖  
## 專題名稱:  
以AlphaZero實作賽局遊戲AI
## 參考書籍  
[這裡](https://www.tenlong.com.tw/products/9789863126515)
# AlphaZero主要理念  
AlphaZero主要是由深度學習、加強式學習以及賽局數演算法組合而成  
## 深度學習  
用來預測最佳棋步的直覺，簡單來說就是以***訓練集***(以前的資料)來預測下一步該如何走  
## 強化式學習  
藉由自我對弈以及蒙地卡羅搜尋樹來獲得回饋值，使代理人能藉由回饋值計算出沒一步棋路的***價值***，從而做出最好的選擇  
## 賽局樹演算法  
預知能力，相較於深度演算法是以當前的棋勢來去局部推演出接下來所可能走的棋步(預測所有可能的未來)，然後把其中最有可能導致獲勝的棋步選擇出來  
# 程式碼大略介紹  
## game.py
定義動物將棋遊戲規則，棋盤大小為3*4，有[獅子](https://github.com/Stanley-Lius/AnimalChess_3x4-Alphazero/blob/main/piece4.png)、[小雞](https://github.com/Stanley-Lius/AnimalChess_3x4-Alphazero/blob/main/piece1.png)、[鹿](https://github.com/Stanley-Lius/AnimalChess_3x4-Alphazero/blob/main/piece3.png)和[象](https://github.com/Stanley-Lius/AnimalChess_3x4-Alphazero/blob/main/piece2.png)四種動物所組成  
小雞只能往前走；鹿可以往前後左右四個方向走；象則是可以往對角線方向走  
獅子則是總和以上三種，八個方位都可以走，如同超連結中途圖片紅點所示  
遊戲中有持駒規則，亦即如果我們吃掉了對方的棋子，在下個我方回合可以把它放到棋盤任意空格子，且會變為我方棋子  
遊戲***勝利條件***是將對手的獅子吃掉，或者下超過三百回合即算平手  
***此程式***主要是用來回傳現在的局勢以及可以下的棋子、可以下的點，還有判斷獅子是否被吃掉的終局條件  
## dual_network.py  
定義了對偶網路的架構，由一個捲基層、16個殘差塊以及一個池化層所組成；輸出有兩個，分別是***策略輸出***(策略，這裡是每個棋盤格子可以被下的機率所組合而成的陣列，陣列合為1)，  以及***價值輸出***(局勢價值，代表了用來預測當前盤面所會導致的勝負)  

