import random

world_size=5
world=[['.' for _ in range(world_size)] for _ in range(world_size)]

life_x, life_y = world_size // 2, world_size // 2
world[life_y][life_x] = '0'


def look(w):
    print('初始化世界：  ')
    for i in w:
        print('  '.join(i))


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


#放置食物
def food():
    global food_x,food_y
    n=0
    food_x,food_y=random.randint(0,world_size-1),random.randint(0,world_size-1)
    while world[food_y][food_x]!='.':
        n+=1
        food_x, food_y = random.randint(0, world_size - 1), random.randint(0, world_size - 1)
    print(f'进行了{n}次放置')
    world[food_y][food_x]='F'
    return food_x,food_y

food_x,food_y=food()
look(world)

n=0
for _ in range(30):
    a = abs(life_x - food_x) + abs(life_y - food_y)
    if a==1 :
        world[food_y][food_x]='0'
        world[life_y][life_x]='.'
        life_x,life_y=food_x,food_y
        look(world)
        n+=1
        print(f'=======总共进行{n}次运动=======')
        print('========吃饱了，开心心=========')
        break
    else:
        move()
        look(world)
        n+=1
        print(f'=======第{n}次移动========')





























































