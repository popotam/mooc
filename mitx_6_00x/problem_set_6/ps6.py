# 6.00x Problem Set 6
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from Tkinter import *


#-----------------------------------------------------------------------
#
# Problem Set 6

#======================
# Code for retrieving and parsing RSS feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret
#======================

#======================
# Part 1
# Data structure design
#======================

# Problem 1


class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def getGuid(self):
        return self.guid

    get_guid = getGuid

    def getTitle(self):
        return self.title

    get_title = getTitle

    def getSubject(self):
        return self.subject

    get_subject = getSubject

    def getSummary(self):
        return self.summary

    get_summary = getSummary

    def getLink(self):
        return self.link

    get_link = getLink


#======================
# Part 2
# Triggers
#======================


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5


class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word

    def isWordIn(self, text):
        text = text.lower()
        for mark in string.punctuation:
            text = text.replace(mark, ' ')
        words = text.split()
        return self.word.lower() in words


class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        return self.isWordIn(story.getTitle())


class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        return self.isWordIn(story.getSubject())


class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        return self.isWordIn(story.getSummary())


# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)


class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


# Phrase Trigger
# Question 9

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        text = story.getTitle() + story.getSubject() + story.getSummary()
        return self.phrase in text


#======================
# Part 3
# Filtering
#======================

def filterStories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    return [story for story in stories
            if any(trigger.evaluate(story) for trigger in triggerlist)]

#======================
# Part 4
# User-Specified Triggers
#======================


def makeTrigger(triggerMap, triggerType, params, name):
    """
    Takes in a map of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and adds a new trigger
    to the trigger map dictionary.

    triggerMap: dictionary with names as keys (strings) and triggers as values
    triggerType: string indicating the type of trigger to make (ex: "TITLE")
    params: list of strings with the inputs to the trigger constructor (ex: ["world"])
    name: a string representing the name of the new trigger (ex: "t1")

    Modifies triggerMap, adding a new key-value pair for this trigger.

    Returns: None
    """
    # TODO: Problem 11
    trigger = triggerMap[name] = {
        'TITLE': TitleTrigger,
        'SUBJECT': SubjectTrigger,
        'SUMMARY': SummaryTrigger,
        'NOT': lambda t: NotTrigger(triggerMap[t]),
        'AND': lambda t1, t2: AndTrigger(triggerMap[t1], triggerMap[t2]),
        'OR': lambda t1, t2: OrTrigger(triggerMap[t1], triggerMap[t2]),
        'PHRASE': lambda *args: PhraseTrigger(" ".join(args)),
    }[triggerType](*params)
    return trigger


def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """

    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    lines = [line.rstrip() for line in triggerfile.readlines()
             if line.rstrip() and line.rstrip()[0] != '#']
    triggers = []
    triggerMap = {}

    # Be sure you understand this code - we've written it for you,
    # but it's code you should be able to write yourself
    for line in lines:

        linesplit = line.split(" ")

        # Making a new trigger
        if linesplit[0] != "ADD":
            # print triggerMap, linesplit[1], linesplit[2:], linesplit[0]
            trigger = makeTrigger(triggerMap, linesplit[1],
                                  linesplit[2:], linesplit[0])

        # Add the triggers to the list
        else:
            for name in linesplit[1:]:
                triggers.append(triggerMap[name])

    return triggers

import thread

SLEEPTIME = 60  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    try:
        # These will probably generate a few hits...
        t1 = TitleTrigger("Obama")
        t2 = SubjectTrigger("Romney")
        t3 = PhraseTrigger("Election")
        t4 = OrTrigger(t2, t3)
        triggerlist = [t1, t4]

        # TODO: Problem 11
        # After implementing makeTrigger, uncomment the line below:
        triggerlist = readTriggerConfig("triggers.txt")

        # from here is about drawing
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_summary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print "Polling . . .",
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

            stories = filterStories(stories, triggerlist)

            map(get_cont, stories)
            scrollbar.config(command=cont.yview)

            print "Sleeping..."
            time.sleep(SLEEPTIME)

    except Exception as e:
        print e


if __name__ == '__main__':

    root = Tk()
    root.title("Some RSS parser")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()