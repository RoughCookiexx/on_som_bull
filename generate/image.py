import json
import os
import time

import pygame
import sys
from urllib import request


def queue_image_generation(prompt_text):
    with open('image_prompt.json') as file:
        prompt = json.load(file)
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')
        req = request.Request("http://127.0.0.1:8188/prompt", data=data)
        request.urlopen(req)

#
# async def show_image():
#     # Screen setup
#     screen_width, screen_height = 512, 600
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     pygame.display.set_caption("Slide In Example")
#
#     # Colors
#     green = (0, 255, 0)
#     white = (255, 255, 255)
#
#     # Font setup
#     font = pygame.font.SysFont('Anton', 108)
#
#     file_name = get_latest_file('C:\\Users\\Tommy\\comfy\\ComfyUI_windows_portable_nvidia\\ComfyUI_windows_portable\\ComfyUI\\output')
#
#     # Load image
#     image = pygame.image.load(file_name)
#     image_rect = image.get_rect()
#     image_rect.x = screen_width  # Start off-screen (right side)
#     image_rect.y = screen_height - image.get_height()
#
#     # Text setup
#     text = font.render("Sliding Text", True, white)
#     text_rect = text.get_rect()
#     text_rect.x = screen_width  # Start off-screen (right side)
#     text_rect.y = 0
#
#     # Speed of sliding
#     slide_speed = 5
#     target_x = 0
#
#     # Main loop
#     clock = pygame.time.Clock()
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#         # Slide image and text from the right
#         if image_rect.x > target_x:
#             image_rect.x -= slide_speed
#         if text_rect.x > target_x:
#             text_rect.x -= slide_speed
#
#         # Fill screen and draw
#         screen.fill(green)
#         screen.blit(image, image_rect)
#         screen.blit(text, text_rect)
#         pygame.display.flip()
#
#         clock.tick(60)
#         time.sleep(10)




if __name__ == '__main__':
    queue_image_generation('')

    # pygame.init()
    # show_image()
