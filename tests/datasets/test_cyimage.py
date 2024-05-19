from src.cygunet.datasets.cyimage import CygImage
import unittest
import numpy as np


class TestCygImage(unittest.TestCase):
    """
    Unit tests for the CygImage class, which extends numpy.ndarray with additional image processing methods.

    Methods
    -------
    setUpClass():
        Sets up the class-level fixtures for the test cases.

    setUp():
        Sets up the individual fixtures for each test case.

    test_random_translate():
        Tests the random_translate method of the CygImage class.

    test_cut_edges():
        Tests the cut_edges method of the CygImage class.

    test_scale():
        Tests the scale method of the CygImage class.
    """

    @classmethod
    def setUpClass(cls):
        """Sets the random seed for numpy to ensure reproducibility of the random_translate method."""
        np.random.seed(0)

    def setUp(self):
        """Creates an instance of CygImage to be used in the test cases."""
        self.input_image = CygImage(
            np.array([[1, 2, 3], [3, 2, 1], [0, 1, 0]])
        )

    def test_random_translate(self):
        """Tests the random_translate method to ensure it translates the image and the output is different from the input."""
        translated_image = self.input_image.random_translate(2)
        self.assertNotEqual(
            self.input_image.tolist(), translated_image.tolist()
        )

    def test_cut_edges(self):
        """Tests the cut_edges method to ensure it correctly cuts the image to the specified bounding box."""
        cut_image = self.input_image.cut_edges(1, 2, 1, 2)
        self.assertEqual(cut_image.tolist(), [[2]])

    def test_scale(self):
        """Tests the scale method to ensure it correctly scales the image pixel values to the range [0, 1]."""
        scaled_image = self.input_image.scale(1, 2)
        self.assertEqual(
            scaled_image.tolist(),
            [[0.0, 1.0, 1.0], [1.0, 1.0, 0.0], [0.0, 0.0, 0.0]],
        )


if __name__ == "__main__":
    unittest.main()
