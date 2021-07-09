import pygame
from spritesheet import load_images






class TrafficLight(pygame.sprite.Sprite):
    
    file_name = 'trafficlight.png'

    def __init__(self,x,y,width):
        super().__init__()

        self._get_images(width)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x,y))


    def _get_images(self,width):
        
        original_width = 1280//3
        original_height = 1024

        aspect_ratio = width/original_width

        self.images = load_images(self.file_name,1,3,1280//3,1024)

        
        for i, image in enumerate(self.images):
            image = pygame.transform.scale(image,(width,int(aspect_ratio * original_height)))
            self.images[i] = image









