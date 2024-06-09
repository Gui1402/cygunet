from kedro.pipeline import Pipeline, pipeline
from .nodes import create_generate_events_node

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        create_generate_events_node(
            simulation_datasets="simulation",
            noise_datasets="noise",
            max_events="params:generate_data.train.simulation.max_events",
            valid_indexes_list_sim="params:generate_data.train.simulation.valid_indexes",
            valid_index_list_noise="params:generate_data.train.noise.valid_indexes",
            number_of_events="params:generate_data.train.events",
            max_translation="params:generate_data.max_translation",
            edges="params:generate_data.edges",
            tag="train"
        )
    ])