# Experiments

## Directories

- `documents/`: documents of varying complexity. Text files (UTF-8).
- `instructions/`:
  - `ner+rel.txt`: original NER and RE instruction, the concatenation of three prompts
  - `scenario.txt`: extended and streamlined version
  - `short.txt`: minimal version of the same prompt
- `output/`: result of experiments


## Repetition

The repetition experiment aims at assessing how much the output varies for the same pair of instruction/document.

The experiment has been conducted on three models (`mistral`, `gpt-4o-mini`, `kimi`), three instructions (`ner+rel`, `scenario`, `short`), and three documents (`Texte2`, `Texte5`, `Texte10`).
Each prompt has been repeated five times.

The result of the experiment is contained in `output/repetition/`.
The results have been organized in a folder tree of three levels corresponding to the model, the instruction and the document.
Each terminal folder contains five files numbered 1 to 5.

Thus each output file has the following path:

```
output/repetition/MODEL/PROMPT/DOC/N.txt
```
