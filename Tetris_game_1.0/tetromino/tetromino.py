from constant import brick_dict
from drawing.drew import *

class BrickManager:
    # 初始化方塊
    def __init__(self):
        self.bricks = []
        for i in range(4):
            self.bricks.append([0]*4)
        
        self.bricks_next = []
        for i in range(4):
            self.bricks_next.append([0]*4)
        
        self.bricks_next_object = []
        for i in range(4):
            self.bricks_next_object.append([0]*4)

        self.bricks_hold = []
        for i in range(4):
            self.bricks_hold.append([0]*4)

        self.bricks_hold_object = []
        for i in range(4):
            self.bricks_hold_object.append([0]*4)

    # 取得方塊的index
    def getBrickIndex(self, brickId, state):
        brickKey = str(brickId)+str(state)
        return brick_dict[brickKey]

    # 將index轉換成方塊
    def transformToBricks(self, brickId, state):
        for x in range(4):
            for y in range(4):
                self.bricks[x][y] = 0
        p_brick = self.getBrickIndex(brickId, state)
    
        # 轉換
        for i in range(4):        
            bx = int(p_brick[i] % 4)
            by = int(p_brick[i] / 4)
            self.bricks[bx][by] = brickId

    # 判斷方塊可否複製到容器中
    def ifCopyToBricksArray(self, container_x, container_y, bricks_array):
        for x in range(4):
            for y in range(4):
               if (self.bricks[x][y] != 0):
                    posX = container_x + x
                    posY = container_y + y
                    if (posX >= 0 and posY >= 0):
                        try:
                            if (bricks_array[posX][posY] != 0):
                                return False
                        except:
                            return False
        return True

    # 複製方塊
    def copyToBricksArray(self, container_x, container_y, bricks_array):
        for x in range(4):
            for y in range(4):
                if (self.bricks[x][y] != 0):
                    posX = container_x + x
                    posY = container_y + y
                    if (posX >= 0 and posY >= 0):
                        bricks_array[posX][posY] = self.bricks[x][y]

    # 下一個方塊
    def updateNextBricks(self, brickId, background_bricks_next):
        for y in range(4):
            for x in range(4):
                self.bricks_next[x][y] = 0

        # 生成下一個方塊
        pBrick = self.getBrickIndex(brickId, 0)
        for i in range(4):
            bx = int(pBrick[i] % 4)
            by = int(pBrick[i] / 4)
            self.bricks_next[bx][by] = brickId

        # 更新背景和方塊
        background_bricks_next.update()
        pos_y = 52
        for y in range(4):
            pos_x = 592
            for x in range(4):
                if(self.bricks_next[x][y] != 0):
                    if brickId == 1:
                        self.bricks_next_object[x][y].color = color_brick_S
                    elif brickId == 2:
                        self.bricks_next_object[x][y].color = color_brick_Z
                    elif brickId == 3:
                        self.bricks_next_object[x][y].color = color_brick_J
                    elif brickId == 4:
                        self.bricks_next_object[x][y].color = color_brick_L
                    elif brickId == 5:
                        self.bricks_next_object[x][y].color = color_brick_T
                    elif brickId == 6:
                        self.bricks_next_object[x][y].color = color_brick_O
                    elif brickId == 7:
                        self.bricks_next_object[x][y].color = color_brick_I
                    
                    self.bricks_next_object[x][y].rect[0] = pos_x
                    self.bricks_next_object[x][y].rect[1] = pos_y
                    self.bricks_next_object[x][y].update()
                pos_x = pos_x + 28        
            pos_y = pos_y + 28
    
    # Hold的方塊
    def updateHoldBricks(self, hold_id, background_hold):
        for y in range(4):
            for x in range(4):
                self.bricks_hold[x][y] = 0
        
        # 生成Hold的方塊
        if hold_id > 0:
            pBrick = self.getBrickIndex(hold_id, 0)
            for i in range(4):
                bx = int(pBrick[i] % 4)
                by = int(pBrick[i] / 4)
                self.bricks_hold[bx][by] = hold_id
        
        # 更新背景、方塊
        background_hold.update()
        pos_y = 430
        for y in range(4):
            pos_x = 592
            for x in range(4):
                if(self.bricks_hold[x][y] != 0):
                    if hold_id == 1:
                        self.bricks_next_object[x][y].color = color_brick_S
                    elif hold_id == 2:
                        self.bricks_next_object[x][y].color = color_brick_Z
                    elif hold_id == 3:
                        self.bricks_next_object[x][y].color = color_brick_J
                    elif hold_id == 4:
                        self.bricks_next_object[x][y].color = color_brick_L
                    elif hold_id == 5:
                        self.bricks_next_object[x][y].color = color_brick_T
                    elif hold_id == 6:
                        self.bricks_next_object[x][y].color = color_brick_O
                    elif hold_id == 7:
                        self.bricks_next_object[x][y].color = color_brick_I

                    self.bricks_hold_object[x][y].rect[0] = pos_x
                    self.bricks_hold_object[x][y].rect[1] = pos_y
                    self.bricks_hold_object[x][y].update()
                pos_x = pos_x + 28        
            pos_y = pos_y + 28
