import math

class Amimation():
    def __init__(self, start, end, length):
        self.start = start
        self.end = end
        self.current = []
        self.frame = 0
        self.length = length
        self.animate = False

    def update(self):
        if self.animate:
            if self.frame > self.length:
                self.animate = False
                self.current = self.end
                return self.end
            else:
                for i in range(len(self.current)):
                    self.current[i] = self.start[i] + (self.end[i] - self.start[i]) * (math.sqrt(self.frame) / math.sqrt(self.length))
                self.frame += 1
                return self.current
        else:
            return False
    
    def start_animation(self):
        self.animate = True
        self.frame = 0
        self.current = [None for i in range(len(self.start))]
        for i in range(len(self.start)):
            self.current[i] = self.start[i]
        self.update()
