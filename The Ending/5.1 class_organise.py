import random



class World(object):
    def __init__(self,world_size=20):
        self.world_size = world_size
        self.grid= [['.' for _ in range(self.world_size)] for _ in range(self.world_size)]
        self.food_position=[]
        self.organism=[]

    def look(self):
        for _ in self.grid:
            print('  '.join(_))

    def set_food(self,i=6):
        for _ in range(i):
            food_x, food_y = random.randint(0, self.world_size - 1), random.randint(0, self.world_size - 1)
            while self.grid[food_y][food_x] != '.':
                food_x, food_y = random.randint(0, self.world_size - 1), random.randint(0, self.world_size - 1)
            self.grid[food_y][food_x] = 'F'
            self.food_position.append((food_x, food_y))
    def set_organisms(self,organism):
        self.organism.append(organism)
    def remove_organisms(self,organism):
        self.organism.remove(organism)
        self.grid[organism.life_y][organism.life_x] = '.'
        print(f'=====玩家 {organism}已死亡++++++')
#prey 猎物

class Organism(object):

    def __init__(self,world):
        n=1
        self.world = world
        self.is_alive = True
        self.energy = 100
        self.vision_range=5
        self.prey=[]
        self.step=0
        self.stop=0
        while True:
            print(f'======{n}+++++++')
            self.life_x,self.life_y=random.randint(0,world.world_size-1),random.randint(0,world.world_size-1)
            n+=1
            if world.grid[self.life_y][self.life_x]=='.':
                world.grid[self.life_y][self.life_x]='0'
                break


    def death(self):
        if self.energy <= 0:
            self.is_alive = False
            self.world.remove_organisms(self)
            return '=======旅途结束++++++++'


    def jud_obstacle(self,new_x,new_y):
        if self.world.grid[new_y][new_x] == '0':
            print('====STOP+++++')
            print(f'======{self.stop}+++++++')
            self.stop += 1
            self.world.look()
        else:
            self.world.grid[self.life_y][self.life_x] = '.'
            self.world.grid[new_y][new_x] = '0'
            self.life_x,self.life_y=new_x,new_y
            print(f'======{self.step}+++++++')
            self.step += 1
            self.world.look()
            self.energy -= 5
            self.death()


    def move(self):

        move_x, move_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        new_x = self.life_x + move_x
        new_y = self.life_y + move_y
        new_x = max(0, min(new_x, self.world.world_size - 1))
        new_y = max(0, min(new_y, self.world.world_size - 1))
        self.jud_obstacle(new_x,new_y)




    def jud(self,x,y):

        if self.world.grid[y][x] == 'F':

            self.prey.append((x, y))


    def search_food(self):

        visible_x=(max(0,self.life_x-self.vision_range),min(self.world.world_size-1,self.life_x+self.vision_range))
        visible_y=(max(0,self.life_y-self.vision_range),min(self.world.world_size-1,self.life_y+self.vision_range))
        print(f'视野x{visible_x}\n'
              f'视野y{visible_y}')
        for y in range(visible_y[0],visible_y[1]+1):
            for x in range(visible_x[0],visible_x[1]+1):
                self.jud(x,y)
        self.prey.sort(key=lambda tur:abs(tur[0]-self.life_x)+abs(tur[1]-self.life_y))
        print(self.prey)
#一步到位，直接到达目的地
#先算步数




    def goal_move(self,goal_x,goal_y):

        for i in range(1000):
            if goal_x!=self.life_x:
                move_x=1 if goal_x>self.life_x else -1
                move_y=0
            elif goal_y!=self.life_y:
                move_x=0
                move_y=1 if goal_y>self.life_y else -1
            else:
                return
            new_x=self.life_x+move_x
            new_y=self.life_y+move_y
            self.jud_obstacle(new_x,new_y)


    def eat(self,x,y):
        if (x,y) in self.prey:
            self.goal_move(x,y)
            self.energy += 30
            print('我吃掉了一个，开心心')
            print(f'{self.world.food_position}')
            print(x,y)
            self.world.food_position.remove((x,y))
            self.prey.remove((x,y))

#1生成生物
#2检测视野范围内是否有食物
#有 规划路线，吃  #无 随机走一步
#多个记住




def main():

    world1=World()
    tjm=Organism(world1)
    world1.set_organisms(tjm)
    world1.set_food()
    for _ in range(100):

        if world1.food_position==[]:
            print('========恭喜恭喜，完成了世界吞噬的任务，原此行终得灵智，赞美新生=========')
            return
        print(f'\n')
        tjm.search_food()
        if tjm.prey:
            for x,y in tjm.prey[:]:
                tjm.eat(x,y)


        else:
            tjm.move()
            print('我随机走了一步')


































if __name__ == '__main__':
    main()






