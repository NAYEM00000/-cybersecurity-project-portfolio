import unittest
import pandas as pd

from nids.models import build_pipeline


class ModelPipelineTests(unittest.TestCase):
    def test_logistic_pipeline_fits_mixed_features(self):
        X = pd.DataFrame({
            "duration": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            "protocol": ["tcp", "udp", "tcp", "udp", "tcp", "udp", "tcp", "udp"],
        })
        y = [0, 0, 0, 0, 1, 1, 1, 1]
        model = build_pipeline("logistic_regression")
        model.fit(X, y)
        self.assertEqual(model.predict(X).shape[0], len(y))
        self.assertEqual(model.predict_proba(X).shape, (len(y), 2))

    def test_rejects_unknown_model(self):
        with self.assertRaises(ValueError):
            build_pipeline("not-a-model")


if __name__ == "__main__":
    unittest.main()
