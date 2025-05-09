#!/bin/env python
 
 
import sys
import re
from bionlpst.model import Corpus, Location
import collections


_, ABSTRACTS_FILE, ENTITIES_FILE, RELATIONS_FILE, OUT_DIR = sys.argv


corpus = Corpus()


sys.stderr.write(f'Reading abstracts {ABSTRACTS_FILE}\n')
with open(ABSTRACTS_FILE) as f:
    for line in f:
        docid, title, abstract = line.strip().split('\t')
        corpus.new_document(ABSTRACTS_FILE, docid, title + '\n' + abstract)


sys.stderr.write(f'Reading entities {ENTITIES_FILE}\n')
ENTITIES = collections.defaultdict(list)
with open(ENTITIES_FILE) as f:
    for no, line in enumerate(f, 1):
        docid, tid, type_, start, end, form = line.strip().split('\t')
        ENTITIES[docid].append((int(start), int(end), tid, type_, form, no))


sys.stderr.write('Raligning entities\n')
n_entities = 0
n_odd_offsets = 0
for doc in corpus.documents:
    prev_th_start = -1
    offset = 0
    for th_start, th_end, tid, type_, form, no in sorted(ENTITIES[doc.docid]):
        if th_start == prev_th_start:
            offset -= 1
        try:
            start = doc.text.index(form, offset)
        except ValueError:
            sys.stderr.write(f'Cannot find "{form}" in "{doc.text[offset:]}" ({doc.docid}, {offset})\n')
            raise
        end = start + len(form)
        loc = Location(ENTITIES_FILE, no)
        e = doc.reference.new_text_bound(type_, ((start, end),), location=loc, id_=tid)
        norm = re.sub('\\W', '', form.lower())
        doc.reference.new_normalization('Name', norm, annotation=e, location=loc)
        if start != th_start or end != th_end:
            n_odd_offsets += 1
            # sys.stderr.write(f'Odd offset\t{doc.docid}\t{form}\t{th_start}-{th_end}\t{start}-{end}\n')
        n_entities += 1
        offset = start + 1
        prev_th_start = th_start
sys.stderr.write(f'Parsed {n_entities} entities, {n_odd_offsets} odd offsets\n')


sys.stderr.write(f'Reading relations {RELATIONS_FILE}\n')
n_relations = 0
with open(RELATIONS_FILE) as f:
    for no, line in enumerate(f, 1):
        docid, type_, arg1, arg2 = line.strip().split('\t')
        doc = corpus.get_document(docid)
        arg1_ent = doc.reference.get_annotation(arg1[5:])
        assert arg1_ent is not None
        arg2_ent = doc.reference.get_annotation(arg2[5:])
        assert arg2_ent is not None
        doc.reference.new_relation(type_, arguments=(('Arg1', arg1_ent), ('Arg2', arg2_ent)), location=Location(RELATIONS_FILE, no))
        n_relations += 1
sys.stderr.write(f'Parsed {n_relations} relations\n')


sys.stderr.write(f'Writing BioNLP-ST files in {OUT_DIR}\n')
corpus.write(text_dir=OUT_DIR, input_dir=OUT_DIR, reference_dir=OUT_DIR)
