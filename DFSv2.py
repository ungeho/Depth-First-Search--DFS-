#############################
# Depth First Search (DFS)
# Tony Davis
# 27.11.2018
#############################

import turtle                    # import turtle library 標準のグラフィックスライブラリ
import time


wn = turtle.Screen()                      # スクリーンを定義
wn.bgcolor("black")                       # バックグラウンドカラーを黒に設定
wn.title("A Maze Solving Program")
wn.setup(1300,700)                        # 作業ウィンドウの大胃さを設定

# システム変数の宣言
start_x = 0
start_y = 0
end_x = 0
end_y = 0

# 以下の5つのクラスは、迷路を構築する為にturtleを使った画像を描画する。

# 白い壁を用意して、迷路を作成する。
class Maze(turtle.Turtle):               # 迷路（Maze）クラスの定義
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")            # 形を"四角"で定義
        self.color("white")             # 色を"白"で定義
        self.penup()                    # 跡を残さないよう、ペンを持ち上げる
        self.speed(0)                   # アニメーションの速度を"0"で定義

# 緑色のturtleを使用して、訪問したセルを表示する。
class Green(turtle.Turtle):               # 上記のコードとほぼ同じ
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")            # 形を"四角"で定義
        self.color("green")             # 色を"緑"で定義
        self.penup()                    # 跡を残さないよう、ペンを持ち上げる
        self.speed(0)                   # アニメーションの速度を"0"で定義

# 青色のturtleを使用して、迷路で分岐した時の、未開拓なセルを表示する。
class Blue(turtle.Turtle):               # 上記のコードとほぼ同じ
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")            # 形を"四角"で定義
        self.color("blue")              # 色を"青"で定義
        self.penup()                    # 跡を残さないよう、ペンを持ち上げる
        self.speed(0)                   # アニメーションの速度を"0"で定義

# 赤色のturtleを使用して、開始位置を表示する。
class Red(turtle.Turtle):                # 上記のコードとほぼ同じ
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")            # 形を"四角"で定義
        self.color("red")               # 色を"赤"で定義
        self.setheading(270)            # 向きを"↓"で定義
        self.penup()                    # 跡を残さないよう、ペンを持ち上げる
        self.speed(0)                   # アニメーションの速度を"0"で定義

# 黄色のturtleを使用して、ゴールの位置とスタートからゴールまでの計算結果の経路を表示する。
class Yellow(turtle.Turtle):           # 上記のコードとほぼ同じ
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")            # 形を"四角"で定義
        self.color("yellow")            # 色を"黄"で定義
        self.penup()                    # 跡を残さないよう、ペンを持ち上げる
        self.speed(0)                   # アニメーションの速度を"0"で定義

grid4 = [
    "+++++++++++++++",
    "              e",
    "               ",
    "               ",
    "               ",
    "               ",
    "               ",
    "               ",
    "s              ",
    "+++++++++++++++",
]

grid2 = [
"+++++++++++++++",
"+s+       + +e+",
"+ +++++ +++ + +",
"+ + +       + +",
"+ +   +++ + + +",
"+ + + +   + + +",
"+   + + + + + +",
"+++++ + + + + +",
"+     + + +   +",
"+++++++++++++++",
 ]

grid3 = [
"+++++++++",
"+ ++ ++++",
"+ ++ ++++",
"+ ++ ++++",
"+s   ++++",
"++++ ++++",
"++++ ++++",
"+      e+",
"+++++++++",
 ]

grid1 = [
"++++++++++++++++++++++++++++++++++++++++++++++",
"+ s             +                            +",
"+ +++++++++++ +++++++++++++++ ++++++++ +++++ +",
"+           +                 +        +     +",
"++ +++++++ ++++++++++++++ ++++++++++++++++++++",
"++ ++    + ++           + ++                 +",
"++ ++ ++ + ++ ++ +++++ ++ ++ +++++++++++++++ +",
"++ ++ ++ + ++ ++ +     ++ ++ ++ ++        ++ +",
"++ ++ ++++ ++ +++++++++++ ++ ++ +++++ +++ ++ +",
"++ ++   ++ ++             ++          +++ ++e+",
"++ ++++ ++ +++++++++++++++++ +++++++++++++++ +",
"++    + ++                   ++              +",
"+++++ + +++++++++++++++++++++++ ++++++++++++ +",
"++ ++ +                   ++          +++ ++ +",
"++ ++ ++++ ++++++++++++++ ++ +++++ ++ +++ ++ +",
"++ ++ ++   ++     +    ++ ++ ++    ++     ++ +",
"++ ++ ++ +++++++ +++++ ++ ++ +++++++++++++++ +",
"++                     ++ ++ ++              +",
"+++++ ++ + +++++++++++ ++ ++ ++ ++++++++++++++",
"++++++++++++++++++++++++++++++++++++++++++++++",
 ]

# この関数は、上記のグリッドタイプに基づいて迷路を構築する。
def setup_maze(grid):                          # 迷路のセットアップという名前の関数を定義する。
    global start_x, start_y, end_x, end_y      # 開始位置と終了位置のグローバル変数を設定する。
    for y in range(len(grid)):                 # グリッド（格子状,方眼状）の各行を反復処理する。
        for x in range(len(grid[y])):          # 行内の各文字を反復処理する。
            character = grid[y][x]             # 各文字をグリッドのy位置（行）とx位置（列）に割り当てる。
            screen_x = -588 + (x * 24)         # x（列）に対して-588つめて、実際の画面上のxの位置に移動する。
            screen_y = 288 - (y * 24)          # y（行）に対して288つめて、実際の画面上のyの位置に移動する。

            if character == "+":                   # もし、character（文字）が"+"である場合
                # maze（迷路クラス）
                maze.goto(screen_x, screen_y)      # ペンをcharacterのx,y（列,行）の位置に移動し
                maze.stamp()                       # 画面上に白色の四角形の画像を描画する。
                # walls 壁リスト
                walls.append((screen_x, screen_y)) # 該当の座標（x,y）を壁のリストに追加する。

            if character == " ":                    # 文字が見つからない" "（半角スペース）の場合
                # path 経路リスト
                path.append((screen_x, screen_y))   # 該当の座標（x,y）を経路リストに追加する。

            if character == "e":                    # もし、該当の座標の文字が"e"である場合
                # yellow 計算結果の経路とゴール位置のセルのクラス
                yellow.goto(screen_x, screen_y)     # ペンをcharacterのx,y（列,行）の位置に移動し
                yellow.stamp()                      # 画面上に黄色の四角形の画像を描画する。
                end_x, end_y = screen_x, screen_y   # 終了（ゴール）位置（x,y）をend_xとend_yに割り当てる
                # path 経路リスト
                path.append((screen_x, screen_y))   # 経路リストに座標（x,y）を追加

            if character == "s":                       # もし、該当の座標の文字が"s"である場合
                start_x, start_y = screen_x, screen_y  # 開始位置（x,y）をstart_xとstart_yに割り当てる
                # red 開始位置のクラス
                red.goto(screen_x, screen_y)           # 赤色の四角形の画像を開始位置の座標に描画する。

def search(x,y):
    frontier.append((x, y))                            # x,y座標をフロンティアリストに追加
    solution[x, y] = x, y                              # x,y座標をソリューション辞書型に追加
    while len(frontier) > 0:                           # フロンティアリストが空になるまで繰り返す
        time.sleep(0)                                  # アニメーション速度の調整（値を上げると遅くなる）
        current = (x,y)                                # 現在位置情報（x,y座標）を追加


        # 左の座標が経路リスト（path）の中にある かつ 左の座標が探索済みでない（not in visited） 事を確認する
        if(x - 24, y) in path and (x - 24, y) not in visited:  # 左の座標をチェックする（24で1マス、x座標を左:-）
            cellleft = (x - 24, y)     # 左の座標をcellleftに代入
            # solution[左のセルの座標] = 現在（移動前）のx,y座標（backRoute関数で戻る時に、終了位置のx,y座標から移動先が記録される形になる）
            # 下のifの条件がtrueの場合、solutionが上書きされていく為、必ずフロンティアリストの末尾が最終更新になり、逆さに辿ると経路になる。
            solution[cellleft] = x, y
            blue.goto(cellleft)        # 左のセルに分岐先の未開拓（青）を描画する為に左の座標に照準を合わせる
            blue.stamp()               # 左のセルに分岐先の未開拓（青い四角形）を描画する。
            frontier.append(cellleft)  # 分岐先の未開拓の座標リスト（frontier）に追加する。

        if (x, y - 24) in path and (x, y - 24) not in visited:  # 下の座標をチェックする（処理は上記とほぼ同じ）
            celldown = (x, y - 24)
            solution[celldown] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            blue.goto(celldown)
            blue.stamp()
            frontier.append(celldown)

        if(x + 24, y) in path and (x + 24, y) not in visited:   # 右の座標をチェックする（処理は上記とほぼ同じ）
            cellright = (x + 24, y)
            solution[cellright] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            blue.goto(cellright)
            blue.stamp()
            frontier.append(cellright)

        if(x, y + 24) in path and (x, y + 24) not in visited:  # 上の座標をチェックする（処理は上記とほぼ同じ）
            cellup = (x, y + 24)
            solution[cellup] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            blue.goto(cellup)
            blue.stamp()
            frontier.append(cellup)

        x, y = frontier.pop()           # 迷路の分岐先の未開拓の座標リスト（frontier）から最後のエントリ（現在値に一番近い）を削除し、x,y座標に割り当てる
        visited.append(current)         # 現在のx,y座標（frontierリストに移動した後）を訪問済みリストに追加する。
        green.goto(x,y)                 # 訪問済みのセル（緑色の四角形）を描画する為、現在のx,y座標（frontierリストに移動した後）を合わせる。
        green.stamp()                   # 現在のx,y座標（frontierリストに移動した後）に訪問済みのセル（緑色の四角形）を描画する。
        if (x,y) == (end_x, end_y):     # もし、現在のx,y座標が終了位置（黄色の四角形）で描画されるべき場所だった場合
            yellow.stamp()              # 終了位置の色（黄色の四角形）で塗り直す。
        if (x,y) == (start_x, start_y): # もし、現在のx,y座標が開始位置（赤色の四角形）で描画されるべき場所だった場合
            red.stamp()                 # 開始位置の色（赤色の四角形）で塗り直す。

def backRoute(x, y):                       # 探索結果の解を示す関数（終了位置から開始位置へ戻る）
    yellow.goto(x, y)                      # 終了位置に移動し
    yellow.stamp()                         # 黄色の四角形で塗りつぶす
    while (x, y) != (start_x, start_y):    # 現在のx,y座標が開始位置のx,y座標と一致する場合、ループを停止する
        yellow.goto(solution[x, y])        # solutionによって逆方向に辿りながら次のx,y座標を参照し
        yellow.stamp()                     # 黄色い四角で塗りつぶす
        x, y = solution[x, y]              # 辿った先（solution）をx,y座標に入れる

#  初期化リスト
maze = Maze()           #迷路の壁を、白色で描画するクラス
red = Red()             #開始位置を、赤色で描画するクラス
blue = Blue()           #迷路の分岐の未開拓なセルを、青色で描画するクラス
green = Green()         #訪問済みのセルを、緑色で描画するクラス
yellow = Yellow()       #終了位置と、計算結果の経路を黄色で描画するクラス
walls = []              #迷路の壁のリスト
path = []               #迷路の道のリスト
visited = []            #探索済みのセル座標のリスト
frontier = []           #迷路の分岐の未開拓なセルのリスト
solution = {}           #計算結果（辞書型、連想配列に近いもの）

setup_maze(grid1)                       # 迷路のセットアップ関数の呼び出し（迷路を作成し、壁、道、開始位置、終了位置を作成する）
search(start_x, start_y)                # 迷路を探索する為の関数
backRoute(end_x, end_y)                 # 終了位置から開始位置に戻る関数

wn.exitonclick()                        # クリックされた時、描画された画面（Pygame）を終了する。
