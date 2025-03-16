#!/bin/env python


import sys
from kbeval import *


def pair_label(pair):
    if pair.is_true_positive:
        return 'Match'
    if pair.is_partial_match:
        return 'Partial Match'
    if pair.is_false_positive:
        return 'False Positive'
    if pair.is_false_negative:
        return 'False Negative'
    return '???'


if __name__ == '__main__':
    _prog, ref_fn, pred_fn = sys.argv
    ref_ds = MergedRefDataset.from_json_file(ref_fn)
    pred_ds = Dataset.from_json_file(pred_fn)
    try:
        _base, _ie, pairs = evaluate(ref_ds, pred_ds, relaxed_type_similarity, relaxed_arg_similarity)
        print('\t'.join(['PAIR TYPE', 'SIMILARITY', 'SAME TYPE', 'REF TYPE', 'PRED TYPE', 'SOURCE SIMILARITY', 'REF SOURCES', 'PRED SOURCE', 'TARGET SIMILARITY', 'REF TARGETS', 'PRED TARGET']))
        for p in pairs:
            row = [''] * 9
            if p.has_ref:
                row[1] = p.ref.type_
                row[4] = ', '.join(p.ref.source.names)
                row[7] = ', '.join(p.ref.target.names)
            if p.has_pred:
                row[2] = p.pred.type_
                row[5] = p.pred.source
                row[8] = p.pred.target
            if p.is_couple:
                row[0] = str(p.ref.match_type(p.pred.type_))
                row[3] = str(relaxed_arg_similarity(p.ref.source, p.pred.source))
                row[6] = str(relaxed_arg_similarity(p.ref.target, p.pred.target))
            print('\t'.join([pair_label(p), str(p.value)] + row))
    except ZeroDivisionError:
        log(f'WARNING: nil R/P')
        print(0.0)
