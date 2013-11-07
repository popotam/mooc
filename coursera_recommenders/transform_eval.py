#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

from collections import defaultdict
import csv


ROWS = [
    'Algorithm', 'Partition', 'DataSet', 'NNbrs', 'BuildTime', 'TestTime',
    'NUsers', 'NAttempted', 'NGood', 'Coverage', 'RMSE.ByRating', 'RMSE.ByUser',
    'nDCG', 'TopN.nDCG', 'TagEntropy@10',
]


def safe_float(value):
    try:
        return float(value)
    except:
        return None


def main():
    with open('eval-results.csv') as f:
        data = list(csv.DictReader(f))
    grouped = defaultdict(list)
    for test in data:
        grouped[test['Algorithm'], test['NNbrs']].append(test)
    new_data = []
    for (algo, nnbrs), group in sorted(grouped.iteritems()):
        aggregate = {
            'Algorithm': algo,
            'Partition': '',
            'DataSet': group[0]['DataSet'],
            'NNbrs': nnbrs,
        }
        for key in ROWS[4:]:
            values = [
                float(test[key]) for test in group
                if isinstance(safe_float(test[key]), float)
            ]
            if len(values) == 0:
                aggregate[key] = ''
                continue
            aggregate[key] = sum(values) / len(values)
        new_data.append(aggregate)
    with open('aggregated_eval.csv', 'w') as f:
        writer = csv.DictWriter(f, ROWS)
        writer.writerows([{key: key for key in ROWS}])
        writer.writerows(new_data)


if __name__ == '__main__':
    main()
