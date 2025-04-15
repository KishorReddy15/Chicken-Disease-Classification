import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns
    
    Args:
        path_to_yaml (str): path like input
    
    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            if content is None:
                raise ValueError("yaml file is empty")
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError as e:
        raise ValueError("yaml file is empty or invalid") from e
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories
    
    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """ 
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):   
    """save json data
    
    Args:
        path (Path): path to save json file
        data (dict): data to save in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data
    
    Args:
        path (Path): path to load json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path, "r") as f:
        content = json.load(f)

    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):                            
    """save binary file
    
    Args:
        data (Any): data to save in binary file
        path (Path): path to save binary file
    """
    joblib.dump(data, path)         
    logger.info(f"binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary file
    
    Args:
        path (Path): path to load binary file

    Returns:
        Any: object stored in binary file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded successfully from: {path}")
    return data 

@ensure_annotations
def get_size(path: Path) -> str:
    """get size of file
    
    Args:                   
        path (Path): path to get size of file

    Returns:
        str: size of file
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"         

def decodeImage(imgstring, filename):
    imgdata = base64.b64decode(imgstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)
    f.close()
    return filename

def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as image_file:
        return base64.b64encode(image_file.read())