world=[]
for i in range(5):
    row=[]
    for j in range(5):
        row.append('.')
    world.append(row)
print(world)
world[2][2]='0'
for i in world:
    print('  '.join(i))
