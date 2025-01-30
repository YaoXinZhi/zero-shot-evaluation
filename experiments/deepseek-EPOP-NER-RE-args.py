# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 08/01/2024 20:04
@Author: yao
"""

import json
import os.path

from openai import OpenAI
import json

from datetime import datetime
import time

import argparse


def read_doc(sent_file: str):
    with open(sent_file) as f:
        sent = f.read().strip()
    # print(f'"{os.path.basename(sent_file)}": "{sent}".')
    return sent


def get_para():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='text_file',
                        default='/Users/yao/Nutstore Files/Mac2PC/LLM-EPOP-RE_BLAH9_2025-01-15/zero-shot-evaluation-main/experiments/documents/Texte2.txt')
    parser.add_argument('-p', dest='prompt_file',
                        default='/Users/yao/Nutstore Files/Mac2PC/LLM-EPOP-RE_BLAH9_2025-01-15/zero-shot-evaluation-main/experiments/instructions/short.txt')
    parser.add_argument('-s', dest='save_path',
                        default='/Users/yao/Nutstore Files/Mac2PC/LLM-EPOP-RE_BLAH9_2025-01-15/zero-shot-evaluation-main/experiments/output/repetition/kimi')
    args = parser.parse_args()

    return args


def main():
    # 官网说明 https://platform.openai.com/docs/api-reference/streaming
    # openai api 使用参考 https://zhuanlan.zhihu.com/p/656959227
    # Step-0 api
    # DeepSeek API 知乎
    api_key = '-'

    model = "deepseek-chat"

    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Step-1 data path.
    args = get_para()

    sent_file = args.text_file
    prompt_file = args.prompt_file
    save_path = args.save_path

    save_dir = os.path.basename(prompt_file).split('.')[ 0 ]
    text_prefix = os.path.basename(sent_file).split('.')[ 0 ]
    repeat_time = 5

    dir_path = f'{save_path}/{save_dir}/{text_prefix}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    print(f'---------model: {model}---------')

    # Step-2 Run: repeat time
    prompt = read_doc(prompt_file)
    sent = read_doc(sent_file)

    print(f'processing {os.path.basename(sent_file)} & {os.path.basename(prompt_file)}.')

    start_time = time.time()
    # moonshot api
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )
    for repeat in range(1, repeat_time + 1):

        print(f'repeating-{repeat}.')
        # save_file = f'{dir_path}/{repeat}.txt'
        save_file = os.path.join(dir_path, f'{repeat}.txt')
        if os.path.exists(save_file):
            print(f'"{save_file}" exists.')
            continue

        with open(save_file, 'w') as wf:
            stream = client.chat.completions.create(
                model=model,
                messages=[ {"role": "system",
                            "content": prompt},
                           {
                               "role": "user",
                               "content": sent,
                           } ],
                # from 0 to 1
                # temperature=0,
                # max_tokens=1,
                # only one response
                # n=1
            )

            result = stream.choices[ 0 ].message.content

            wf.write(f'{str(result)}\n\n')

        print(f'{save_file} saved.')
        # if repeat != repeat_time:
        time.sleep(30)
    end_time = time.time()
    print(f'time cost: {end_time - start_time:.4f}s.')


if __name__ == '__main__':
    main()
