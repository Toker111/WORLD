import random
import math
world_size=8
world=[['.' for _ in range(world_size)] for _ in range(world_size)]



def people():
    global life_x,life_y
    life_x,life_y=random.randint(0,world_size-1),random.randint(0,world_size-1)
    while world[life_y][life_x]!='.':
        life_x, life_y = random.randint(0, world_size - 1), random.randint(0, world_size - 1)
    world[life_y][life_x]='0'
    return life_x,life_y
life_x,life_y=people()







def look(w):
    print('初始化世界：  ')
    for _ in w:
        print('  '.join(_))
#放置食物
food_position=[]
n=0
def food():
    global food_x,food_y
    food_x,food_y=random.randint(0,world_size-1),random.randint(0,world_size-1)
    while world[food_y][food_x]!='.':
        food_x, food_y = random.randint(0, world_size - 1), random.randint(0, world_size - 1)
    world[food_y][food_x]='F'
    food_position.append((food_x,food_y))


n=0
def gaol_move(food_x,food_y):

    move_x,move_y=0,0

    global life_x, life_y,n
    for step in range(1000):
        if world[food_y][food_x]==world[life_y][life_x]:
            print(f'总共{n}')
            print('========吃到了，开心心=========')
            # ==========移除被吃掉的食物===========
            food_position.remove((food_x,food_y))
            return
        if food_x!=life_x:
            move_x=1 if food_x>life_x else -1
            move_y=0
        else:
            move_x=0
            move_y=1 if food_y>life_y else -1
        world[life_y][life_x]='.'
        life_x+=move_x
        life_y+=move_y
        world[life_y][life_x]='0'
        n+=1
        print(f'======这是第{n}步=======')
        look(world)
def move():
    global life_x, life_y
    move_x,move_y=random.choice([(0,1),(0,-1),(1,0),(-1,0)])
    new_x=life_x+move_x
    new_y=life_y+move_y
    new_x=max(0,min(new_x,world_size-1))
    new_y=max(0,min(new_y,world_size-1))
    world[life_y][life_x]='.'
    world[new_y][new_x]='0'
    life_x,life_y=new_x,new_y
look(world)
vision_range=4

for i in range(6):
    food()
#计算当前位置与食物的距离
look(world)

for i in range(100):
    visible_food = []
    if not food_position:
        break
    for x, y in food_position:
        distance = math.sqrt((x - life_x) ** 2 + (y - life_y) ** 2)
        if distance < vision_range:
            visible_food.append((x, y, distance))

    visible_food = sorted(visible_food, key=lambda item: item[2])
    if visible_food:
        print(f'=========当前目标{visible_food[0][0],visible_food[0][1]}=========')
        gaol_move(visible_food[0][0],visible_food[0][1])
        print(f"=============剩余{len(visible_food)}========")
    else:
        move()
        print('========我随机走了一步哦========')








































