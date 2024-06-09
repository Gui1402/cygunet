from kedro.pipeline import node
from typing import List
from ...datasets.cygno_data import CygnoDataset
import numpy as np
from .utils import generate_event




def create_generate_events_node(
        simulation_datasets: CygnoDataset,
        noise_datasets: CygnoDataset,
        max_events: int,
        valid_indexes_list_sim: List[int],
        valid_index_list_noise: List[int],
        number_of_events: int,
        max_translation: int,
        edges: List[int],
        tag: str
    ):
    
    inputs = {
        "simulation_datasets": simulation_datasets,
        "noise_datasets": noise_datasets,
        "max_events": max_events,
        "valid_indexes_list_sim": valid_indexes_list_sim,
        "valid_index_list_noise": valid_index_list_noise,
        "number_of_events": number_of_events,
        "max_translation": max_translation,
        "edges": edges
    }

    return node(
        generate_event,
        inputs=inputs,
        outputs="array_dataset",
        name="generate_events_node",
        tags=[f"data_generating_{tag}"]
    )

