#!/bin/env python


import ollama
import sys
import os.path
import os


_, output_dir, instruction_file, *doc_files = sys.argv


sys.stderr.write(f'reading instruction file: {instruction_file}\n')
with open(instruction_file) as f:
    instruction = f.read()
sys.stderr.write(f'  instruction: {instruction[:20]} ... {instruction[-20:]}\n')


os.makedirs(output_dir, exist_ok=True)
for docf in doc_files:
    sys.stderr.write(f'reading message: {docf}\n')
    with open(docf) as f:
        doc = f.read()
    sys.stderr.write('  prompting LLM\n')
    response = ollama.chat(
        model='mistral', stream=False, messages=
        [
         {
          'role': 'user',
          'content': instruction,
          },
         {
          'role': 'user',
          'content': 'Message: ' + doc,
          },
        ],
    )
    answer = str(response['message']['content'])
    basename = os.path.basename(docf)
    outf = os.path.join(output_dir, basename)
    sys.stderr.write(f'  writing result in {outf}\n')
    with open(outf, 'w') as f:
        f.write(answer)
