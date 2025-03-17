# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 13/03/2025 13:12
@Author: yao
"""

# 该代码用于统计EPOP数据集的entity，和relation的数量
import json
import re
import sys
from datetime import datetime
from evaluate.pairing import MunkresPairing, Pair
from evaluate.scoring import BaseScores, IEScores

import os
from icecream import ic

ic.disable()


def log(msg):
    now = datetime.now()
    sys.stderr.write(now.strftime('[%Y-%m-%d %H:%M:%S] ') + msg + '\n')


NORM_TYPES = ('NCBI_Taxonomy', 'GeoNames', 'OntoBiotope', 'name')

CODEBLOCK = re.compile('```json(.*)```', re.DOTALL)


def remove_codeblock(content):
    m = CODEBLOCK.search(content)
    if m is None:
        return content
    return m.group(1)


LAST_COMMA = re.compile(r',(?=\s*[\}\]])')


def remove_last_comma(content):
    return LAST_COMMA.sub('', content)


def squash_list(j):
    if isinstance(j, list):
        entities = [ ]
        relationships = [ ]
        for elt in j:
            entities.extend(elt.get('entities', [ ]))
            relationships.extend(elt.get('relationships', [ ]))
        return dict(entities=entities, relationships=relationships)
    return j


class Entity:
    def __init__(self, **args):
        self.id_ = args.get('id')
        self.type_ = args[ 'type' ]
        self.name = args[ 'name' ]
        for nt in NORM_TYPES:
            if nt in args:
                setattr(self, nt, args[ nt ])
                self.normalization_type = nt
                self.normalization_value = args[ nt ]
                break
        self.key = self.type_, self.normalization_type, self.normalization_value

    def __str__(self):
        return f'Entity({self.type_}, "{self.name}", {self.normalization_type}: {self.normalization_value})'

    def __repr__(self):
        return str(self)


class MergedEntity:
    QUOTES = set('"\'\u2018\u2019\u201c\u201d\u0060\u00b4')

    def __init__(self, ent):
        self.type_ = ent.type_
        self.ids = set((ent.id_,))
        self.names = set((ent.name,))
        self.normalization_type = ent.normalization_type
        self.normalization_value = ent.normalization_value
        setattr(self, ent.normalization_type, ent.normalization_value)
        self.key = ent.key

    def add(self, ent):
        self.ids.add(ent.id_)
        self.names.add(ent.name)

    def match_name(self, pred_name):
        if pred_name[ 0 ] in MergedEntity.QUOTES and pred_name[ -1 ] in MergedEntity.QUOTES:
            pred_name = pred_name[ 1:-1 ]
            # log(pred_name)
        pred_name = pred_name.lower()
        for name in self.names:
            if name.lower() == pred_name:
                return True
        return False

    def __str__(self):
        return f'MergedEntity({self.type_}, {self.ids}, {self.names}, {self.normalization_type}: {self.normalization_value})'

    def __repr__(self):
        return str(self)


class Relation:
    def __init__(self, **args):
        self.type_ = args[ 'type' ]
        if 'arguments' in args:
            self.arguments = args[ 'arguments' ]
        else:
            del args[ 'type' ]
            self.arguments = args
        self.source, self.target = self.arguments.values()

    def key(self, ent_id_map):
        argname1, argname2 = self.arguments
        arg1_type, arg1_nt, arg1_nv = ent_id_map[ self.arguments[ argname1 ] ].key
        arg2_type, arg2_nt, arg2_nv = ent_id_map[ self.arguments[ argname2 ] ].key
        return self.type_, argname1, arg1_type, arg1_nt, arg1_nv, arg2_type, arg2_nt, arg2_nv

    def __str__(self):
        return f'Relation({self.type_}, {", ".join((k + ": " + v) for k, v in self.arguments.items())})'

    def __repr__(self):
        return str(self)


class MergedRelation:
    JUNK_CHARS_IN_TYPE = re.compile(r'[\s_]+')

    def __init__(self, ent_id_map, rel):
        self.type_ = rel.type_
        self.arguments = dict((k, ent_id_map[ v ]) for k, v in rel.arguments.items())
        self.source, self.target = self.arguments.values()

    @staticmethod
    def _normalize_type(type_):
        nt = MergedRelation.JUNK_CHARS_IN_TYPE.sub('', type_).lower()
        return nt

    def match_type(self, pred_type):
        return MergedRelation._normalize_type(self.type_) == MergedRelation._normalize_type(pred_type)

    def __str__(self):
        return f'MergedRelation({self.type_}, {", ".join((k + ": " + str(v)) for k, v in self.arguments.items())})'

    def __repr__(self):
        return str(self)


class Dataset:
    def __init__(self, entities, relations):
        self.entities = entities
        self.relations = relations

    @staticmethod
    def from_json_file(filename):
        log(f'reading {filename}')
        try:
            with open(filename) as f:
                jc = f.read().strip()
        except FileNotFoundError:
            log('ERROR: file not found')
            exit(1)
        jc = remove_codeblock(jc)
        jc = remove_last_comma(jc)
        try:
            j = json.loads(jc)
        except json.decoder.JSONDecodeError:
            log('ERROR: malformed JSON')
            return Dataset([ ], [ ])
        j = squash_list(j)
        entities = list(Entity(**ent) for ent in j[ 'entities' ])
        relations = list(Relation(**rel) for rel in j[ 'relationships' ])
        if len(relations) == 0:
            log('WARNING: empty relations')
        return Dataset(entities, relations)

    def merge_ref(self):
        log('merging reference relations')
        entities = list(self._merge_ref_entities())
        relations = list(self._merge_ref_relations(entities))
        return MergedRefDataset(entities, relations)

    def _merge_ref_entities(self):
        ent_map = dict()
        for ent in self.entities:
            if ent.key in ent_map:
                ent_map[ ent.key ].add(ent)
            else:
                me = MergedEntity(ent)
                ent_map[ ent.key ] = me
                yield me

    def _merge_ref_relations(self, entities):
        ent_id_map = dict()
        for me in entities:
            for id_ in me.ids:
                ent_id_map[ id_ ] = me
        rel_map = set()
        for rel in self.relations:
            key = rel.key(ent_id_map)
            if key not in rel_map:
                rel_map.add(key)
                yield MergedRelation(ent_id_map, rel)

class MergedRefDataset(Dataset):
    def __init__(self, entities, relations):
        Dataset.__init__(self, entities, relations)

    def _map_name_to_entity(self, pred_ent):
        for ref_ent in self.entities:
            if ref_ent.match_name(pred_ent):
                return ref_ent
        return None

    def map_entities(self, pred):
        return dict((pred_ent, self._map_name_to_entity(pred_ent.name)) for pred_ent in pred.entities)

    @staticmethod
    def from_json_file(filename):
        return Dataset.from_json_file(filename).merge_ref()


def main():
    reference_path = '/Users/yao/Nutstore Files/Mac2PC/LLM-EPOP-RE_BLAH9_2025-01-15/data/EPOP from Robert - 2025 02 25/EPOP_json_new_format-25-03-07/dev'


    document_list = [file.split('.')[0] for file in os.listdir(reference_path) if file.endswith('.json')]

    save_path = '/Users/yao/Nutstore Files/Mac2PC/LLM-EPOP-RE_BLAH9_2025-01-15/zero-shot-evaluation-main/experiments/output/evaluation/main-experiment'

    save_file = f'{save_path}/entities_relation_statistics.EPOP.tsv'

    with open(save_file, 'w') as wf:
        wf.write(f'Documents\t# of Entities\t# of Relationships\n')
        for document_idx in document_list:

            ic(document_idx)
            reference_file = f'{reference_path}/{document_idx}.json'

            ref_ds = MergedRefDataset.from_json_file(reference_file)

            wf.write(f'{document_idx}\t{len(ref_ds.entities)}\t{len(ref_ds.relations)}\n')

    print(f'{save_file} saved.')

if __name__ == '__main__':
    main()


