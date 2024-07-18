import obsws_python as obs
from copy import deepcopy
import constants as const
import random
import asyncio
import traceback
from typing import Any, Dict
from obs.dataclass import SceneItemTransform   

class NicoChat:
    def __init__(self, client: obs.ReqClient):  
        self.client: obs.ReqClient = client
        self.chatCount: int = 0
        self.maxCount: int = 10

    async def splash_chat(self, message: str, user_name: str, color: int) -> None:
        try:
            # deepcopy
            input_settings: Dict[str, Any] = deepcopy(const.NicoChat.TEXT_SETTINGS)
            input_settings["text"] = message
            input_settings["color"] = color
            input_kind: str = "text_gdiplus_v2"
            input_name: str = f'MyTextSource_{user_name} {self.chatCount}'
            self.chatCount += 1
            scene_name: str = self.current_scene_name

            if self.chatCount > self.maxCount:
                self.chatCount -= 1
                return

            response = self.client.create_input(sceneName=scene_name, inputName=input_name, inputKind=input_kind, inputSettings=input_settings, sceneItemEnabled=True)

            item_id: int = getattr(response, "scene_item_id")
            print(f"Created item {item_id}: {message}")
            initial_x: int = const.Screen.WIDTH
            initial_y: int = random.randint(0, const.Screen.HEIGHT // 2)

            self.client.set_scene_item_transform(scene_name=scene_name, item_id=item_id, transform={
                "positionX": initial_x,
                "positionY": initial_y,
            })

            transform = self.get_transform(scene_name, item_id)

            item_width: int = 0

            while transform.positionX + item_width > 0:
                transform = self.get_transform(scene_name, item_id)
                if item_width == 0:
                    item_width = transform.sourceWidth
                await self.move_text_left(scene_name, item_id, transform, message)

                transform = self.get_transform(scene_name, item_id)

            self.client.remove_input(input_name)
            self.chatCount -= 1
            print(f"Removed item {item_id}: {message}")

        except Exception as e:
            print(f"Error in splash_chat: {e}")
            print(traceback.format_exc())
            return


    async def move_text_left(self, scene_name: str, item_id: int, transform: SceneItemTransform, text: str, step: int = 1, base_delay: float = 0.0001) -> None:
        text_length: int = len(text)
        delay: float = base_delay / max(1, text_length / 10)  # 글자수가 많을수록 딜레이가 길어지도록

        self.client.set_scene_item_transform(scene_name=scene_name, item_id=item_id, transform={
            "positionX": transform.positionX - step,
            "positionY": transform.positionY
        })

        await asyncio.sleep(delay)

    @property
    def current_scene_name(self) -> str:
        response = self.client.get_scene_list()
        if hasattr(response, "current_program_scene_name"):
            return getattr(response, "current_program_scene_name")
        else:
            raise ValueError("Invalid response from get_scene_list")

    def get_transform(self, scene_name: str, item_id: int) -> SceneItemTransform:
        response = self.client.get_scene_item_transform(scene_name=scene_name, item_id=item_id)
        if hasattr(response, "scene_item_transform"):
            return SceneItemTransform.from_response(response)
        else:
            raise ValueError("Invalid response from get_scene_item_transform")