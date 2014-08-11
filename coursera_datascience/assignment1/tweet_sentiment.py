import csv
import json
import sys


def main():
    sentiments = dict(
        (word, float(score))
        for word, score in
        csv.reader(open(sys.argv[1]), dialect='excel-tab')
    )
    for line in open(sys.argv[2]):
        tweet = json.loads(line)
        if 'text' not in tweet:
            continue
        words = tweet.get('text', '').split()
        score = sum((sentiments.get(word, 0) for word in words), 0.0)
        print score


if __name__ == '__main__':
    main()
