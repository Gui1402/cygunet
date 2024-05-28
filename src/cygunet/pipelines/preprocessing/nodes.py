from kedro.pipeline import node
from .utils import create_event
from ...datasets.cygno_data import HDF5GroupWrapper
import numpy as np

def access_event(dataset: HDF5GroupWrapper):
    np.save("data/02_intermediate/img.npy", dataset[10])
    return "data/02_intermediate/img.npy"


save_event = node(
    func=access_event,
    inputs=["simulation.ER_1"],
    outputs="array_dataset",
    name="save_event_node"
    
)

# generate_image = node(
#     func=create_event,
#     inputs=dict(
#         sim_dataset="params:generate_image.sim_dataset",
#         noise_dataset="params:generate_image.noise_dataset",
#         random_shift_max="params:generate_image.random_shift_max",
#         cut_edges="params:generate_image.cut_edges",
#         number_of_events="params:generate_image.number_of_events",
#         output_location_path="params:generate_image.output_location_path",
#         start_index_sim="params:generate_image.start_index_sim",
#         end_index_sim="params:generate_image.end_index_sim",
#         start_index_noise="params:generate_image.start_index_noise",
#         end_index_noise="params:generate_image.end_index_noise",
#     ),
#     outputs="real_image",
#     name="generate_image",
#     tags=["generate_image"]
# )


