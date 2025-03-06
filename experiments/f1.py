#!/bin/env python


import json
import sys
import re
from datetime import datetime
import argparse


def log(msg):
    now = datetime.now()
    sys.stderr.write(now.strftime('[%Y-%m-%d %H:%M:%S] ') + msg + '\n')


parser = argparse.ArgumentParser(
    prog='run'
)
parser.add_argument('-i', '--instruction', type=str, action='store')
parser.add_argument('-d', '--document', type=str, action='store')
parser.add_argument('-o', '--output', type=str, action='store')
parser.add_argument('-m', '--model', type=str, action='store')


args = parser.parse_args()


REPEATS = 5


CODEBLOCK = re.compile('```json(.*)```', re.DOTALL)


def parse_json(filename):
    # filename = 
    with open(filename) as f:
        content = f.read().strip()
    m = CODEBLOCK.fullmatch(content)
    if m is None:
        jc = content
    else:
        jc = m.group(1)
    j = json.loads(jc)
    if type(j) == list:
        return j[0]
    return j


def get_entities(j):
    for e in j['entities']:
        etype = e['type']
        assert type(etype) == str
        ename = e['name']
        assert type(ename) == str
        yield etype.lower(), ename.lower()


def get_relations(j):
    for r in j['relationships']:
        rsource = r['source']
        assert type(rsource) == str
        rtype = r['type']
        assert type(rtype) == str
        rtarget = r['target']
        assert type(rtarget) == str
        yield rtype.lower(), rsource.lower(), rtarget.lower()


def get_reference_relations(j):
    for r in j['relationships']:
        args = list(r['arguments'].values())
        rsource = args[0]
        assert type(rsource) == str
        rtype = r['type']
        assert type(rtype) == str
        rtarget = args[1]
        assert type(rtarget) == str
        yield rtype.lower(), rsource.lower(), rtarget.lower()


def get_annotations(j):
    yield from get_entities(j)
    yield from get_relations(j)


def get_reference_annotations(j):
    yield from get_entities(j)
    yield from get_reference_relations(j)


REFERENCE = set(get_reference_annotations(parse_json(f'../Reference answer Extraction scenario/Information{args.document}.txt')))


def get_f(rep):
    PREDICTION = set(get_annotations(parse_json(f'output/repetition/{args.model}/{args.instruction}/Texte{args.document}/{rep}.txt')))
    TP = len(REFERENCE & PREDICTION)
    try:
        R = float(TP) / len(REFERENCE)
        P = float(TP) / len(PREDICTION)
        F = 2 * R * P / (R + P)
        return F
    except ZeroDivisionError:
        return 0.0


SCORES = list(get_f(rep) for rep in range(1, REPEATS + 1))
SCORES.sort()
print(SCORES[REPEATS//2])
