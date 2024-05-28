from ...datasets.cygno_data import CygnoNoiseImage, CygnoSimulationImage
from typing import Tuple, Optional
import numpy as np
import os
import uuid
import pdb
from kedro.io import DataCatalog

def create_event(
    sim_dataset: str, 
    noise_dataset: str, 
    random_shift_max: int,
    cut_edges: Tuple[str],
    number_of_events: int,
    output_location_path: str,
    start_index_sim: Optional[int] = 0,
    end_index_sim:  Optional[int] = -1,
    start_index_noise: Optional[int] = 0,
    end_index_noise:  Optional[int] = -1,

):
    for _ in range(0, number_of_events):

        sim_img_sample = sim_dataset[
            np.random.choice(range(start_index_sim, end_index_sim))
        ].random_translate(random_shift_max)
        noise_img_sample = noise_dataset[
            np.random.choice(range(start_index_noise, end_index_noise))
        ]
        save_path = os.path.join(output_location_path, str(uuid.uuid4()) + ".npy")
        np.save(
            save_path,
            sim_img_sample + noise_img_sample
        )

        
