from collections import defaultdict
import csv
import json
import sys


def main():
    sentiments = dict(
        (word, float(score))
        for word, score in
        csv.reader(open(sys.argv[1]), dialect='excel-tab')
    )
    states = defaultdict(list)
    for line in open(sys.argv[2]):
        tweet = json.loads(line)
        if 'text' not in tweet:
            continue
        if 'place' not in tweet or tweet['place'] is None:
            continue
        if tweet['place']['country_code'] != u'US':
            continue
        try:
            state = tweet['place']['full_name'].split(', ')[1]
        except:
            continue
        words = tweet.get('text', '').split()
        score = sum((sentiments.get(word, 0) for word in words), 0.0)
        states[state].append(score)
    states = [(sum(scores) / len(scores), state)
              for state, scores in states.iteritems()]
    states.sort(reverse=True)
    print states[0][1]


if __name__ == '__main__':
    main()
