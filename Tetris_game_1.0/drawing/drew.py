import pygame
from constant import color_gray, color_gray_block, color_red, color_white, color_gray_green

#繪製矩形
class Box(object):
    #初始化
    def __init__(self, pygame, canvas, name, rect, color):
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.rect = rect
        self.color = color

        self.visible = True
    
    #繪製    
    def update(self):
        if(self.visible):
            self.pygame.draw.rect(self.canvas, self.color, self.rect)

# 其他顯示項目
class Display:
    # 初始化
    def __init__(self, canvas, font):
        self.canvas = canvas
        self.font = font

    # 顯示字
    def showFont(self, text, x, y, color):
        text = self.font.render(text, True, color) 
        self.canvas.blit(text, (x, y))

    # 更新顯示
    def updateGameDisplay(self, game, brick_manager, background, background_brick_next, brick_list):
        brick_manager.updateNextBricks(game.brick_next_id, background_brick_next)
        pos_y = 20
        # 更新背景區塊
        background.update()
        for y in range(20):
            pos_x = 280
            for x in range(10):
                if(game.bricks_array[x][y] != 0):
                    brick_list[y][x].rect[0] = pos_x
                    brick_list[y][x].rect[1] = pos_y
                    brick_list[y][x].update()
                pos_x = pos_x + 28        
            pos_y = pos_y + 28    
        # 更新方塊
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
            # 更新容器
            pos_x = 15
            pos_y = 20
            for y in range(20):
                str_x = ""
                for x in range(10):
                    str_x = str_x + str(game.bricks_array[x][y]) + " "
                self.showFont(str_x, pos_x, pos_y, color_red)
                pos_y = pos_y + 28
            
            # 更新方塊
            posX = 0
            posY = 0    
            for y in range(4):
                str_x = ""
                for x in range(4):            
                    if (brick_manager.bricks[x][y] != 0):
                        posX = game.container_x + x
                        posY = game.container_y + y
                        if (posX >= 0 and posY >= 0):
                            str_x = str_x + str(brick_manager.bricks[x][y]) + " "
                    else:
                        str_x = str_x + "  "
                pos_x = 15 + (game.container_x * 26)
                pos_y = 20 + (posY * 28)
                self.showFont(str_x, pos_x, pos_y, color_white)

    # 顯示訊息
    def displayGameInfo(self, game, clock):
        self.showFont("Next", 588, 16, color_gray)

        self.showFont("Max", 588, 190, color_gray)
        self.showFont(str(int(game.lines_number_max)), 588, 220, color_gray)

        self.showFont("Cumulate", 588, 260, color_gray)
        self.showFont(str(int(game.lines_number)), 588, 290, color_gray)

        self.showFont("Level", 588, 330, color_gray)
        self.showFont(str(int(game.game_level)), 588, 360, color_gray)

        # 在除錯訊息顯示FPS
        if(game.debug_message):    
            self.showFont("FPS:" + str(clock.get_fps()), 6, 0, color_gray_green) 