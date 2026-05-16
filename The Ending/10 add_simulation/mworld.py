import random
import pandas as pd
from Config import WorldConfig,OrganismConfig
from events import EventBus
import mypy


class World(object):
    def __init__(self,config : WorldConfig=WorldConfig()):
        self.config = config
        self.world_size = config.size
        self.grid= [['.' for _ in range(self.world_size)] for _ in range(self.world_size)]
        self.food_position=[]

    def look(self) -> None:
        for _ in self.grid:
            print('  '.join(_))


    #随机找一个空的位置
    def _random_empty_cell(self) -> tuple[int,int]:
        while True:
            x=random.randint(0,self.world_size-1)
            y=random.randint(0,self.world_size-1)
            if self.grid[y][x] =='.':
                return x,y

    def set_food(self,i: int | bool =None) -> None:
        if i is None:
            i=self.config.initial_food
        for _ in range(i):
            food_x,food_y = self._random_empty_cell()
            self.grid[food_y][food_x] = 'F'
            self.food_position.append((food_x, food_y))

    # def add_organisms(self,organism: "Organism") -> None:
    #       self.organism.append(organism)

    def remove_organisms(self,organism:"Organism") -> None:
        self.grid[organism.life_y][organism.life_x] = '.'
#prey 猎物


class Organism(object):
    org_count = 0
    def __init__(self,
                 world:World ,
                 vision_range:bool | float=None,
                 move_cost:bool | float=None,
                 generation:int =0,
                 config:OrganismConfig=OrganismConfig(),
                 event_bus: EventBus | bool=None) -> None:

        n=1
        self.ID = Organism.org_count
        self.event_bus=event_bus
        self.config=config
        self.generation=generation
        self.world = world
        self.is_alive = True
        self.energy = config.energy
        self.move_cost=move_cost if move_cost is not None else random.randint(3,6)
        self.vision_range=vision_range if vision_range is not None else random.randint(3,5)
        self.prey=[]

        while True:
            # print(f'======放置生命的次数{n}+++++++')
            self.life_x,self.life_y=random.randint(0,world.world_size-1),random.randint(0,world.world_size-1)
            # n+=1
            if world.grid[self.life_y][self.life_x]=='.':
                world.grid[self.life_y][self.life_x]='0'
                Organism.org_count += 1
                self.id=Organism.org_count
                self.event_bus.publish("organism_born",self)
                break

    def __repr__(self) -> str:
        return f'Organism({self.ID})'

    def can_reproduce(self)-> bool | None:
        if self.energy >self.config.energy_to_reproduct:
            return True

    def reproduce(self)->  "None | Organism" :
        if not self.can_reproduce():
            return None
        if random.random()>0.5:
            return None
        child_vision_range=self.vision_range+random.randint(-1,1)
        child_move_cost=self.move_cost+random.randint(-1,1)
        child=Organism(self.world,child_vision_range,child_move_cost,self.generation+1,event_bus=self.event_bus)
        return child








    def death(self) -> None:
        if  self.is_alive:
            return  None
        self.update()
        self.world.remove_organisms(self)
        self.event_bus.publish("organism_died",self)

    def check_death(self) -> None:
        if self.energy <= 0:
            self.is_alive = False
            self.death()
        return None


    def jud_obstacle(self,
                     new_x:int,
                     new_y:int,
                     old_x:int,
                     old_y:int) -> tuple[int,int]:
        if self.world.grid[new_y][new_x] == '0':
            return old_x,old_y
        return new_x,new_y


    def jud_move(self,
                 new_x:int,
                 new_y:int) -> None:
        self.world.grid[self.life_y][self.life_x] = '.'
        self.world.grid[new_y][new_x] = '0'
        self.life_x,self.life_y=new_x,new_y
        self.energy -= self.move_cost
        self.check_death()





    def move(self) -> tuple[int,int]:

        move_x, move_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        new_x = self.life_x + move_x
        new_y = self.life_y + move_y
        new_x = max(0, min(new_x, self.world.world_size - 1))
        new_y = max(0, min(new_y, self.world.world_size - 1))
        new_x,new_y = self.jud_obstacle(new_x,new_y,self.life_x,self.life_y)
        self.jud_move(new_x,new_y)
        return new_x,new_y




    def jud(self,x:int,y:int) -> None:

        if self.world.grid[y][x] == 'F':

            self.prey.append((x, y))


    def search_food(self) -> list[tuple[int,int]]:
        self.prey=[]
        visible_x=(max(0,self.life_x-self.vision_range),min(self.world.world_size-1,self.life_x+self.vision_range))
        visible_y=(max(0,self.life_y-self.vision_range),min(self.world.world_size-1,self.life_y+self.vision_range))
        # print(f'视野x{visible_x}      视野y{visible_y}')
        for y in range(visible_y[0],visible_y[1]+1):
            for x in range(visible_x[0],visible_x[1]+1):
                self.jud(x,y)
        self.prey.sort(key=lambda tur:abs(tur[0]-self.life_x)+abs(tur[1]-self.life_y))
        return self.prey
#一步到位，直接到达目的地
#先算步数




    def goal_move(self,
                  goal_x:int,
                  goal_y:int) -> None:
            if not self.is_alive:
                return None
            if goal_x!=self.life_x:
                move_x=1 if goal_x>self.life_x else -1
                move_y=0
            elif goal_y!=self.life_y:
                move_x=0
                move_y=1 if goal_y>self.life_y else -1
            else:
                return None
            new_x=self.life_x+move_x
            new_y=self.life_y+move_y
            new_x,new_y = self.jud_obstacle(new_x,new_y,self.life_x,self.life_y)
            self.jud_move(new_x, new_y)

    #待优化，如果目标处，是食物的话，前进与进食事件一并触发
    def eat(self) -> None:
        self.goal_move(self.prey[0][0], self.prey[0][1])
        if (self.life_x, self.life_y) in self.prey:  # 在猎物里面
            if not (self.life_x, self.life_y) in self.world.food_position:  # 在猎物里但不在食物里面，也就是防备它已经被别人吃了
                self.prey.remove((self.life_x, self.life_y))
                return None
            self.energy += self.config.food_energy
            self.event_bus.publish("organism_ate", self)  # 来自事件总线的提示
            self.world.food_position.remove((self.life_x, self.life_y))
            self.prey.remove((self.life_x, self.life_y))



