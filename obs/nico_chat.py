# import os
# from dotenv import load_dotenv
import obsws_python as obs
from copy import deepcopy
import constants as const
import random
import asyncio
import traceback


class NicoChat:
    def __init__(self, host, port, password):  
        self.client = obs.ReqClient(host=host, port=port, password=password)
        self.chatCount = 0

    async def splash_chat(self, message, user_name, color):
        try:
            # deepcopy
            input_settings = deepcopy(const.NICO_TEXT_SETTINGS)
            input_settings["text"] = message
            input_settings["color"] = color
            input_kind = "text_gdiplus_v2" 
            input_name = f'MyTextSource_{user_name} {self.chatCount}'
            self.chatCount += 1
            scene_name = self.current_scene_name

            response = self.client.create_input(sceneName=scene_name, inputName=input_name, inputKind=input_kind, inputSettings=input_settings, sceneItemEnabled=True)
    
            item_id = response.scene_item_id
             # TODO: 텍스트 소스의 width, height가 정해질 때까지 대기하도록 수정
            # await asyncio.sleep(0.5)

            initial_x = const.SCREEN.WIDTH
            initial_y = random.randint(0, const.SCREEN.HEIGHT / 2)

            self.client.set_scene_item_transform(scene_name=scene_name, item_id=item_id, transform={
            "positionX": initial_x,
            "positionY": initial_y,
            })

            # 텍스트가 화면 밖으로 나갈때 까지, 왼쪽으로 계속 이동
            transform = self.client.get_scene_item_transform(scene_name=scene_name, item_id=item_id).scene_item_transform

            item_width = 0
            
            while transform['positionX'] + item_width > 0:
                transform = self.get_transform(scene_name, item_id)
                if (item_width == 0):
                    item_width = transform['sourceWidth']
                await self.move_text_left(scene_name, item_id, transform, message)
                
                transform = self.get_transform(scene_name, item_id)

            self.client.remove_scene_item(scene_name, item_id)
            self.chatCount -= 1
            print(f"Removed item {item_id}")
            
        except Exception as e:
            print(f"Error in nicodong_chat: {e}")
            print(traceback.format_exc())
            return
    
    def get_resolution(self):
        width = self.client.get_video_info().baseWidth
        height = self.client.get_video_info().baseHeight
        return width, height
    
    async def move_text_left(self, scene_name, item_id, transform, text,step=5, base_delay=0.05):
        text_length = len(text)
        delay = base_delay / max(1, text_length / 10) # 글자수가 많을수록 딜레이가 길어지도록
      
        self.client.set_scene_item_transform(scene_name=scene_name, item_id=item_id, transform={
                    "positionX": transform['positionX'] - 10,
                    "positionY": transform['positionY']
                })
    
        await asyncio.sleep(delay)
    
    @property
    def current_scene_name(self):
        return self.client.get_scene_list().current_program_scene_name


    def get_transform(self, scene_name, item_id):
        return self.client.get_scene_item_transform(scene_name=scene_name, item_id=item_id).scene_item_transform
  