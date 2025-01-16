#!/bin/env python


import ollama
import sys
import os.path
import os
import argparse
from openai import OpenAI
from datetime import datetime


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


log(f'reading instruction file: {args.instruction}')
with open(args.instruction) as f:
    inst = f.read()


log(f'reading document file: {args.document}')
with open(args.document) as f:
    doc = f.read()


def client_ollama(inst, doc, model):
    log(f'calling Ollama server')
    response = ollama.chat(
        model=model, stream=False, messages=
        [
         {
          'role': 'user',
          'content': inst,
          },
         {
          'role': 'user',
          'content': 'Message: ' + doc,
          },
        ],
    )
    return str(response['message']['content'])


def client_gpt(inst, doc, model):
    log(f'calling OpenAI server')
    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
             "role": "user",
            "content": inst + '\nMessage: ' + doc
            }
        ]
    )
    return completion.choices[0].message.content


if args.model.startswith('gpt'):
    answer = client_gpt(inst, doc, args.model)
else:
    answer = client_ollama(inst, doc, args.model)


log(f'writing result in {args.output}')
outdir = os.path.dirname(args.output)
if outdir != '':
    os.makedirs(outdir, exist_ok=True)
with open(args.output, 'w') as f:
    f.write(answer)


log('done')
