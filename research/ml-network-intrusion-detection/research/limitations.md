# Limitations and threats to validity

1. **Benchmark age and representativeness:** UNSW-NB15 is a research benchmark, not a current live enterprise network. Results may not transfer to modern environments.
2. **Synthetic attack generation:** The dataset contains generated attack behaviours and a specific capture environment. This can create dataset-specific patterns.
3. **Binary target simplification:** Combining attack categories into one class hides differences between attack families and their operational severity.
4. **Class imbalance:** Aggregate accuracy can obscure minority-class errors. Class-wise metrics and confusion matrices are required.
5. **Potential dataset artefacts:** Features may encode characteristics of the collection setup. Strong performance is not automatically evidence of generalisable detection.
6. **Baseline scope:** Logistic Regression and Random Forest are conventional baselines. This project does not introduce a novel model.
7. **No live deployment:** The code trains and evaluates on offline CSV flow records. It is not a production network sensor or real-time prevention system.
8. **External validity:** The first phase uses one dataset. A separate, predeclared external evaluation is needed before making broader claims.
9. **Feature importance caveat:** Tree-based feature importance can be biased toward certain feature types and should not be interpreted as causal explanation.

These limitations must be discussed in any report or presentation based on this work.
