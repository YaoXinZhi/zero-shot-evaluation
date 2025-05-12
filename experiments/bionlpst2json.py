#!/bin/env python


import json
import sys
import bionlpst.parser
import bionlpst.model
import os
import os.path
from collections.abc import Iterator


_, TYPEMAP_FILE, TEXTDIR, REFDIR, OUTDIR = sys.argv


with open(TYPEMAP_FILE) as f:
    TYPEMAP = json.load(f)


parser = bionlpst.parser.BioNLPSTParser(form_check='no_check')
parser.parse_text(TEXTDIR)
parser.parse_input(REFDIR)
parser.parse_reference(REFDIR)
parser.resolve_annotation_references()


def doc2layout(doc: bionlpst.model.Document) -> Iterator[dict]:
    for tag in doc.input.text_bounds():
        yield dict(id=tag.id_, tag=tag.type_, offset=tag.fragments[0])


def doc2entities(doc: bionlpst.model.Document) -> Iterator[dict]:
    for ent in doc.reference.text_bounds():
        if ent.type_ in TYPEMAP['entities']:
            type_ = TYPEMAP['entities'][ent.type_]
            result = dict(id=ent.id_, type=type_, name=ent.form)
            for norm in ent.back_references(bionlpst.model.Normalization):
                ntype = TYPEMAP['normalizations'].get(norm.type_, norm.type_)
                result[ntype] = norm.referent
            yield result


def doc2equivalences(doc: bionlpst.model.Document) -> Iterator[list[str]]:
    for eq in doc.reference.equivalences:
        yield [a.id_ for a in eq.annotations]


def doc2binrel(doc: bionlpst.model.Document) -> Iterator[dict]:
    aset = doc.reference
    for rel in aset.relations():
        if rel.type_ in TYPEMAP['relations']:
            relinfo = TYPEMAP['relations'][rel.type_]
            type_ = relinfo['type']
            source = rel.arguments[relinfo['source']].id_
            target = rel.arguments[relinfo['target']].id_
            if aset.get_annotation(source).type_ in TYPEMAP['entities'] and aset.get_annotation(target).type_ in TYPEMAP['entities']:
                yield dict(type=type_, source=source, target=target)


os.makedirs(OUTDIR, exist_ok=True)
for doc in parser.corpus.documents:
    j = dict(entities=list(doc2entities(doc)), equivalences=list(doc2equivalences(doc)), relationships=list(doc2binrel(doc)))
    filename = os.path.join(OUTDIR, doc.docid + '.json')
    with open(filename, 'w') as f:
        json.dump(j, f, indent=4)
