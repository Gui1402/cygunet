from kedro.pipeline import Pipeline, pipeline
from .nodes import save_event

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([save_event])