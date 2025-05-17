import os
from RAGwithSagemaker.logging.logging import logger 
import yaml
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError
from dotenv import dotenv_values

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    
    try:
        with open(path_to_yaml, "r") as file:
            content = yaml.safe_load(file)
            logger.info(f"{path_to_yaml} file loaded sucessfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_dir(path_to_dirs: list, verbose=True):
    for path in path_to_dirs:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory {path} created")
            
@ensure_annotations
def save_json(path:Path, data:dict):
    with open(path, "w") as file:
        json.dump(data,file, indent=4)
    logger.info(f"data saved to {path}")


@ensure_annotations
def load_json(path:Path):
    with open(path, "r") as file:
        content = json.load(file)
    logger.info(f"data laoded from {path}")
    return ConfigBox(content)



@ensure_annotations
def save_bin(path:Path, data: Any):
    joblib.dump(value=data, filename=path)
    logger.info(f"data saved to {path}")
    

@ensure_annotations
def load_bin(path:Path):
    data = joblib.load(path)
    logger.info(f"data loaded from {path}")
    return data


@ensure_annotations
def read_envfile(path:Path):
    env_vars = dict(dotenv_values(path))
    return env_vars