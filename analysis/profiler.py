''' profiler.py
A debugging feature to understand the use of processing time on each module. The
Profile class is first initialised in universe.py when the Universe class is
initialised. At certain points throughout the code, the module name and current
time is added to the profile.modules list as per: universe.profile.add('gravity')

Then at the end of each frame, astraea.py calls the print_profile function which
will calculate the total time spent on that frame, as well as the fraction of
that total time each module used up, and will print that information.
'''

import time

class Profile():
    def __init__(self):
        self.total = 0
        self.frame_end = time.time()
        self.modules = []
        self.display = False

    def add(self, name):
        self.modules.append([name, time.time()])

    def print_profile(self, dt):
        if self.display:
            totaltime = (time.time() - self.frame_end)
            total = str(round(1/dt)) + ' f/s, ' + str(1000*(totaltime))[0:4]+' ms/f | '
            for module in self.modules:
                total += module[0] + ': ' + str(100*(module[1] - self.frame_end)/totaltime)[0:4] + '% | '
                self.frame_end = module[1]
            print(total)
            self.frame_end = time.time()
        self.modules = []
