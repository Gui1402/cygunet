from pathlib import Path
from typing import Any, List, Union
from glob import glob
import h5py
import pandas as pd
import uproot
from kedro.io import AbstractDataset
import re
from .cyimage import CygImage


class LazyROOTData:
    """Provides lazy access to ROOT file data."""

    def __init__(self, file, keys: List[str]):
        """Initialize the LazyROOTData with the path to the ROOT file.

        Parameters:
            file (str): Path to the ROOT file.
            keys (List[str]): List of keys in the ROOT file.
        """
        self._file = file
        self.keys = keys

    def __getattr__(self, name: str):
        """Provide lazy, attribute-style access to the ROOT file's trees.

        Parameters:
            name (str): Name of the branch or tree to access.

        Returns:
            The object (tree, branch, etc.) associated with 'name' if it exists.

        Raises:
            AttributeError: If the attribute does not exist in the ROOT file.
        """
        try:
            return CygImage(self._file[name].to_numpy()[0])
        except KeyError:
            raise AttributeError(f"{name} not found in ROOT file.")

    def __getitem__(self, index):
        """Get item by index."""
        return CygImage(self._file[self.keys[index]].to_numpy()[0])

    def close(self):
        """_summary_

        Raises:
            AttributeError: _description_
            ValueError: _description_
            AttributeError: _description_
            AttributeError: _description_
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        self._file.close()


class HDF5GroupWrapper:
    """Wrapper for HDF5 file groups and datasets to facilitate attribute and
    item access.

    Attributes:
        group (h5py.Group or h5py.Dataset): The underlying HDF5 group or dataset.
        keys (List[str]): A list of keys from the parent HDF5 file.
    """

    def __init__(self, group: h5py.Group, keys: List[str], path):
        """Initialize the HDF5GroupWrapper with an HDF5 group and its keys.

        Parameters:
            group (h5py.Group): The HDF5 group or dataset to wrap.
            keys (List[str]): Keys from the parent HDF5 file.
        """
        self.group = group
        self.keys = keys
        self.path = str(path)

    def __getattr__(self, name: str):
        """Allow dot-access to HDF5 datasets or groups within the file.

        Parameters:
            name (str): The name of the dataset or group to access.

        Returns:
            HDF5GroupWrapper: A new wrapper for the requested dataset or group.

        Raises:
            AttributeError: If the specified name is not a key in the group.
        """
        try:
            return HDF5GroupWrapper(self.group[name], self.keys)
        except KeyError:
            raise AttributeError(f"No such group or dataset: {name}")

    def __getitem__(self, key: Union[str, int]):
        """Allow dictionary-style or list-style access to datasets or groups
        within the HDF5 file.

        Parameters:
            key (Union[str, int]): The key or index of the dataset or group to access.

        Returns:
            Any: The dataset or group corresponding to the key.

        Raises:
            ValueError: If the key is neither an integer nor a string.
        """
        if isinstance(key, str):
            return CygImage(self.group[key][:])
        elif isinstance(key, int):
            return CygImage(self.group[self.keys[key]][:])
        else:
            raise ValueError("Key must be integer or string")

    def __repr__(self) -> str:
        """Return a string representation of the underlying HDF5 group or
        dataset.

        Returns:
            str: The string representation of the HDF5 group.
        """
        return repr(self.group)

    def __len__(self) -> int:
        """Return the number of keys in the group.

        Returns:
            int: The number of keys.
        """
        return len(self.keys)

    def close(self):
        """_summary_

        Raises:
            AttributeError: _description_
            ValueError: _description_
            AttributeError: _description_
            AttributeError: _description_
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        self.group.close()


class SuperH5GroupWrapper:
    """
    A class to dynamically manage multiple HDF5GroupWrapper instances, with each
    instance being accessible as an attribute named after the file path.

    Attributes:
        paths (List[str]): List of file paths for which HDF5GroupWrapper instances are created.
    """

    def __init__(self, paths: List[str], pattern=r'(ER|NR)_(.*?)_keV'):
        """
        Initializes the NewClass with a list of file paths.

        Parameters:
            paths (List[str]): List of file paths.
        """
        self._paths = paths
        self._pattern = pattern.replace("\\", "")
        compiler = re.compile(self._pattern)
        self._alias = {}
        for p in paths:
            try:
                a = f"{re.search(compiler, p).group(1)}_{re.search(compiler, p).group(2)}"
                self._alias[a.lower()] = p
            except:
                pass
        self._wrappers = {}  # Cache for already created wrappers
        self.keys = list(self._alias.keys())

    def __getattr__(self, name: str):
        """
        Dynamically create or retrieve a HDF5GroupWrapper for the requested file path.

        Parameters:
            name (str): The attribute name which corresponds to a file path.

        Returns:
            HDF5GroupWrapper: The HDF5GroupWrapper instance for the given file path.

        Raises:
            AttributeError: If the name does not correspond to a file path in the initial list.
        """
        if name in self._alias:
            if name not in self._wrappers:
                h5file = h5py.File(self._alias[name], 'r')
                keys = list(h5file.keys())
                self._wrappers[name] = HDF5GroupWrapper(h5file, keys, self._alias[name])         
            return self._wrappers[name]
        else:
            raise AttributeError(f"{name} is not a valid path")

    def __repr__(self):
        """
        String representation of the SuperH5GroupWrapper, listing all managed paths.
        """
        return f"Cygno Simulation Dataset managing paths: {self._alias}"


class SuperROOTGroupWrapper:
    """
    A class to dynamically manage multiple LazyROOTData instances, with each
    instance being accessible as an attribute named after the file path.

    Attributes:
        paths (List[str]): List of file paths for which LazyROOTData instances are created.
    """

    def __init__(self, paths: List[str], pattern=r'.*/01_raw/(fusion|quest)/.*\.root$'):
        """
        Initializes the NewClass with a list of file paths.

        Parameters:
            paths (List[str]): List of file paths.
        """
        self._paths = paths
        self._pattern = pattern.replace("\\", "")
        compiler = re.compile(self._pattern)
        self._alias = {}
        for p in paths:
            if re.match(compiler, p):
                a = p.split("/")[-1].replace(".root", "").replace("histograms_", "")
                self._alias[a.lower()] = p
        self._wrappers = {}  # Cache for already created wrappers
        self.keys = list(self._alias.keys())

    def __getattr__(self, name: str):
        """
        Dynamically create or retrieve a LazyROOTData for the requested file path.

        Parameters:
            name (str): The attribute name which corresponds to a file path.

        Returns:
            HDF5GroupWrapper: The HDF5GroupWrapper instance for the given file path.

        Raises:
            AttributeError: If the name does not correspond to a file path in the initial list.
        """
        if name in self._alias:
            if name not in self._wrappers:
                rfile = uproot.open(self._alias[name])
                keys = list(rfile.keys())
                self._wrappers[name] = LazyROOTData(rfile, keys)         
            return self._wrappers[name]
        else:
            raise AttributeError(f"{name} is not a valid path")

    def __repr__(self):
        """
        String representation of the SuperH5GroupWrapper, listing all managed paths.
        """
        return f"Cygno Simulation Dataset managing paths: {self._alias}"

class CygnoDataset(AbstractDataset[pd.DataFrame, pd.DataFrame]):
    """Kedro dataset for managing simulation images stored in HDF5 format."""

    def __init__(self, filepath: str, pattern: str, format_file:str):
        """Initialize the dataset with the path to the HDF5 file.

        Parameters:
            filepath (str): The file path to the HDF5 dataset.
        """
        self._filepath = Path(filepath)
        self._keys: List[str] = []
        self._pattern = re.escape(pattern)
        self._format_file = format_file

    def __get_files(self) -> List[str]:
        """Method to retrieve the found files according to pattern class attribute.

        Returns:
            List[str]: _description_
        """
        folder_files = glob(str(self._filepath) + "/*/*")
        return folder_files

    def _load(self) -> HDF5GroupWrapper:
        """Load the HDF5 file, wrap it in an HDF5GroupWrapper, and return the
        wrapper.

        Returns:
            HDF5GroupWrapper: A wrapped HDF5 file ready for data interaction.
        """
        files = self.__get_files()
        if self._format_file == "h5":
            return SuperH5GroupWrapper(files, self._pattern)
        elif self._format_file == "root":
            return SuperROOTGroupWrapper(files, self._pattern)
        else:
            raise ValueError("Format of input data is not supported")


    def _save(self, wrapper: HDF5GroupWrapper) -> None:
        """Save any changes back to the HDF5 file. Currently does nothing.

        Parameters:
            wrapper (HDF5GroupWrapper): The wrapper around the HDF5 file.
        """
        pass

    def _exists(self) -> bool:
        """Check if the HDF5 file exists at the specified path.

        Returns:
            bool: True if the file exists, otherwise False.
        """
        return self._filepath.exists()

    def _describe(self) -> dict:
        """Provide a basic description of the dataset.

        Returns:
            dict: An empty dictionary as a placeholder for dataset description.
        """
        return dict()