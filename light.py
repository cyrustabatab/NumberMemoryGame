import pygame
from spritesheet import load_images






class TrafficLight(pygame.sprite.Sprite):
    
    file_name = 'trafficlight4.png'

    def __init__(self,width,screen_width,screen_height):
        super().__init__()

        self._get_images(width)
        self.image = self.images[0]
        self.image_index = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.rect = self.image.get_rect(topleft=(screen_width//2 - self.image.get_width()//2,screen_height//2 - self.image.get_height()//2))


    def _get_images(self,width):
        
        original_width = 1176//3
        original_height = 1024

        aspect_ratio = width/original_width

        self.images = load_images(self.file_name,1,3,1176//3,1024)

        
        for i, image in enumerate(self.images):
            image = pygame.transform.scale(image,(width,int(aspect_ratio * original_height)))
            self.images[i] = image

    
    def update(self):

        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(topleft=(self.screen_width//2 - self.image.get_width()//2,self.screen_height//2 - self.image.get_height()//2))










