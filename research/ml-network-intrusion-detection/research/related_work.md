# Related work and literature notes

## Dataset paper

Moustafa and Slay introduced UNSW-NB15 as a network intrusion detection dataset containing normal activity and multiple contemporary attack behaviours. The official UNSW project page describes the data-generation environment, 49 derived features, attack categories, and the supplied train/test files.

This project uses the official binary `label` for the first-stage task. The `attack_cat` field is not used as a model input.

## Dataset provenance

The authoritative source for downloading the dataset and checking its use/citation requirements is the [UNSW Research dataset page](https://research.unsw.edu.au/projects/unsw-nb15-dataset).

## Research gap addressed by this project

This is a small, reproducible baseline exercise, not a claim that the field lacks intrusion-detection models. Its focus is transparent preprocessing and evaluation discipline: a fixed split, train-only transformations, class-sensitive metrics, and explicit limitations.

## Reading questions

When reviewing additional papers, record:

1. Which dataset and exact version were used?
2. Was the split random, chronological, or supplied by the dataset authors?
3. Were any identifiers or target-derived fields removed?
4. Was preprocessing fitted only on training data?
5. Were class imbalance and false positives discussed?
6. Was evaluation performed on an independent dataset?
7. Are the code, data provenance, and experimental settings reproducible?

Add papers only after reading them. Do not copy claims from abstracts without checking the methods and limitations.
