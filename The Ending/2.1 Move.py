import random

world_size=5
world=[['.' for _ in range(world_size)] for _ in range(world_size)]

life_x, life_y = world_size // 2, world_size // 2
world[life_y][life_x] = '0'


def look(w):
    print('初始化世界：  ')
    for i in w:
        print('  '.join(i))



#放置食物
def food():
    n=0
    food_x,food_y=random.randint(0,world_size-1),random.randint(0,world_size-1)
    while world[food_y][food_x]!='.':
        n+=1
        food_x, food_y = random.randint(0, world_size - 1), random.randint(0, world_size - 1)
    print(f'进行了{n}次放置')
    world[food_y][food_x]='F'
    return food_x,food_y


def gaol_move(food_x,food_y):

    move_x,move_y=0,0

    global life_x, life_y
    for step in range(1000):
        if world[food_y][food_x]==world[life_y][life_x]:
            print(f'总共{step}')
            print('========吃到了，开心心=========')
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
        print(f'======这是第{step}步=======')
        look(world)



if __name__ == '__main__':
    food_x,food_y=food()
    gaol_move(food_x,food_y)


































