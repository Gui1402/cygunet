import unittest
from src.cygunet.datasets.cyimage import CygImage
from src.cygunet.pipelines.preprocessing.nodes import generate_event
import numpy as np

class TestNodes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Sets the random seed for numpy to ensure reproducibility of the
        random_translate method."""
        np.random.seed(0)
    
    def setUp(self):
        """Creates an instance of CygImage to be used in the test cases."""
        self.input_sim_dataset = [
            [
                CygImage(
                    np.array([[1, 2, 3], [3, 2, 1], [0, 1, 0]])
                ),
                CygImage(
                    np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                ),
                CygImage(
                    np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
                ),
            ],
            [
                CygImage(
                    np.array([[1, 2, 3], [3, 2, 1], [0, 1, 0]])
                ),
                CygImage(
                    np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                ),
                CygImage(
                    np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
                ),
            ]
        ]
        self.input_noise_dataset = [
            [
                CygImage(
                    np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                ),
                CygImage(
                    np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                ),
                CygImage(
                    np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                ),
            ],
            [
                CygImage(
                    np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                ),
                CygImage(
                    np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                ),
                CygImage(
                    np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                ),
            ]
        ]
    def test_acess_event(self):
        output_img = save_event(
            simulation_datasets=self.input_sim_dataset, 
            noise_datasets=self.input_noise_dataset,
            max_events=2,
            valid_indexes_list_sim=[0],
            valid_index_list_noise=[1]
        )
        assert output_img.sum() == 13