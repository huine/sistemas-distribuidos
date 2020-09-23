from threading import Lock, Thread
import random
import time

# Dining philosophers, 5 Phillies with 5 forks. Must have two forks to eat.
#
# Deadlock is avoided by never waiting for a fork while holding a fork (locked)
# Procedure is to do block while waiting to get first fork, and a nonblocking
# acquire of second fork.  If failed to get second fork, release first fork,
# swap which fork is first and which is second and retry until getting both.
#
# See discussion page note about 'live lock'.

t_count = 1


class Philosopher(Thread):

    running = True

    def __init__(self, xname, forkOnLeft, forkOnRight):
        Thread.__init__(self)
        self.name = xname
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight
        self.thinking_time = 0.1
        self.eating_time = 1
        self.status = None

    def run(self):
        while(self.running):
            #  Philosopher is thinking (but really is sleeping).
            global t_count
            self.status = "T"
            t_count += 1
            print ('%s is thinking.' % self.name)
            time.sleep(self.thinking_time)
            self.status = "H"
            print ('%s is hungry.' % self.name)
            self.dine()

    def dine(self):
        fork1, fork2 = self.forkOnLeft, self.forkOnRight

        while self.running:
            fork1.acquire(True)
            locked = fork2.acquire(True)
            if locked:
                break
            # fork1.release()
            # print('%s swaps forks' % self.name)
            # fork1, fork2 = fork2, fork1
        else:
            return

        self.dining()
        fork2.release()
        fork1.release()

    def dining(self):
        self.status = "E"
        time.sleep(self.eating_time)
        print('%s finishes eating and leaves to think.' % self.name)


def DiningPhilosophers(num_ph=5):
    forks = [Lock() for n in range(num_ph)]
    philosopherNames = [i + 1 for i in range(num_ph)]

    philosophers = [
        Philosopher(
            philosopherNames[i],
            forks[i % num_ph],
            forks[(i+1) % num_ph])
        for i in range(num_ph)
    ]

    random.seed(507129)
    Philosopher.running = True
    for p in philosophers:
        p.start()

    global t_count
    last_print = ''
    while t_count < 100000:
        new_print = ("Ciclo {} -" + " {}"*num_ph).format(*([t_count] + ['P{}:{}'.format(i.name, i.status) for i in philosophers]))
        if new_print != last_print:
            last_print = new_print
            print(new_print)

    Philosopher.running = False
    print("Now we're finishing.")


if __name__ == "__main__":
    DiningPhilosophers()
