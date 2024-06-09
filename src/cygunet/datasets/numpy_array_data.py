import numpy as np
from kedro.io import AbstractDataset
from kedro.io.core import get_filepath_str, get_protocol_and_path
from pathlib import Path
import logging
import pandas as pd
import os 

class NumpyArrayDataset(AbstractDataset[np.ndarray, np.ndarray]):
    def __init__(self, filepath, load_args=None, save_args=None):
        """Create a new instance of NumpyArrayDataset to work with NumPy arrays.
        
        Args:
            filepath (str): Path to a .npy file.
            load_args (dict, optional): Arguments passed on to `numpy.load`.
            save_args (dict, optional): Arguments passed on to `numpy.save`.
        """
        self._filepath = Path(filepath)
        self._load_args = load_args if load_args else {}
        self._save_args = save_args if save_args else {}

    def _load(self):
        """Load a numpy array from a .npy file.
        
        Returns:
            numpy.ndarray: Loaded array.
        """
        load_path = get_filepath_str(self._filepath, None)
        return np.load(load_path, **self._load_args)

    def _save(self, data):
        """Save a numpy array to a .npy file.
        
        Args:
            data (numpy.ndarray): Data to save.
        """
        save_path = get_filepath_str(self._filepath, None)
        parent_path = str(self._filepath.parents[0])
        os.makedirs(parent_path, exist_ok=True)
        np.save(save_path, data, **self._save_args)
        self._filepath.touch()

    def _describe(self):
        """Return a dict that describes the attributes of the dataset."""
        return dict(filepath=self._filepath, load_args=self._load_args, save_args=self._save_args)
