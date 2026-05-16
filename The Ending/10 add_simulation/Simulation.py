from mworld import World,Organism
import pandas as pd
from events import EventBus
from Config import *
import random
class Simulation :
    def __init__(self) -> None:
        self.data_log = pd.DataFrame(columns=["id","energy","move_cost","vision_range","age","generation"])
        self.organisms = [] #存活的生物列表
        self.world=World(WorldConfig())
        self.org_config=OrganismConfig()
        self.eventbus=EventBus()
        self.time=0

        self.eventbus.subscribe("organism_died",self._on_organism_died)
        self.eventbus.subscribe("organism_born",self._on_organism_born)
        self.eventbus.subscribe("organism_ate",self._on_organism_ate)

    def _on_organism_born(self,org:"Organism") -> None:
        self.organisms.append(org)
        new_row=pd.DataFrame({"id":[org.org_count],
                               'energy':[f'{org.energy}'],
                               'vision_range':[f'{org.vision_range}'],
                               'move_cost':[f'{org.move_cost}'],
                               'age':[0],
                               'generation':[org.generation]})
        self.data_log=pd.concat([self.data_log,new_row],ignore_index=True)
        print(f"生物{org.ID},世代{org.generation}  出生了")

    def _on_organism_died(self,org:"Organism") -> None:
        #去除存活生物列表的死亡生物
        if org in self.organisms:
            self.organisms.remove(org)
        #去除网格上的死亡生物      （ideal：死亡的生物可以变成食物）
        self.world.remove_organisms(org)
        self.data_log.loc[self.data_log['id'] == org.id, 'age'] = self.time
        print(f"生物{org.ID},存活时间{self.time}")

    def _on_organism_ate(self,org) -> None:
        print(f"{org}吃了一个食物，开心心")




    def run(self,max_steps:int=1000) -> None:
        self.world.set_food()

        for _ in range(max_steps):
            print(f'=========================={self.time}++++++++++++++++++++++++++++')
            # 如果世界没有生物了
            if not self.organisms:
                print('\n===================死亡后的世界+++++++++++++++++')
                self.world.look()
                print('=====死亡不是终点，期待王的新生++++++')
                return None

            # 如果世界的食物都没有了
            if self.world.food_position == []:
                print('========恭喜恭喜，完成了世界吞噬的任务，原此行终得灵智，赞美新生=========')
                return None

            # 几个生物就执行几次，搜寻食物
            for org in self.organisms[:]:
                org.search_food()

            # 打乱执行顺序
            random.shuffle(self.organisms)

            # 主要运行的代码
            for org in self.organisms[:]:
                if org.prey == []:
                    org.move()
                else:
                    org.eat()
                    t_child = org.reproduce()


            self.world.look()
            print("\n\n")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            self.time += 1
