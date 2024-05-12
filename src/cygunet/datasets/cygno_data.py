from pathlib import Path
from kedro.io import AbstractDataset
import h5py
import pandas as pd
from typing import Union
import uproot


class LazyROOTData:
    def __init__(self, file, keys):
        """
        Initializes the LazyROOTData with the path to the ROOT file.

        Parameters:
            file_path (str): Path to the ROOT file.
        """
        self._file = file
        self.keys = keys
    
    def __getattr__(self, name: str):
        """
        Enables lazy, attribute-style access to the ROOT file's trees.

        Parameters:
            name (str): Name of the branch or tree to access.

        Returns:
            The object (tree, branch, etc.) associated with 'name' if it exists.

        Raises:
            AttributeError: If the attribute does not exist in the ROOT file.
        """
        try:
            return self._file[name].to_numpy()[0]
        except KeyError:
            raise AttributeError(f"{name} not found in ROOT file.")

    def __getitem__(self, index):
        return self._file[self.keys[index]].to_numpy()[0]


class HDF5GroupWrapper:
    """
    A wrapper for HDF5 file groups and datasets to facilitate attribute and item access.
    
    Attributes:
        group (h5py.Group or h5py.Dataset): The underlying HDF5 group or dataset.
        keys (List[str]): A list of keys from the parent HDF5 file.
    """

    def __init__(self, group: h5py.Group, keys: list):
        """
        Initializes the HDF5GroupWrapper with an HDF5 group and its keys.
        
        Parameters:
            group (h5py.Group): The HDF5 group or dataset to wrap.
            keys (List[str]): Keys from the parent HDF5 file.
        """
        self.group = group
        self.keys = keys

    def __getattr__(self, name: str):
        """
        Allows dot-access to HDF5 datasets or groups within the file.
        
        Parameters:
            name (str): The name of the dataset or group to access.
        
        Returns:
            HDF5GroupWrapper: A new wrapper for the requested dataset or group.
        
        Raises:
            AttributeError: If the specified name is not a key in the group.
        """
        try:
            return HDF5GroupWrapper(self.group[name], self.keys)[:]
        except KeyError:
            raise AttributeError(f"No such group or dataset: {name}")

    def __getitem__(self, key: Union[str, int]):
        """
        Allows dictionary-style or list-style access to datasets or groups within the HDF5 file.

        Parameters:
            key (Union[str, int]): The key or index of the dataset or group to access.
        
        Returns:
            Any: The dataset or group corresponding to the key.

        Raises:
            ValueError: If the key is neither an integer nor a string.
        """
        if isinstance(key, str):
            return self.group[key][:]
        elif isinstance(key, int):
            return self.group[self.keys[key]][:]
        else:
            raise ValueError("Key must be integer or string")

    def __repr__(self) -> str:
        """
        Returns a string representation of the underlying HDF5 group or dataset.
        
        Returns:
            str: The string representation of the HDF5 group.
        """
        return repr(self.group)

    def __len__(self) -> int:
        """
        Returns the number of keys in the group.
        
        Returns:
            int: The number of keys.
        """
        return len(self.keys)


class CygnoSimulationImage(AbstractDataset[pd.DataFrame, pd.DataFrame]):
    """
    A Kedro dataset for managing simulation images stored in HDF5 format.
    """

    def __init__(self, filepath: str):
        """
        Initializes the dataset with the path to the HDF5 file.
        
        Parameters:
            filepath (str): The file path to the HDF5 dataset.
        """
        self._filepath = Path(filepath)
        self._keys = None

    def get_keys(self) -> None:
        """
        Retrieves and stores the list of top-level keys from the HDF5 file.
        """
        with h5py.File(self._filepath, 'r') as file:
            self._keys = list(file.keys())
            
    def _load(self) -> HDF5GroupWrapper:
        """
        Loads the HDF5 file, wraps it in an HDF5GroupWrapper, and returns the wrapper.
        
        Returns:
            HDF5GroupWrapper: A wrapped HDF5 file ready for data interaction.
        """
        self.get_keys()
        file = h5py.File(self._filepath, 'r')
        return HDF5GroupWrapper(file, self._keys)

    def _save(self, wrapper: HDF5GroupWrapper) -> None:
        """
        Placeholder function to save any changes back to the HDF5 file. Currently does nothing.
        
        Parameters:
            wrapper (HDF5GroupWrapper): The wrapper around the HDF5 file.
        """
        pass

    def _exists(self) -> bool:
        """
        Checks if the HDF5 file exists at the specified path.
        
        Returns:
            bool: True if the file exists, otherwise False.
        """
        return self._filepath.exists()

    def _describe(self) -> dict:
        """
        Provides a basic description of the dataset.
        
        Returns:
            dict: An empty dictionary as a placeholder for dataset description.
        """
        return dict()


class CygnoNoiseImage(AbstractDataset[pd.DataFrame, pd.DataFrame]):
    """
    A Kedro dataset for managing noise images stored in .root format.
    """

    def __init__(self, filepath: str):
        """
        Initializes the dataset with the path to the HDF5 file.
        
        Parameters:
            filepath (str): The file path to the HDF5 dataset.
        """
        self._filepath = Path(filepath)
        self._keys = None

    def get_keys(self) -> None:
        """
        Retrieves and stores the list of top-level keys from the HDF5 file.
        """
        with uproot.open(self._filepath) as file:
            self._keys = list(file.keys())
            
    def _load(self) -> LazyROOTData:
        """
        Loads the root file, wraps it in an LazyROOTData, and returns the wrapper.
        
        Returns:
            LazyROOTData: A wrapped root file ready for data interaction.
        """
        self.get_keys()
        file = uproot.open(self._filepath)
        return LazyROOTData(file, self._keys)

    def _save(self, wrapper: LazyROOTData) -> None:
        """
        Placeholder function to save any changes back to the HDF5 file. Currently does nothing.
        
        Parameters:
            wrapper (HDF5GroupWrapper): The wrapper around the HDF5 file.
        """
        pass

    def _exists(self) -> bool:
        """
        Checks if the HDF5 file exists at the specified path.
        
        Returns:
            bool: True if the file exists, otherwise False.
        """
        return self._filepath.exists()

    def _describe(self) -> dict:
        """
        Provides a basic description of the dataset.
        
        Returns:
            dict: An empty dictionary as a placeholder for dataset description.
        """
        return dict()
