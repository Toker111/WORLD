from Simulation import *
from mworld import *
def main():
    sim=Simulation()

    for _ in range(1):
        tjm=Organism(sim.world,event_bus=sim.eventbus)
    sim.run()

if __name__=="__main__":
    main()