# Machine Learning-Based Network Intrusion Detection

A reproducible, defensive cybersecurity research project that compares classical machine-learning baselines on the **official UNSW-NB15 train/test split**.

> **Research status:** first baseline experiment completed on the supplied UNSW-NB15 train/test files. Results are preliminary and dataset-specific; external validation has not yet been performed.

## Research question

How well do Logistic Regression and Random Forest distinguish normal from attack-labelled network flows on the official UNSW-NB15 test split, and how do their precision, recall, F1-score, ROC-AUC, and false-positive behaviour compare?

## Why UNSW-NB15?

The University of New South Wales publishes separate training and testing CSV files (175,341 and 82,332 records respectively) and documents nine attack categories. Using the published split avoids silently creating a new split and makes the baseline easier to reproduce. See the official [UNSW-NB15 dataset page](https://research.unsw.edu.au/projects/unsw-nb15-dataset).

This repository does **not** redistribute the dataset. Download it from the official source and follow its academic-use and citation conditions.

## Models

- **Logistic Regression** — interpretable linear baseline with class weighting.
- **Random Forest** — non-linear tree-ensemble baseline with class weighting.

Both models use the same preprocessing pipeline:
- numeric features: median imputation and standardisation;
- categorical features: most-frequent imputation and one-hot encoding;
- unknown categories in the test data are ignored safely.

The target is the binary `label` column (`0 = normal`, `1 = attack`). The target-derived `attack_cat` column and record identifier `id` are excluded from model inputs. Source/destination IP address columns, if present, are also excluded to reduce direct host-identity memorisation. All preprocessing is fitted on the training data only.

## 1. Environment

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## 2. Obtain the dataset

1. Open the [official UNSW-NB15 dataset page](https://research.unsw.edu.au/projects/unsw-nb15-dataset).
2. Download the provided training and testing CSV files:
   - `UNSW_NB15_training-set.csv`
   - `UNSW_NB15_testing-set.csv`
3. Place both files in `data/raw/`.

Expected layout:

```text
data/
└── raw/
    ├── UNSW_NB15_training-set.csv
    └── UNSW_NB15_testing-set.csv
```

The dataset is intentionally not committed to Git because of its size and source-specific usage conditions.

## 3. Inspect the data

```bash
python scripts/inspect_dataset.py --data-dir data/raw
```

Check the printed row counts, label distribution, missing-value counts, and duplicate counts before training.

## 4. Run the baseline experiments

```bash
python -m nids.train --data-dir data/raw --output-dir results
```

The command trains both models and writes one folder per model under `results/`, including:
- `metrics.json`
- `classification_report.json`
- `predictions.csv`
- `confusion_matrix.png`
- `roc_curve.png`
- `model.joblib`
- `feature_importance.csv` for Random Forest, when available.

Do not edit reported metrics manually. Keep the generated outputs together with the run configuration and dataset provenance.

## 5. Run tests

From the repository root:

```bash
python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
```

The tests use small synthetic fixtures only. Passing tests confirms code behaviour; it does **not** establish detection performance on UNSW-NB15.

## First baseline results

The first experiment used 175,341 training records and 82,332 test records from the supplied UNSW-NB15 split. The test split was not used for model tuning. See [`research/results_analysis.md`](research/results_analysis.md) and [`research/run_log_2026-11-11.md`](research/run_log_2026-11-11.md) for methodology, file hashes, metrics, confusion matrices, and limitations.

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Accuracy | 83.55% | 90.82% |
| Balanced accuracy | 82.48% | 90.13% |
| Attack F1-score | 86.17% | 92.08% |
| ROC-AUC | 95.60% | 98.44% |
| False-positive rate | 28.11% | 16.67% |

The Random Forest used 40 trees, maximum depth 16, and minimum leaf size 4. These results describe this benchmark split only; they do not establish real-world or production performance.

## Research workflow

1. Read `research/research_proposal.md`.
2. Follow `research/experiment_protocol.md` before running models.
3. Record dataset source, download date, file hashes, package versions, and exact command in `research/run_log_template.md`.
4. Run the experiment on the official split.
5. Analyse class-wise errors and false positives; do not report accuracy alone.
6. Complete `research/results_analysis_template.md` only after inspecting generated results.
7. Discuss limitations in `research/limitations.md`.

## Important research cautions

- The official split is used as supplied; do not tune model choices on the test set.
- The dataset is a benchmark, not a live enterprise network. Results do not prove real-world generalisation.
- The two models are baselines, not a novel algorithm.
- High scores can be misleading when classes are imbalanced or dataset artefacts are present.
- Report the confusion matrix, per-class precision/recall/F1, ROC-AUC, and false-positive rate.
- For stronger research, add repeated training-seed checks and an external-dataset evaluation (for example, a separately documented CIC-IDS2017 experiment) only after the baseline is complete.

## Project structure

```text
ml-network-intrusion-detection/
├── data/                 # dataset instructions; raw data is not committed
├── research/             # proposal, protocol, templates, limitations
├── scripts/              # dataset inspection utility
├── src/nids/              # reusable training and evaluation code
├── tests/                 # synthetic-data unit tests
├── .github/workflows/     # project CI
├── requirements.txt
└── pyproject.toml
```

## Dataset citation

Moustafa, N., & Slay, J. (2015). *UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set).* 2015 Military Communications and Information Systems Conference (MilCIS). IEEE.

See `research/references.md` for source and citation notes.

## Responsible use

This is an academic, defensive network-security project. Use only datasets and systems you are authorised to access. Do not use the code to monitor or inspect networks without permission.
