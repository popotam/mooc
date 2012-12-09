import pylab
import math
import random


class Location(object):
    def __init__(self, x, y):
        """x and y are floats"""
        self.x = x
        self.y = y

    def move(self, deltaX, deltaY):
        """deltaX and deltaY are floats"""
        return Location(self.x + deltaX, self.y + deltaY)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distFrom(self, other):
        ox = other.x
        oy = other.y
        xDist = self.x - ox
        yDist = self.y - oy
        return (xDist ** 2 + yDist ** 2) ** 0.5

    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'


class Field(object):
    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc

    def moveDrunk(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        # use move method of Location to get new location
        self.drunks[drunk] = currentLocation.move(xDist, yDist)

    def getLoc(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


import random


class Drunk(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'This drunk is named ' + self.name


def walkVector(f, d, numSteps):
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return(f.getLoc(d).getX() - start.getX(),
           f.getLoc(d).getY() - start.getY())


class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices = \
            [(0.0, 1.0), (0.0, -1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)


class ColdDrunk(Drunk):
    def takeStep(self):
        stepChoices = \
            [(0.0, 0.9), (0.0, -1.03), (1.03, 0.0), (-1.03, 0.0)]
        return random.choice(stepChoices)


class EDrunk(Drunk):
    def takeStep(self):
        ang = 2 * math.pi * random.random()
        length = 0.5 + 0.5 * random.random()
        return (length * math.sin(ang), length * math.cos(ang))


class PhotoDrunk(Drunk):
    def takeStep(self):
        stepChoices = \
                    [(0.0, 0.5), (0.0, -0.5),
                     (1.5, 0.0), (-1.5, 0.0)]
        return random.choice(stepChoices)


class DDrunk(Drunk):
    def takeStep(self):
        stepChoices = \
                    [(0.85, 0.85), (-0.85, -0.85),
                     (-0.56, 0.56), (0.56, -0.56)]
        return random.choice(stepChoices)


def run_sim(drunk_type, num=1000):
    field = Field()
    start = Location(0.0, 0.0)
    xes, ys = [], []
    for drunk in xrange(1000):
        drunk = drunk_type(None)
        field.addDrunk(drunk, start)
        x, y = walkVector(field, drunk, 1000)
        xes.append(x)
        ys.append(y)
    return xes, ys


def show_drunk_plot(drunk_type):
    """
    What information does the plot produced by this function tell you?
    """
    xes, ys = run_sim(drunk_type)
    pylab.plot(xes, ys, marker=",", linestyle="")
    pylab.title("title")
    pylab.legend((str(drunk_type),))
    pylab.xlabel("x_label")
    pylab.ylabel("y_label")
    pylab.show()


# 7


def sampleQuizzes(numTrials=10000):
    hits = 0.0
    for i in xrange(numTrials):
        mid1 = random.randint(50, 60)
        mid2 = random.randint(60, 90)
        final = random.randint(55, 95)
        score = (mid1 + mid2 + 2 * final) / 4.0
        if score >= 70 and score <= 75:
            hits += 1.0
    return hits / numTrials


def generateScores(numTrials):
    """
    Runs numTrials trials of score-generation for each of
    three exams (Midterm 1, Midterm 2, and Final Exam).
    Generates uniformly distributed scores for each of
    the three exams, then calculates the mean score and
    appends it to a list of scores.

    Returns: A list of numTrials scores.
    """
    scores = []
    for i in xrange(numTrials):
        mid1 = random.randint(50, 60)
        mid2 = random.randint(60, 90)
        final = random.randint(55, 95)
        score = (mid1 + mid2 + 2 * final) / 4.0
        scores.append(score)
    return scores


def plotQuizzes(trials=10000):
    # Your code here
    # show, plot, title, xlabel, ylabel, legend, figure, and hist
    scores = generateScores(trials)
    pylab.hist(scores, bins=7)
    pylab.title("Distribution of Scores")
    # pylab.legend((str(drunk_type),))
    pylab.xlabel("Final Score")
    pylab.ylabel("Number of Trials")
    pylab.show()



if __name__ == "__main__":
    # show_drunk_plot(DDrunk)
    plotQuizzes()
