import random
import pandas as pd
from Config import WorldConfig,OrganismConfig
import mypy


class World(object):
    def __init__(self,config : WorldConfig=WorldConfig()):
        self.config = config
        self.t=0
        self.world_size = config.size
        self.grid= [['.' for _ in range(self.world_size)] for _ in range(self.world_size)]
        self.food_position=[]
        self.organism=[]
        self.Organism=pd.DataFrame({"id":[],'energy':[],'move_cost':[],'vision_range':[],'age':[],'generation':[]})

    def look(self) -> None:
        # print(f'=================={self.t}+++++++++++++++++++++++')
        for _ in self.grid:
            print('  '.join(_))
            # self.t+=1

    def set_food(self,i: int | bool =None) -> None:
        if i is None:
            i=self.config.initial_food
        for _ in range(i):
            food_x, food_y = random.randint(0, self.world_size - 1), random.randint(0, self.world_size - 1)
            while self.grid[food_y][food_x] != '.':
                food_x, food_y = random.randint(0, self.world_size - 1), random.randint(0, self.world_size - 1)
            self.grid[food_y][food_x] = 'F'
            self.food_position.append((food_x, food_y))

    def set_organisms(self,organism: "Organism") -> None:
        self.organism.append(organism)

    def remove_organisms(self,organism:"Organism") -> None:
        self.organism.remove(organism)
        self.grid[organism.life_y][organism.life_x] = '.'
        print(f'=====玩家 {organism}已死亡++++++')
#prey 猎物

class Organism(object):
    org_count = 0
    def __init__(self,
                 world:World ,
                 vision_range:bool | float=None,
                 move_cost:bool | float=None,
                 generation:int =0,
                 config:OrganismConfig=OrganismConfig()) -> None:

        n=1
        self.config=config
        self.generation=generation
        self.world = world
        self.is_alive = True
        self.energy = config.energy
        self.move_cost=move_cost if move_cost is not None else random.randint(3,6)
        self.vision_range=vision_range if vision_range is not None else random.randint(3,5)
        self.prey=[]
        self.step=0
        self.stop=0
        while True:
            print(f'======放置生命的次数{n}+++++++')
            self.life_x,self.life_y=random.randint(0,world.world_size-1),random.randint(0,world.world_size-1)
            n+=1
            if world.grid[self.life_y][self.life_x]=='.':
                world.grid[self.life_y][self.life_x]='0'
                Organism.org_count += 1
                self.id=Organism.org_count
                new_org=pd.DataFrame({"id":[self.org_count],'energy':[f'{self.energy}'],'vision_range':[f'{self.vision_range}'],'move_cost':[f'{self.move_cost}'],'age':[0],'generation':[self.generation]})
                self.world.Organism=pd.concat([new_org,self.world.Organism],ignore_index=True)

                break
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
        child=Organism(self.world,child_vision_range,child_move_cost,self.generation+1)

        return child


#记录存活时间
    def update(self) -> None:
        self.world.Organism.loc[self.world.Organism['id'] == self.id, 'age'] = self.step





    def death(self) -> None:
        if  self.is_alive:
            return  None
        self.update()
        self.world.remove_organisms(self)
        print('=======旅途结束++++++++')

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
            print('====STOP+++++')
            print(f'======{self.step}+++++++')
            self.step += 1
            return old_x,old_y
        return new_x,new_y


    def jud_move(self,
                 new_x:int,
                 new_y:int) -> None:
        self.world.grid[self.life_y][self.life_x] = '.'
        self.world.grid[new_y][new_x] = '0'
        self.life_x,self.life_y=new_x,new_y
        self.step += 1
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


    def eat(self) -> None:
        if (self.life_x,self.life_y) in self.prey: #在猎物里面
            if not (self.life_x,self.life_y) in self.world.food_position: #在猎物里但不在食物里面，也就是防备它已经被别人吃了
                self.prey.remove((self.life_x,self.life_y))
                return None
            self.energy += self.config.food_energy
            print('我吃掉了一个，开心心')
            print(f'世界中的食物位置{self.world.food_position}')
            # print(f'目标食物位置  {self.life_x},{self.life_y}')
            self.world.food_position.remove((self.life_x,self.life_y))
            self.prey.remove((self.life_x,self.life_y))
        else:
            self.goal_move(self.prey[0][0], self.prey[0][1])



# def read_in(df):
#
#
#     file_path = 'output.xlsx'
#     sheet_name = 'Sheet1'
#
#     # 创建 ExcelWriter，以追加模式打开，使用 openpyxl 引擎，如果工作表存在则覆盖（但不会清除已有数据）
#     writer = pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay')
#
#     # 直接使用 writer.sheets 获取工作表对象
#     sheet = writer.sheets[sheet_name]
#     startrow = sheet.max_row  # 已有数据的最后一行
#
#     # 将新数据写入，从 startrow 开始（注意：to_excel 的 startrow 是从0开始，且不包含表头）
#     df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=startrow, header=False)
#
#     writer.close()


#生命周期
#1生成生物
#2检测视野范围内是否有食物
#有 规划路线，吃  #无 随机走一步
#多个记住
def main() -> None:
    time=0
    world1=World()
    for _ in range(10):
        tjm=Organism(world1)
        world1.set_organisms(tjm)
    world1.set_food()
    for _ in range(10000):

        #如果世界没有生物了
        if not world1.organism:
            print('\n===================死亡后的世界+++++++++++++++++')
            world1.look()
            print('=====死亡不是终点，期待王的新生++++++')
            print(world1.Organism.sample(10))
            # read_in(world1.Organism)
            return None

        #如果世界的食物都没有了
        if world1.food_position==[]:
            world1.set_food()
            print('========恭喜恭喜，完成了世界吞噬的任务，原此行终得灵智，赞美新生=========')
            return None
        #几个生物就执行几次，搜寻食物
        for _ in world1.organism:
            tjm.search_food()

        #打乱执行顺序
        random.shuffle(world1.organism)

        #主要运行的代码
        for i in world1.organism:
            if i.prey==[]:
                i.move()
            else:
                i.eat()
                t_child=i.reproduce()
                if t_child:
                    world1.set_organisms(t_child)


        print(f'=========================={time}++++++++++++++++++++++++++++')
        world1.look()
        time+=1










if __name__ == '__main__':
    main()
