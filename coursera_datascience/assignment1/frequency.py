from collections import defaultdict
import json
import sys


def main():
    count = 0.0
    terms = defaultdict(float)
    for line in open(sys.argv[1]):
        tweet = json.loads(line)
        words = tweet.get('text', '').split()
        for word in words:
            terms[word] += 1.0
            count += 1.0
    for term, term_count in terms.iteritems():
        print term.encode('utf-8'), term_count / count


if __name__ == '__main__':
    main()
