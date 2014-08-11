from collections import defaultdict
import csv
import json
import sys


def main():
    sentiments = dict(
        (term, float(score)) for term, score in
        csv.reader(open(sys.argv[1]), dialect='excel-tab')
    )
    term_scores  = defaultdict(list)
    for line in open(sys.argv[2]):
        tweet_score = 0.0
        unknown_terms = set()
        tweet = json.loads(line)
        for term in tweet.get('text', '').split():
            if term in sentiments:
                tweet_score += sentiments[term]
            else:
                unknown_terms.add(term)
        for term in unknown_terms:
            term_scores[term].append(tweet_score)
    # print new terms with scores
    for term, scores in term_scores.iteritems():
        print term.encode('utf-8'), sum(scores) / len(scores)


if __name__ == '__main__':
    main()
