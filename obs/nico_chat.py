import obsws_python as obs
from copy import deepcopy
import constants.common_const as const
import constants.nico_chat_const as NicoConst
import random
import asyncio
import time
import traceback
from typing import Any, Dict
import obs.obs_utils as utils


class NicoChat:
    def __init__(self, client: obs.ReqClient):  
        self.client: obs.ReqClient = client
        self.chat_count: int = 0
        self.max_count: int = 10
        self.chat_idx: int = 0

        self.remove_existing_mytext_sources()

    def remove_existing_mytext_sources(self) -> None:
        try:
            scene_name = utils.get_current_scene_name(self.client)
            sources = self.client.get_scene_item_list(scene_name)
            scene_items = getattr(sources, "scene_items")
            if not isinstance(scene_items, list):
                raise ValueError("Invalid response from get_scene_item_list")
            for source in scene_items:
                if source['sourceName'].startswith('MyTextSource'):
                    self.client.remove_scene_item(scene_name, source['sceneItemId'])
        except Exception as e:
            print(f"Error in remove_existing_mytext_sources: {e}")
            print(traceback.format_exc())
            return

    async def splash_chat(self, message: str, color: int) -> None:
        try:
            # deepcopy
            input_settings: Dict[str, Any] = deepcopy(NicoConst.TEXT_SETTINGS)
            input_settings["text"] = message
            input_settings["color"] = color
            input_kind: str = "text_gdiplus_v3"
            input_name: str = f'MyTextSource_{self.chat_idx}'
            
            scene_name: str = utils.get_current_scene_name(self.client)

            if self.chat_count > self.max_count:
                return
            
            response = self.client.create_input(sceneName=scene_name, inputName=input_name, inputKind=input_kind, inputSettings=input_settings, sceneItemEnabled=True)
            item_id: int = getattr(response, "scene_item_id")
            
            self.chat_count += 1
            self.chat_idx += 1

            print(f"Created item {item_id}: {message}")
            
            initial_x: int = const.Screen.WIDTH
            initial_y: int = random.randint(0, const.Screen.HEIGHT // 2)

            self.client.set_scene_item_transform(scene_name=scene_name, item_id=item_id, transform={
                "positionX": initial_x,
                "positionY": initial_y,
            })

            await self.move_text_left(scene_name, item_id, message, initial_x, initial_y)

        except Exception as e:
            print(f"Error in splash_chat: {e}")
            print(traceback.format_exc())
            return


    async def move_text_left(self, scene_name: str, item_id: int, text: str, initial_x: int, initial_y: int) -> None:
        base_step: float = 5
        text_length: int = len(text)
        step: float = base_step + text_length / 5 # 글자 수에 따라 이동 속도 조절

        current_x: float = initial_x
        
        item_width: int = 0
        while current_x + item_width > 0:
            if item_width == 0:
                item_width = utils.get_transform(self.client, scene_name, item_id).sourceWidth
            current_x -= step
            self.client.set_scene_item_transform(
                scene_name=scene_name,
                item_id=item_id,
                transform={
                    "positionX": current_x,
                    "positionY": initial_y,
                }
            )
            start_time = time.perf_counter()
            while time.perf_counter() - start_time < 0.01:
                await asyncio.sleep(0)
        
        # 이동이 끝나면 삭제
        self.client.remove_scene_item(scene_name, item_id)
        self.chat_count -= 1
        print(f"Removed item {item_id}")