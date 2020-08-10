import numpy as np
import unittest
import os
from gradio import outputs
import json

PACKAGE_NAME = 'gradio'
BASE64_IMG = "data:image/jpeg;base64,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"

# Where to find the static resources associated with each template.
BASE_OUTPUT_INTERFACE_JS_PATH = 'static/js/interfaces/output/{}.js'

class TestLabel(unittest.TestCase):
    def test_postprocessing_string(self):
        string = 'happy'
        out = outputs.Label()
        label = out.postprocess(string)
        self.assertDictEqual(label, {outputs.Label.LABEL_KEY: string})

    def test_postprocessing_dict(self):
        orig_label = {
            3: 0.7,
            1: 0.2,
            0: 0.1
        }
        true_label = {outputs.Label.LABEL_KEY: 3,
                      outputs.Label.CONFIDENCES_KEY: [
                          {outputs.Label.LABEL_KEY: 3, outputs.Label.CONFIDENCE_KEY: 0.7},
                          {outputs.Label.LABEL_KEY: 1, outputs.Label.CONFIDENCE_KEY: 0.2},
                          {outputs.Label.LABEL_KEY: 0, outputs.Label.CONFIDENCE_KEY: 0.1},
                      ]}
        out = outputs.Label()
        label = out.postprocess(orig_label)
        self.assertDictEqual(label, true_label)

    def test_postprocessing_array(self):
        array = np.array([0.1, 0.2, 0, 0.7, 0])
        out = outputs.Label()
        self.assertRaises(ValueError, out.postprocess, array)

    def test_postprocessing_int(self):
        label = 3
        true_label = {outputs.Label.LABEL_KEY: '3'}
        out = outputs.Label()
        label = out.postprocess(label)
        self.assertDictEqual(label, true_label)


class TestTextbox(unittest.TestCase):
    def test_postprocessing(self):
        string = 'happy'
        out = outputs.Textbox()
        string = out.postprocess(string)
        self.assertEqual(string, string)


class TestImage(unittest.TestCase):
    def test_postprocessing(self):
        string = BASE64_IMG
        out = outputs.Textbox()
        string = out.postprocess(string)
        self.assertEqual(string, string)


if __name__ == '__main__':
    unittest.main()
