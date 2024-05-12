import numpy as np
def generate_data(
    mask_datasets, 
    bg_dataset, 
    range_mask, 
    range_noise, 
    max_translation, 
    cut_egdes, 
    max_events):

    events = np.random.randint(max_events)
    for ev in events:
        index = np.random.randint(*range_mask)
        ds = random.choice(mask_datasets)