import random
import math

class SetGenerator:

    def generate_linear(self):

        examples = []
        labels = []

        for i in range(100):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            f = x * 2 + 0.3

            examples.append([x, y])
            labels.append(int(f < y))

        return (examples, labels)

    def generate_circle(self, n):

        examples = []
        labels = []

        for i in range(n):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            r = math.sqrt(x*x+y*y)

            examples.append([x, y])
            labels.append(int(r < 0.3))

        return (examples, labels)

    def generate_circle_2(self, n):

        examples = []
        labels = []

        x1 = 0.5
        y1 = 0.5
        r1 = 0.6

        x2 = -0.2
        y2 = 0.15
        r2 = 0.3

        for i in range(n):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)

            dx1 = x-x1
            dy1 = y-y1
            d1 = math.sqrt(dx1*dx1+dy1*dy1)

            dx2 = x-x2
            dy2 = y-y2
            d2 = math.sqrt(dx2*dx2+dy2*dy2)

            examples.append([x, y])
            labels.append(int(d1 < r1 or d2 < r2))

        return (examples, labels)