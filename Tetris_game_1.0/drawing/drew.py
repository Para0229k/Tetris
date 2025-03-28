import pygame
from constant import color_gray, color_gray_block, color_red, color_white, color_gray_green

# 繪製矩形
class Box(object):
    # 初始化
    def __init__(self, pygame, canvas, name, rect, color):
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.rect = rect
        self.color = color
        self.visible = True
    
    # 繪製    
    def update(self):
        if(self.visible):
            self.pygame.draw.rect(self.canvas, self.color, self.rect)

# 顯示項目
class Display:
    # 初始化
    def __init__(self, canvas, font):
        self.canvas = canvas
        self.font = font

    # 顯示字
    def showFont(self, text, x, y, color):
        text = self.font.render(text, True, color) 
        self.canvas.blit(text, (x, y))

    # 更新顯示器
    def updateGameDisplay(self, game, brick_manager, background, background_brick_next, background_brick_hold, brick_list):
        # 更新背景區域
        brick_manager.updateNextBricks(game.brick_next_id, background_brick_next)
        brick_manager.updateHoldBricks(game.hold_id, background_brick_hold)
        pos_y = 20
        background.update()
        
        # 方塊陣列(10x20)
        for y in range(20):
            pos_x = 280
            for x in range(10):
                if(game.bricks_array[x][y] != 0):
                    brick_list[y][x].rect[0] = pos_x
                    brick_list[y][x].rect[1] = pos_y
                    brick_list[y][x].update()
                pos_x = pos_x + 28        
            pos_y = pos_y + 28

        # 方塊陣列(4x4)
        for y in range(4):
            for x in range(4):            
                if (brick_manager.bricks[x][y] != 0):
                    posX = game.container_x + x
                    posY = game.container_y + y
                    if (posX >= 0 and posY >= 0 and posY < 20 and posX < 10):
                        brick_list[posY][posX].rect[0] = (posX * 28) + 280
                        brick_list[posY][posX].rect[1] = (posY * 28) + 20
                        brick_list[posY][posX].update()
  
    # 除錯訊息
    def displayDebugInfo(self, game, brick_manager):
        if(game.debug_message):
            pos_x = 15
            pos_y = 20
            num_width = 12
            
            # 顯示紅字
            for y in range(20):
                for x in range(10):
                    num_x = pos_x + (x * num_width)
                    num_y = pos_y + (y * 28)
                    self.showFont(str(game.bricks_array[x][y]), num_x, num_y, color_red)
            
            # 顯示白字（移動中的方塊）
            for y in range(4):
                for x in range(4):
                    if brick_manager.bricks[x][y] != 0:
                        posX = game.container_x + x
                        posY = game.container_y + y

                        # 確保位置在遊戲區域內
                        if posX >= 0 and posY >= 0 and posY < 20 and posX < 10:
                            text_x = pos_x + (posX * num_width)
                            text_y = pos_y + (posY * 28)
                            self.showFont(str(brick_manager.bricks[x][y]), text_x, text_y, color_white)

    # 顯示訊息
    def displayGameInfo(self, game, clock):
        self.showFont("Next", 588, 16, color_gray)

        self.showFont("Max", 588, 190, color_gray)
        self.showFont(str(int(game.lines_number_max)), 588, 220, color_gray)
        
        self.showFont("Cumulate", 588, 260, color_gray)
        self.showFont(str(int(game.lines_number)), 588, 290, color_gray)

        self.showFont("Score", 588, 330, color_gray)
        show_text = f"{game.score:,}"
        self.showFont(show_text, 588, 360, color_gray)

        self.showFont("Hold", 588, 400, color_gray)

        self.showFont("Level", 200, 535, color_gray)
        self.showFont(str(int(game.game_level)), 255, 535, color_gray)

        # 在除錯訊息顯示FPS
        if(game.debug_message):    
            self.showFont("FPS:" + str(clock.get_fps()), 6, 0, color_gray_green) 
    
    # 遊戲說明
    def displayInstruction(self, page=1):
        # 背景
        pygame.draw.rect(self.canvas, color_gray, [100, 50, 600, 500])
        
        # 標題
        title_text = self.font.render("Tetris Game Instruction", True, color_white)
        title_width = title_text.get_width()
        self.canvas.blit(title_text, (400 - title_width // 2, 80))

        # 頁碼
        page_text = self.font.render(f"Page {page}/2", True, color_white)
        self.canvas.blit(page_text, (600, 70))

        # 分隔線
        pygame.draw.line(self.canvas, color_white, [150, 120], [650, 120], 2)

        line_height = 30
        y_pos = 150

        # pg.1 遊戲系統&顯示說明
        if page == 1:
            # 遊戲系統說明
            left_x = 150
            left_y = 150
            
            self.showFont("Game System", left_x, left_y, color_white)
            left_y += 40
    
            self.showFont("- Level increases every", left_x, left_y, color_white)
            left_y += 25
            self.showFont("  10,000 points", left_x, left_y, color_white)
            left_y += 35
    
            self.showFont("- Each level increases", left_x, left_y, color_white)
            left_y += 25
            self.showFont("  falling speed", left_x, left_y, color_white)
            left_y += 35
    
            self.showFont("- Score by lines cleared:", left_x, left_y, color_white)
            left_y += 30
        
            self.showFont("  Single: 1,000 points", left_x, left_y, color_white)
            left_y += 25
        
            self.showFont("  Double: 3,000 points", left_x, left_y, color_white)
            left_y += 25
        
            self.showFont("  Triple: 5,000 points", left_x, left_y, color_white)
            left_y += 25
        
            self.showFont("  Tetris: 8,000 points", left_x, left_y, color_white)

            # 顯示說明
            right_x = 400
            right_y = 150
            
            self.showFont("Display Information", right_x, right_y, color_white)
            right_y += 40
    
            self.showFont("- Next:", right_x, right_y, color_white)
            right_y += 25
            self.showFont("  Preview of next tetromino", right_x, right_y, color_white)
            right_y += 35
        
            self.showFont("- Max:", right_x, right_y, color_white)
            right_y += 25
            self.showFont("  Maximum lines cleared", right_x, right_y, color_white)
            right_y += 35
        
            self.showFont("- Cumulate:", right_x, right_y, color_white)
            right_y += 25
            self.showFont("  Total lines cleared", right_x, right_y, color_white)
            right_y += 35
        
            self.showFont("- Score:", right_x, right_y, color_white)
            right_y += 25
            self.showFont("  Your current score", right_x, right_y, color_white)
            right_y += 35
        
            self.showFont("- Hold:", right_x, right_y, color_white)
            right_y += 25
            self.showFont("  Reserved tetromino", right_x, right_y, color_white)
            right_y += 35

            self.showFont("- Level:", right_x, right_y, color_white)
            right_y += 25
            self.showFont("  Current game level", right_x, right_y, color_white)
        
            prompt_text = self.font.render("Press any key to continue", True, color_white)
            text_width = prompt_text.get_width()
            self.canvas.blit(prompt_text, (250 - text_width // 2, 520))
        # pg.2 操作方式說明
        elif page == 2:
            center_x = 400
            y_pos = 100
            
            title_text = self.font.render("Controls", True, color_white)
            title_width = title_text.get_width()
            self.canvas.blit(title_text, (center_x - title_width // 2, y_pos))
            y_pos += 50
        
            control_bg = pygame.Rect(170, y_pos, 460, 45)
            pygame.draw.rect(self.canvas, color_gray_block, control_bg)
            self.showFont("Left / Right", 200, y_pos + 12, color_white)
            self.showFont("Move horizontally", 380, y_pos + 12, color_white)
            y_pos += 60
        
            control_bg = pygame.Rect(170, y_pos, 460, 45)
            pygame.draw.rect(self.canvas, color_gray_block, control_bg)
            self.showFont("Up", 200, y_pos + 12, color_white)
            self.showFont("Rotate", 380, y_pos + 12, color_white)
            y_pos += 60
        
            control_bg = pygame.Rect(170, y_pos, 460, 45)
            pygame.draw.rect(self.canvas, color_gray_block, control_bg)
            self.showFont("Down", 200, y_pos + 12, color_white)
            self.showFont("Speed up falling", 380, y_pos + 12, color_white)
            y_pos += 60
        
            control_bg = pygame.Rect(170, y_pos, 460, 45)
            pygame.draw.rect(self.canvas, color_gray_block, control_bg)
            self.showFont("Space", 200, y_pos + 12, color_white)
            self.showFont("Hold the current tetromino", 380, y_pos + 12, color_white)
            y_pos += 60
        
            control_bg = pygame.Rect(170, y_pos, 460, 45)
            pygame.draw.rect(self.canvas, color_gray_block, control_bg)
            self.showFont("D", 200, y_pos + 12, color_white)
            self.showFont("Show debug information", 380, y_pos + 12, color_white)
            y_pos += 60
        
            control_bg = pygame.Rect(170, y_pos, 460, 45)
            pygame.draw.rect(self.canvas, color_gray_block, control_bg)
            self.showFont("ESC", 200, y_pos + 12, color_white)
            self.showFont("Quit the game", 380, y_pos + 12, color_white)
        
            prompt_text = self.font.render("Press any key to start game", True, color_white)
            text_width = prompt_text.get_width()
            self.canvas.blit(prompt_text, (400 - text_width // 2, 520))

    # 結算畫面
    def displayGameOver(self, game):
        # 背景
        pygame.draw.rect(self.canvas, color_gray, [100, 100, 600, 400])
        
        # 標題
        title_text = self.font.render("Game Over", True, color_white)
        title_width = title_text.get_width()
        self.canvas.blit(title_text, (400 - title_width // 2, 130))

        # 分隔線
        pygame.draw.line(self.canvas, color_white, [150, 170], [650, 170], 2)

        # 結算訊息
        stats_y = 210
        stats_x = 300

        self.showFont("Level:", stats_x, stats_y, color_white)
        self.showFont(str(int(game.game_level)), stats_x + 200, stats_y, color_white)
        stats_y += 40

        self.showFont("Score:", stats_x, stats_y, color_white)
        show_text = f"{game.score:,}"
        self.showFont(show_text, stats_x + 200, stats_y, color_white)
        stats_y += 40

        self.showFont("Cumulate Lines:", stats_x, stats_y, color_white)
        self.showFont(str(int(game.lines_number)), stats_x + 200, stats_y, color_white)
        stats_y += 40

        self.showFont("Max Lines:", stats_x, stats_y, color_white)
        self.showFont(str(int(game.lines_number_max)), stats_x + 200, stats_y, color_white)
        stats_y += 70

        # 結算提示
        control_bg = pygame.Rect(200, stats_y, 400, 45)
        pygame.draw.rect(self.canvas, color_gray_block, control_bg)
        control_text = self.font.render("Press R to restart", True, color_white)
        self.canvas.blit(control_text, (400 - control_text.get_width() // 2, stats_y + 12))
        
        stats_y += 50
        control_bg = pygame.Rect(200, stats_y, 400, 45)
        pygame.draw.rect(self.canvas, color_gray_block, control_bg)
        control_text = self.font.render("Press ESC to quit", True, color_white)
        self.canvas.blit(control_text, (400 - control_text.get_width() // 2, stats_y + 12))
