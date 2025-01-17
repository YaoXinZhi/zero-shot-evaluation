#!/bin/env python


import json
import sys
import re
from datetime import datetime
import argparse


def log(msg):
    now = datetime.now()
    sys.stderr.write(now.strftime('[%Y-%m-%d %H:%M:%S] ') + msg + '\n')


log('start')


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


def parse_json(rep):
    filename = f'output/repetition/{args.model}/{args.instruction}/{args.document}/{rep}.txt'
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
        ename = e['name']
        yield etype, ename


def get_relations(j):
    for r in j['relationships']:
        rsource = r['source']
        rtype = r['type']
        rtarget = r['target']
        yield rtype, rsource, rtarget


def get_annotations(j):
    yield from get_entities(j)
    yield from get_relations(j)


ANN_MAP = dict((rep, set(get_annotations(parse_json(rep)))) for rep in range(1, REPEATS + 1))
ALL_ANNOTATIONS = set.union(*ANN_MAP.values())


def get_row(a):
    result = [0, 0]
    for ranns in ANN_MAP.values():
        idx = int(a in ranns)
        result[idx] += 1
    return result


# from https://github.com/Shamya/FleissKappa/blob/master/fleiss.py
def checkInput(rate, n):
    """ 
    Check correctness of the input matrix
    @param rate - ratings matrix
    @return n - number of raters
    @throws AssertionError 
    """
    N = len(rate)
    k = len(rate[0])
    assert all(len(rate[i]) == k for i in range(k)), "Row length != #categories)"
    assert all(isinstance(rate[i][j], int) for i in range(N) for j in range(k)), "Element not integer" 
    assert all(sum(row) == n for row in rate), "Sum of ratings != #raters)"


def fleissKappa(rate,n):
    """ 
    Computes the Kappa value
    @param rate - ratings matrix containing number of ratings for each subject per category 
    [size - N X k where N = #subjects and k = #categories]
    @param n - number of raters   
    @return fleiss' kappa
    """

    N = len(rate)
    k = len(rate[0])
    print("#raters = ", n, ", #subjects = ", N, ", #categories = ", k)
    checkInput(rate, n)

    #mean of the extent to which raters agree for the ith subject 
    PA = sum([(sum([i**2 for i in row])- n) / (n * (n - 1)) for row in rate])/N
    print("PA = ", PA)
    
    # mean of squares of proportion of all assignments which were to jth category
    PE = sum([j**2 for j in [sum([rows[i] for rows in rate])/(N*n) for i in range(k)]])
    print("PE =", PE)
    
    try:
        return (PA - PE) / (1 - PE)
    except ZeroDivisionError:
        return 1.0


matrix = list(get_row(a) for a in ALL_ANNOTATIONS)


print(matrix)
print(fleissKappa(matrix, REPEATS))
