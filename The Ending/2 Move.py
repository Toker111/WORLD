import random

world_size=5
world=[['.' for _ in range(world_size)] for _ in range(world_size)]
def look(w):
    print('初始化世界：  ')
    for i in w:
        print('  '.join(i))

#随机运动
def move(x,y):
    move_x,move_y=random.choice([(0,1),(0,-1),(1,0),(-1,0)])
    new_x=x+move_x
    new_y=y+move_y
    new_x=max(0,min(new_x,world_size-1))
    new_y=max(0,min(new_y,world_size-1))
    world[x][y]='.'
    world[new_x][new_y]='0'
    global life_x,life_y
    life_x,life_y=new_x,new_y
def run(times):
    for n in range(times):
        move(life_x,life_y)
        look(world)

#放置食物
def food():
    n=0
    food_x,food_y=random.randint(0,world_size-1),random.randint(0,world_size-1)
    while world[food_x][food_y]!='.':
        n+=1
        food_x, food_y = random.randint(0, world_size - 1), random.randint(0, world_size - 1)
    print(f'进行了{n}次放置')
    world[food_x][food_y]='F'
    return food_x,food_y

#进行有目的性的运动
def goal_go(food_x,food_y):
    a=0
    global life_x,life_y
    gap_x=food_x-life_x
    if gap_x<0:
        for i in range(abs(gap_x)):
            world[life_x][life_y]='.'
            life_x-=1
            world[life_x][life_y]='0'
            print(f"这是第{i}步")
            a=i
            look(world)
    elif gap_x>0:
        for i in range(abs(gap_x)):
            world[life_x][life_y]='.'
            life_x+=1
            world[life_x][life_y]='0'
            print(f"这是第{i}步")
            a=i
            look(world)
    gap_y=food_y-life_y
    if gap_y<0:
        for i in range(abs(gap_x)):
            world[life_x][life_y]='.'
            life_y-=1
            world[life_x][life_y]='0'
            print(f"这是第{a+1+i}步")
            look(world)
    elif gap_y>0:
        for i in range(abs(gap_x)):
            world[life_x][life_y]='.'
            life_y+=1
            world[life_x][life_y]='0'
            print(f"这是第{a+1+i}步")
            look(world)


if __name__ == '__main__':
    #初始化将生物放到中间
    life_x,life_y=world_size//2,world_size//2
    world[life_x][life_y]='0'

    a,b=food()

    goal_go(a,b)































