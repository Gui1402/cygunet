from ...datasets.cygno_data import CygnoDataset
from typing import Tuple, Optional, List
import numpy as np
import os
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed


def generate_partition_number(start=0):
    current = start
    while True:
        yield "{:07}".format(current)
        current += 1

def process_event(simulation_datasets, noise_datasets, max_events, valid_indexes_list_sim, valid_index_list_noise, max_translation, edges):
    number_of_events = np.random.randint(low=1, high=max_events)
    sim_keys = simulation_datasets.keys
    noise_keys = noise_datasets.keys
    seed_sim_events = np.random.choice(sim_keys, number_of_events)
    seed_noise_event = np.random.choice(noise_keys)

    output_map = map(lambda x: 
        getattr(simulation_datasets, x)
        [int(np.random.choice(valid_indexes_list_sim))]
        .random_translate(max_translation=max_translation)
        .cut_edges(*edges), 
        seed_sim_events
    )
    noise_img = (
        getattr(noise_datasets, seed_noise_event)
        [int(np.random.choice(valid_index_list_noise))]
        .cut_edges(*edges)
    )
    return np.add.reduce(list(output_map)) + noise_img


def generate_event(
    simulation_datasets, 
    noise_datasets,
    max_events,
    valid_indexes_list_sim,
    valid_index_list_noise,
    number_of_events,
    max_translation,
    edges
    ):
    output_dict = {}
    partition_id = generate_partition_number()
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_event, 
                simulation_datasets, 
                noise_datasets, 
                max_events, 
                valid_indexes_list_sim, 
                valid_index_list_noise, 
                max_translation, 
                edges
            )
            for _ in range(number_of_events)
        ]

        for future in as_completed(futures):
            output_dict[f"part-{next(partition_id)}"] = future.result()
    
    return output_dict


# def generate_event(
#     simulation_datasets: CygnoDataset, 
#     noise_datasets: CygnoDataset,
#     max_events: int,
#     valid_indexes_list_sim: List[int],
#     valid_index_list_noise: List[int],
#     number_of_events: int,
#     max_translation:int,
#     edges: List[int]
#     ):
#     output_dict = {}
#     partition_id = generate_partition_number()
#     for _ in range(number_of_events):
#         number_of_events = np.random.randint(low=1, high=max_events)
#         sim_keys = simulation_datasets.keys
#         noise_keys = noise_datasets.keys
#         seed_sim_events = np.random.choice(sim_keys, number_of_events)
#         seed_noise_event = np.random.choice(noise_keys)
        
#         output_map = map(lambda x: 
#             getattr(simulation_datasets,x)
#             [int(np.random.choice(valid_indexes_list_sim))]
#             .random_translate(max_translation=max_translation)
#             .cut_edges(*edges), 
#             seed_sim_events
#         )
#         noise_img = (
#             getattr(noise_datasets,seed_noise_event)
#             [int(np.random.choice(valid_index_list_noise))]
#             .cut_edges(*edges)
#         )
#         output_dict[f"part-{next(partition_id)}"] = np.add.reduce(list(output_map)) + noise_img
    
#     return output_dict


        
