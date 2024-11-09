# Accuracy assessment through consistency metrics

## Zero-shot evaluation experiment in the plant health domain

# Objectives

This project aims at evaluating LLM-based generative agents for Information Extraction (IE) tasks in a zero/one-shot evaluation setting, that is without reference data. We will explore consistency metrics and their dependency to accuracy metrics. We will work on a corpus in the domain of plant health.

LLMs appear to yield good results in zero-shot learning settings. However the evaluation with traditional metrics (Recall/Precision/F-score) requires reference data, which are absent or scarce. We plan to explore alternate indicators for the quality of LLM-based IE, in particular consistency metrics. Consistency metrics measure the stability of extractions from one run to another, rather than the accuracy of extractions that require reference annotations. While accuracy on benchmarks is valuable, consistency metrics become crucial during inference, where the system is applied to vast, diverse datasets. Consistency measures help ensure stability and reliability at scale, addressing potential variations and reducing erratic outputs that accuracy alone may not capture. They also help to measure if the model maintains coherence and reduces drift when encountering varied contexts. Consistency measures are essential for robust extraction in real-world applications.

Generative models sometimes hallucinate information, especially when their outputs are influenced by randomness, e.g., temperature setting in language models as explored by the authors. Consistency over runs can help in detecting and controlling hallucinations. If different runs produce significantly varied outputs, this could indicate hallucination, prompting further tuning or constraints on generation.

We actually have a reference annotation at disposal called Epidemiomonitoring Of Plant (EPOP) that we will exploit to study the relationship between consistency and accuracy and their complementarity.

# Dataset

The Epidemiomonitoring Of Plant (EPOP) dataset consists of 247 documents (\>100k tokens) gathered by the *Plateforme d’Épidémiologie Végétale* (PESV), a unit in charge of monitoring media and scientific publications for crop outbreaks. The documents are collected from the web targeting a list of harmful organisms under close surveillance. PESV gathers and examines approximately a thousand documents each week, these documents are originally in several languages and automatically translated so that PESV’s operators can read them.

The EPOP 247 documents were drawn randomly from this collection, but biased in order to cover a wide range of targeted organisms and of document types. The documents have been annotated by a team of 31 plant health experts in double-blind fashion and adjudicated, then the annotation was revised by a team of four NLP experts.

The annotation contains named entities of 7 types (Date, Disease, Dissemination\_pathway, Location, Pest, Plant, Vector), binary relations of 7 types (Causes, Detected\_at, Dispersed\_by, Localized\_in, Expressed\_on, Found\_on, Vected\_by), and n-ary relations. The EPOP corpus has been split into training development and test subsets.

For this project, we will have at disposal 30 thousand documents gathered for one year to conduct consistency experiments. The annotated training and development subsets of EPOP corpus allow to compare the consistency analysis with the accuracy measure.

# Work plan

We plan to assess the consistency of LLM-based extraction through (1) several runs, (2) the comparison of results obtained from a pair of close input documents, or from a single document in distinct runs \[Hu et al., 2024\]. The difference in the results will indicate at which point the answer results from a stable representation of the task or not. Before BLAH9, we will have studied the bibliography on consistency to identify consistency measure candidates. For practical experimentation, we will call a document either a full document or a subpart (paragraph or sentence).

## **Document pairs**

We will explore different strategies for obtaining close document pairs, in order to highlight the consistency in different situations \[Elazar et al., 2021\].

### Plagiarism detection metrics

Search in a large collection for similar documents using plagiarism detection metrics \[e.g. Broder, 1997\]. We assume that similar documents yield similar extracted information. For instance:

### Introduce noise

Extract information from a document, then from a noised version of the same document, by randomly replacing, deleting, or inserting characters or words. This will indicate the robustness to noisy input. 

### Generative reformulation

Ask for a generative LLM to reformulate the document, then compare extractions from the original and reformulated documents. This will indicate the impact of differences in formulation and language range.

### Named-entity substitution

Replace all occurrences of a named entity with another one from the same type, then compare extractions from the original document and the doctored document. This will indicate the influence of the latent background knowledge contained in the LLM.

### Translated pairs

Since documents are translated from a diverse set of languages, we can compare the extracted information from the document in its original language and from the document translated to English. This requires that the LLM has been trained with multilingual data \[Fierro and Søgaard, 2022\].

## **Metrics**

For comparing the extractions obtained from document pairs, we will use IE metrics (Recall, Precision, F-score). Because none of the documents and extractions are gold-standard, these metric values will not indicate accuracy but consistency.

For comparing consistency and accuracy, one of the documents must be part of the EPOP in order to have the gold standard annotation at disposal. In this way we can compare the consistency metric value with the accuracy of each extraction with the gold standard.

## **Calibration of document pairs**

If we detect a correlation between consistency and accuracy, then we intend to quantify the effect of the closeness on the consistency. We will plot a range of document “closeness” (e.g. increasing the noise, or increasing the plagiarism threshold) against the consistency and accuracy values. In this way we may find the optimal target “closedness” for which the accuracy is a reliable indicator of accuracy.

Once the similarity criteria and consistency metrics are defined, we will explore whether information extraction from pairs of close unseen documents produces results comparable to the previous setting.

From the experiments with this large document set, we seek to understand the factors that can explain \[un\]stability of results, such as the complexity of the task or the length of the output text  \[Attil et al., 2024\]

# Experiment overview

# We are looking for

- Expertise on instruction design, in particular for Information Extraction tasks in biology.  
- General expertise on LLM usage: choice of LLM, choice of output format.  
- Ideas for finding or generating close document pairs.  
- Ideas for alternative consistency assessment methods.

# Data and code availability

- The EPOP dataset will be publicly available at the time of BLAH9 along with the annotation guidelines.  
- The year archive of PESV will be available for participants at the time of BLAH9.  
- All code produced during BLAH9 will be released under an open source license.

# References

Atil, B., Chittams, A., Fu, L., Ture, F., Xu, L., & Baldwin, B. (2024). LLM Stability: A detailed analysis with some surprises. arXiv preprint arXiv:2408.04667.

A. Z. Broder, "On the resemblance and containment of documents," Proceedings. Compression and Complexity of SEQUENCES 1997 (Cat. No.97TB100171), Salerno, Italy, 1997, pp. 21-29, doi: 10.1109/SEQUEN.1997.666900.

Yanai Elazar, Nora Kassner, Shauli Ravfogel, Abhilasha Ravichander, Eduard Hovy, Hinrich Schütze, and Yoav Goldberg. 2021\. Measuring and Improving Consistency in Pretrained Language Models. Transactions of the Association for Computational Linguistics, 9:1012–1031.

Constanza Fierro and Anders Søgaard. 2022\. Factual Consistency of Multilingual Pretrained Language Models. In Findings of the Association for Computational Linguistics: ACL 2022, pages 3046–3052, Dublin, Ireland. Association for Computational Linguistics.

Hu D, Liu B, Zhu X, Lu X, Wu N. Zero-shot information extraction from radiological reports using ChatGPT. Int J Med Inform. 2024 Mar;183:105321. doi: 10.1016/j.ijmedinf.2023.105321. Epub 2023 Dec 21\. PMID: 38157785\.