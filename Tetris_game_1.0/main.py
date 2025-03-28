import os, sys, random
import time
import pygame 
from pygame.locals import *
from drawing.drew import Box, Display
from constant import *
from tetromino.tetromino import BrickManager
from game.game import Game

def main():
    pygame.init()
    pygame.display.set_caption("俄羅斯方塊遊戲")

    # 全螢幕模式
    # canvas = pygame.display.set_mode((canvas_width, canvas_height), pygame.DOUBLEBUF and pygame.FULLSCREEN )
    
    # 視窗模式
    canvas = pygame.display.set_mode((canvas_width, canvas_height))

    # 設定
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("simsunnsimsun", 24)
    brick_manager = BrickManager()
    game = Game(brick_manager)
    display = Display(canvas, font)

    # 把方塊放入陣列(20x10)
    bricks_list = []
    for y in range(20):
        row = []
        for x in range(10):
            row.append(Box(pygame, canvas, "brick_x_" + str(x) + "_y_" + str(y), [ 0, 0, 26, 26], color_gray_block))
        bricks_list.append(row)
    
    # 把Next方塊放入陣列(4x4)
    for y in range(4):
        for x in range(4):
            brick_manager.bricks_next_object[x][y] = Box(pygame, canvas, "brick_next_x_" + str(x) + "_y_" + str(y), [0, 0, 26, 26], color_gray_block)

    # 把Hold方塊放入陣列(4x4)
    for y in range(4):
        for x in range(4):
            brick_manager.bricks_hold_object[x][y] = Box(pygame, canvas, "brick_hold_x" + str(x) + "_y_" + str(y), [0, 0, 26, 26], color_gray_block)

    # 背景
    background = Box(pygame, canvas, "background", [278, 18, 282, 562], color_gray)
    background_bricks_next = Box(pygame, canvas, "background_bricks_next", [590, 50, 114, 114], color_gray)
    background_bricks_hold = Box(pygame, canvas, "background_bricks_hold", [590, 434, 114, 114], color_gray)

    # 隨機產生新方塊
    game.brick_next_id = random.randint( 1, 7)   
    game.brickNew()

    running = True
    time_temp = time.time()
    time_now = 0

    game.instructions_mode = True
    game.instruction_page = 1

    while running:
        # 計算時脈
        time_now = time_now + (time.time() - time_temp)
        time_temp = time.time()

        # 事件判斷
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                continue
            
            if game.instructions_mode:
                # 說明介面
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        # 顯示第二頁或開始遊戲
                        if game.instruction_page == 1:
                            game.instruction_page = 2
                        else:
                            game.instructions_mode = False
            elif game.game_over_screen:
                # 結算畫面
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        game.restartGame()
                        brick_manager.transformToBricks(game.brick_id, game.brick_state)

            else:     
                # 按下按鍵
                if event.type == pygame.KEYDOWN:
                    # esc - 退出
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # D - 除錯訊息
                    elif event.key == pygame.K_d:
                        game.debug_message = not game.debug_message
                    # 空白鍵 - Hold
                    elif event.key == pygame.K_SPACE and game.game_mode == 0 and game.can_hold:
                        game.holdBrick()
                        brick_manager.transformToBricks(game.brick_id, game.brick_state)    
                    # 上 - 旋轉
                    elif event.key == pygame.K_UP and game.game_mode == 0:
                        # 保存當前狀態
                        original_state = game.brick_state
                        original_x = game.container_x
                    
                        # 討論不同情形
                        # 在邊界
                        if (game.container_x == 8 and game.brick_id == 6):
                            continue
                        # S、Z
                        if game.brick_id == 1 or game.brick_id == 2:
                            new_state = (game.brick_state + 1) % 2
                        # I
                        elif game.brick_id == 7:
                            if game.container_x < 0 or game.container_x == 7:
                                continue
                            new_state = (game.brick_state + 1) % 2                         
                        # J、L、T     
                        elif (game.brick_id == 3 or game.brick_id == 4 or game.brick_id == 5):
                            new_state = (game.brick_state + 1) % 4
                        # O
                        else:
                            continue

                        # 更新狀態
                        game.brick_state = new_state
                        brick_manager.transformToBricks(game.brick_id, game.brick_state)
                    
                        # wall kick
                        kick_offsets = [0, -1, 1, -2, 2]
                        rotation_success = False
                        for offset_x in kick_offsets:
                            test_x = original_x + offset_x

                            if brick_manager.ifCopyToBricksArray(test_x, game.container_y, game.bricks_array):
                                game.container_x = test_x
                                rotation_success = True
                                break
                    
                        # 不能旋轉就復原狀態
                        if not rotation_success:
                            game.container_x = original_x
                            game.brick_state = original_state
                            brick_manager.transformToBricks(game.brick_id, game.brick_state)

                    # 下 - 加速
                    elif event.key == pygame.K_DOWN and game.game_mode == 0:
                        game.brick_down_speed = brick_drop_rapidly
                    # 左 - 移動
                    elif event.key == pygame.K_LEFT and game.game_mode == 0:
                        game.container_x = game.container_x - 1
                        if (game.container_x < 0):
                            if (game.container_x == -1):
                                if (brick_manager.bricks[0][0] != 0 or brick_manager.bricks[0][1] != 0 or brick_manager.bricks[0][2] != 0 or brick_manager.bricks[0][3] != 0):
                                    game.container_x = game.container_x + 1
                            elif (game.container_x == -2): 
                                if (brick_manager.bricks[1][0] != 0 or brick_manager.bricks[1][1] != 0 or brick_manager.bricks[1][2] != 0 or brick_manager.bricks[1][3] != 0):
                                    game.container_x = game.container_x + 1
                            else:
                                game.container_x = game.container_x + 1
                        # 碰到方塊
                        if (not brick_manager.ifCopyToBricksArray(game.container_x, game.container_y, game.bricks_array)):
                            game.container_x = game.container_x + 1
                    # 右 - 移動
                    elif event.key == pygame.K_RIGHT and game.game_mode == 0:
                        game.container_x = game.container_x + 1
                        if (game.container_x > 6):
                            if (game.container_x == 7):
                                if (brick_manager.bricks[3][0] != 0 or brick_manager.bricks[3][1] != 0 or brick_manager.bricks[3][2] != 0 or brick_manager.bricks[3][3] != 0):
                                    game.container_x = game.container_x - 1;                        
                            elif (game.container_x == 8):
                                if (brick_manager.bricks[2][0] != 0 or brick_manager.bricks[2][1] != 0 or brick_manager.bricks[2][2] != 0 or brick_manager.bricks[2][3] != 0):
                                    game.container_x = game.container_x - 1                        
                            else:
                                game.container_x = game.container_x - 1
                        # 碰到方塊
                        if (not brick_manager.ifCopyToBricksArray(game.container_x, game.container_y, game.bricks_array)):
                            game.container_x = game.container_x - 1                    
                # 放開按鍵
                if event.type == pygame.KEYUP:
                    # 放開下 - 恢復正常速度 
                    if event.key == pygame.K_DOWN:
                        game.brick_down_speed = brick_down_speed_max
        
        canvas.fill(color_block)

        # 說明介面
        if game.instructions_mode:
            display.displayInstruction(game.instruction_page)
            pygame.display.update()
            clock.tick(60)
            continue

        # 結算畫面
        if game.game_over_screen:
            display.displayGameOver(game)
            pygame.display.update()
            clock.tick(60)
            continue

        # 遊戲進行中
        if (game.game_mode == 0):
            # 方塊下降
            if(time_now >= game.brick_down_speed):
                game.container_y = game.container_y + 1; 
                
                # 碰到方塊就產生下一個
                if (not brick_manager.ifCopyToBricksArray(game.container_x, game.container_y, game.bricks_array)):
                    game.brickNew()            
                brick_manager.transformToBricks(game.brick_id, game.brick_state)
                time_now = 0
        # 消除方塊
        elif (game.game_mode == 1):
            game.clearBrick()
            # 回到遊戲
            game.game_mode = 0
            brick_manager.transformToBricks(game.brick_id, game.brick_state)

        # 更新顯示內容
        display.updateGameDisplay(game, brick_manager, background, background_bricks_next, background_bricks_hold, bricks_list)
        display.displayDebugInfo(game, brick_manager)
        display.displayGameInfo(game, clock)
        pygame.display.update()
        clock.tick(60)

    # 離開遊戲
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
