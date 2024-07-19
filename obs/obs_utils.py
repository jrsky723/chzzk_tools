import obsws_python as obs
from typing import Any, Dict
from .dataclass import SceneItemTransform

def get_current_scene_name(obs_client: obs.ReqClient) -> str:
    response = obs_client.get_scene_list()
    if hasattr(response, "current_program_scene_name"):
        return getattr(response, "current_program_scene_name")
    else:
        raise ValueError("Invalid response from get_scene_list")

def get_transform(obs_client: obs.ReqClient, scene_name: str, item_id: int) -> SceneItemTransform:
    response = obs_client.get_scene_item_transform(scene_name=scene_name, item_id=item_id)
    if hasattr(response, "scene_item_transform"):
        return SceneItemTransform.from_response(response)
    else:
        raise ValueError("Invalid response from get_scene_item_transform")

def scene_item_exists(client: obs.ReqClient, scene_name: str, item_name: str) -> bool:
    try:
        response = client.get_scene_item_list(scene_name)
        if hasattr(response, "scene_items"):
            scene_items = getattr(response, "scene_items")
            for item in scene_items:
                if item['sourceName'] == item_name:
                    return True
        return False
    except Exception as e:
        raise e
