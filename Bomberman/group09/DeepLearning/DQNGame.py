import torchvision.transforms as T
import torch

import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')
from DeepAgent import DeepAgent
from interactivecharacter import InteractiveCharacter
from entity import CharacterEntity
from game import Game
from real_world import RealWorld
import pygame
from events import Event
import colorama
import numpy as np
import math
from PIL import Image


class DQNGame(Game):
    def __init__(self, width, height, max_time, bomb_time, expl_duration, expl_range, sprite_dir="../../bomberman/sprites/"):
        super(DQNGame, self).__init__(width,height,max_time,bomb_time,expl_duration,expl_range,sprite_dir)
        self.agent = None
        self.resize = T.Compose([T.ToPILImage(),
                    T.Resize(40, interpolation=Image.CUBIC),
                    T.ToTensor()])
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.add_character()

    def add_character(self):
        self.agent = DeepAgent("me", # namFe
                                    "C",  # avatar
                                     0, 0,  # position
    )
        super(DQNGame, self).add_character(self.agent)

    def get_frame(self,wait=1):
        """ Main game loop. """
        if wait == 0:
            def step():
                self.capture_screen()
                pygame.event.clear()
                input("Press Enter to continue or CTRL-C to stop...")
        else:
            def step():
                    self.capture_screen()
                    pygame.time.wait(abs(wait))
                    pygame.event.clear()


        colorama.init(autoreset=True)
        (self.world, self.events) = self.world.next()
        self.display_gui()
        # self.draw()
        step()
        self.world.next_decisions()
        colorama.deinit()

        return self.capture_screen(), self.done()


    def capture_screen(self):
        pygame.image.save(self.screen,"imgs/0.jpeg")
        np_image = self.get_jpg("imgs/0.jpeg")
        screen = torch.from_numpy(np_image)
        return self.resize(screen).unsqueeze(0).to(self.device)
    
    def get_jpg(self,file):
        image = Image.open(file)
        img_data = np.array(image)
        img_data = self.rgb2gray(img_data)
        rescaled = (255.0 / img_data.max() * (img_data - img_data.min())).astype(np.uint8)
        return rescaled

    def rgb2gray(self,rgb):
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray