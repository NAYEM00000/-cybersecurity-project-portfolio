# External validation plan: CIC-IDS2017

## Purpose

Evaluate whether the intrusion-detection findings persist on a second, independently collected network-flow dataset. CIC-IDS2017 is a suitable next benchmark because it contains labelled benign and attack flows, CSV exports generated with CICFlowMeter, and multiple attack scenarios.

Official dataset page: https://www.unb.ca/cic/datasets/ids-2017.html

## What to download

Download the **MachineLearningCSV.zip** package only. The full PCAP collection is not required for this flow-feature experiment and is substantially larger.

Extract the CSV files under:

```text
data/
└── cicids2017/
    ├── Monday-WorkingHours.pcap_ISCX.csv
    ├── Tuesday-WorkingHours.pcap_ISCX.csv
    ├── Wednesday-workingHours.pcap_ISCX.csv
    ├── Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
    ├── Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
    ├── Friday-WorkingHours-Morning.pcap_ISCX.csv
    └── Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
```

The exact file names may vary slightly by archive version. Record the source, download date, hashes, and archive version.

## Feature mapping: do not assume columns are interchangeable

UNSW-NB15 and CIC-IDS2017 use different flow-generation tools and feature definitions. A transfer evaluation must map fields by documented meaning and units, not merely by similar names.

Candidate common concepts to investigate:

| Concept | UNSW-NB15 candidate | CIC-IDS2017 candidate | Validation needed |
|---|---|---|---|
| Flow duration | `dur` | `Flow Duration` | Confirm units and conversion |
| Forward packet count | `spkts` | `Total Fwd Packets` | Confirm direction convention |
| Backward packet count | `dpkts` | `Total Backward Packets` | Confirm direction convention |
| Forward bytes | `sbytes` | `Total Length of Fwd Packets` | Confirm byte-count definition |
| Backward bytes | `dbytes` | `Total Length of Bwd Packets` | Confirm byte-count definition |
| Protocol | `proto` | `Protocol` | Map protocol names to numeric IDs using a verified mapping |
| Flow rate | `rate` | `Flow Packets/s` or `Flow Bytes/s` | Confirm exact formula and units before using |

Do not use a candidate feature until its definition and unit have been checked against the dataset documentation or the original feature-extraction tool.

## Two distinct experiments

### A. Independent within-dataset benchmark

Train and evaluate the same baseline families separately on CIC-IDS2017 using a documented split strategy. This tests whether the model comparison pattern is also seen on another dataset, but it is not cross-dataset transfer.

### B. Cross-dataset transfer

After establishing a defensible common feature subset and unit conversions:
1. Train on UNSW-NB15 using only the common feature subset.
2. Freeze preprocessing and model parameters.
3. Evaluate on CIC-IDS2017 without fitting transformations on the CIC test records.
4. Report domain-shift effects and limitations.
5. Do not compare this restricted-feature transfer score directly with the full-feature UNSW score as if the feature sets were identical.

## Labels

Map CIC labels to a documented binary target:
- benign / normal -> 0
- attack -> 1

Keep original attack names for post-hoc per-category recall analysis. Remove label columns, flow IDs, source/destination IPs, timestamps, and other identifiers from model inputs unless a separately justified experiment explicitly studies them.

## Evaluation

Report accuracy, balanced accuracy, per-class precision/recall/F1, ROC-AUC, false-positive rate, confusion matrix, and category-specific recall. Include class counts and the split strategy.

## Citation

Cite the CIC-IDS2017 dataset paper:

Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization. *Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP)*.

The official dataset page provides the download and citation requirements. Check the current page before academic submission.
