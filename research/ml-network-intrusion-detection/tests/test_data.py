import unittest
import pandas as pd

from nids.data import split_features_target, normalise_columns


class DataPreparationTests(unittest.TestCase):
    def test_normalises_bom_and_whitespace(self):
        frame = pd.DataFrame([[1, 0]], columns=["\ufeff label ", " feature "])
        result = normalise_columns(frame)
        self.assertEqual(list(result.columns), ["label", "feature"])

    def test_drops_target_attack_category_and_identifier(self):
        frame = pd.DataFrame({
            "id": [1, 2, 3, 4],
            "srcip": ["a", "b", "c", "d"],
            "attack_cat": ["Normal", "DoS", "Normal", "Fuzzers"],
            "feature": [0.1, 0.2, 0.3, 0.4],
            "label": [0, 1, 0, 1],
        })
        X, y = split_features_target(frame)
        self.assertEqual(list(X.columns), ["feature"])
        self.assertEqual(y.tolist(), [0, 1, 0, 1])

    def test_rejects_missing_target(self):
        with self.assertRaisesRegex(ValueError, "label"):
            split_features_target(pd.DataFrame({"feature": [1, 2]}))

    def test_rejects_non_binary_target(self):
        with self.assertRaisesRegex(ValueError, "binary"):
            split_features_target(pd.DataFrame({"feature": [1, 2], "label": [0, 2]}))


if __name__ == "__main__":
    unittest.main()
