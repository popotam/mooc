from collections import defaultdict
import json
import sys


def main():
    tags = defaultdict(float)
    for line in open(sys.argv[1]):
        tweet = json.loads(line)
        entities = tweet.get('entities', {})
        hashtags = entities.get('hashtags', [])
        for tag in hashtags:
            tags[tag['text']] += 1.0
    tags = tags.items()
    tags.sort(key=lambda x: -x[1])
    for i, (hashtag, count) in enumerate(tags[:10]):
        print hashtag.encode('utf-8'), count


if __name__ == '__main__':
    main()
