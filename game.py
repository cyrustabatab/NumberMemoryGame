import pygame,sys,random,time,string
pygame.init()

SCREEN_WIDTH = SCREEN_HEIGHT = 800
FPS = 60
BGCOLOR = (255,) * 3
BGCOLOR = (30,144,255)
WHITE = (255,255,255)
BLACK = (0,) *3
GREEN = (0,255,0)
RED = (255,0,0)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()


pygame.display.set_caption("Number Memory Game")



class Button(pygame.sprite.Sprite):


    def __init__(self,x,y,width,height,text,text_color,button_color,font):
        super().__init__()


        self.original_image = pygame.Surface((width,height))
        self.original_rect = self.original_image.get_rect(topleft=(x,y))

        self.bigger_image = pygame.Surface((width + 20,height + 20))
        self.bigger_rect = self.bigger_image.get_rect(center=self.original_rect.center)

        self.text = font.render(text,True,text_color)
        for surface in (self.original_image,self.bigger_image):
            surface.fill(button_color)
            surface.blit(self.text,(surface.get_width()//2 - self.text.get_width()//2,surface.get_height()//2 - self.text.get_height()//2))


        self.image,self.rect = self.original_image,self.original_rect
        self.hovered_on = False

    def update(self,point):
        
        collided = self.rect.collidepoint(point)

        if self.hovered_on and not collided:
            self.hovered_on = False
            self.rect = self.original_rect
            self.image = self.original_image
        elif not self.hovered_on and collided:
            self.hovered_on = True
            self.rect = self.bigger_rect
            self.image = self.bigger_image


    def collided_on(self,point):


        return self.rect.collidepoint(point)
















def game(game_mode):
    
    high_score_file_name = "high_scores.txt"
    
    with open(high_score_file_name,'r') as f:
        high_scores = list(map(int,f.readlines()))
    
    DOMAIN = {0: string.digits,1: string.ascii_uppercase,2: string.digits + string.ascii_uppercase}

    domain = DOMAIN[game_mode]


    prompt = "NUMBER" if game_mode == 0 else "LETTER" if game_mode == 1 else "CHARACTER"
     
    
    def start_timer():

        
        SECOND_EVENT = pygame.USEREVENT + 1
        
        pygame.time.set_timer(SECOND_EVENT,1000)
        index = 0
        start_sound.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SECOND_EVENT:
                    index += 1
                    if index == len(starter_texts):
                        pygame.time.set_timer(SECOND_EVENT,0)
                        return


            screen.fill(BGCOLOR)

            screen.blit(starter_texts[index],(SCREEN_WIDTH//2 - starter_texts[index].get_width()//2,SCREEN_HEIGHT//2 - starter_texts[index].get_height()//2))
            pygame.display.update()



            

    
    
    negative_sound = pygame.mixer.Sound("negative.wav")
    positive_sound = pygame.mixer.Sound("positive.wav")
    win_sound = pygame.mixer.Sound("win.mp3")
    lose_sound = pygame.mixer.Sound('Retro_No hope.ogg')
    start_sound = pygame.mixer.Sound("racestart.wav")


    print(domain)

    def generate_new_number_and_text():
        number = random.choice(domain)
        number_text = number_font.render(str(number),True,BLACK)
        return number,number_text
    

    def write_to_high_score_file_if_needed(score):

        if score > high_scores[-1]:
            high_scores.pop()

            high_scores.append(score)

            high_scores.sort(reverse=True)


            with open(high_score_file_name,'w') as f:
                for score in high_scores:
                    f.write(str(score) + '\n')




    font = pygame.font.SysFont("calibri",80)
    number_font = pygame.font.SysFont("calibri",200)
    

    font.set_bold(True)
    correct_text = font.render("CORRECT!",True,GREEN)
    incorrect_text = font.render("INCORRECT!",True,RED)




    texts = ['READY!','SET!','GO!']
    colors =[(255,0,0),(255,255,0),(0,255,0)]

    starter_texts = []


    for text,color in zip(texts,colors):
        text = font.render(text,True,color)
        starter_texts.append(text)

    font.set_bold(False)

    number,number_text = generate_new_number_and_text()
    numbers = [number]

    current_length = 1
    length = 1
    user_answer = ''
    gap = 50

    enter_start_time = gap_start =  None

    user_entered_length = 0
    incorrect = False
    

    number_enter_text = font.render(f"{prompt} 1",True,BLACK)
    result_text =result_start_time =  None
    
    smaller_font = pygame.font.SysFont("calibri",40)
    length_text = smaller_font.render(f"SCORE: {str(length - 1)}",True,BLACK)
    high_scores_text = smaller_font.render(f"HIGH SCORE: {str(high_scores[0])}",True,BLACK)


    length_text_2 = smaller_font.render(f"LENGTH: {str(length)}",True,BLACK)
    game_over_text = font.render("GAME OVER",True,BLACK)
    

    texts = ['MENU','PLAY AGAIN']
    
    buttons = pygame.sprite.Group()
    button_width = 400
    button_height = 100
    gaps = [50,SCREEN_HEIGHT - 50 - button_height]
    for i,text in enumerate(texts):
        button = Button(SCREEN_WIDTH//2 - button_width//2,gaps[i],button_width,button_height,text,BLACK,RED,font)
        buttons.add(button)




    start_timer()
    start_time = time.time()
    game_over = False
    while True:
        
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not start_time and not gap_start and event.type == pygame.KEYDOWN:
                if not game_over:
                    try:
                        char = chr(event.key).upper()
                    except:
                        continue
                    if not user_answer and not enter_start_time and char in domain:
                        user_answer = char
                        user_answer_text = font.render(user_answer,True,BLACK)
                    elif user_answer and not enter_start_time and not result_start_time:
                        if event.key == pygame.K_BACKSPACE:
                            user_answer = None
                        elif event.key == pygame.K_RETURN:
                            answer = user_answer
            

                            user_answer_text = font.render(user_answer,True,GREEN if answer == numbers[user_entered_length] else RED)

                            incorrect = answer != numbers[user_entered_length]
                            if not incorrect:
                                positive_sound.play()
                            else:
                                negative_sound.play()
                            user_entered_length += 1
                            if user_entered_length == len(numbers) or incorrect:
                                result_text = correct_text if not incorrect else incorrect_text
                                result_start_time = time.time()
                                if result_text is correct_text:
                                    win_sound.play()
                            else:
                                enter_start_time =time.time()
                else:
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        start_timer()
                        start_time = time.time()

            elif game_over and event.type == pygame.MOUSEBUTTONDOWN:      
                point = pygame.mouse.get_pos()


                for i,button in enumerate(buttons):
                    if button.collided_on(point):
                        if i == 0:
                            return
                        game_over = False
                        start_timer()
                        start_time = time.time()






        
        screen.fill(BGCOLOR)

        if not game_over:
            if start_time and current_time - start_time >= 1:
                if current_length == length:
                    start_time = None
                else:
                    gap_start = time.time()
                    number_text= font.render("",True,BLACK)
                    start_time = None

            elif gap_start and current_time - gap_start >= 0.5:
                number,number_text = generate_new_number_and_text()
                numbers.append(number)
                start_time = time.time()
                current_length += 1
                gap_start = None
            if start_time:
                if current_time - start_time >= 1:
                    if current_length == length:
                        start_time = None
                    else:
                        number,number_text = generate_new_number_and_text()
                        start_time = time.time()
                        current_length += 1
                screen.blit(number_text,(SCREEN_WIDTH//2 - number_text.get_width()//2,SCREEN_HEIGHT//2 - number_text.get_height()//2))
            elif enter_start_time and current_time - enter_start_time >= 0.5:
                if user_entered_length < len(numbers):
                    number_enter_text = font.render(f"{prompt} {user_entered_length + 1}",True,BLACK)
                    enter_start_time = None
                    user_answer = ''
            elif result_start_time and current_time - result_start_time >= 3:
                number,number_text = generate_new_number_and_text()
                user_entered_length = 0
                numbers = [number]
                enter_start_time = None
                if incorrect:
                    write_to_high_score_file_if_needed(length - 1)
                    game_over = True
                    final_score_text = font.render(f"SCORE: {str(length - 1)}",True,BLACK)
                else:
                    start_time = time.time()
                length = length + 1 if not incorrect else 1
                number_enter_text = font.render(f"{prompt} 1",True,BLACK)
                user_answer = None
                length_text = smaller_font.render(f"SCORE: {str(length - 1)}",True,BLACK)
                current_length = 1
                result_start_time = None
                result_text = None


            if not start_time and not gap_start:
                if user_answer:
                    screen.blit(user_answer_text,(SCREEN_WIDTH//2 -user_answer_text.get_width()//2,SCREEN_HEIGHT- gap - user_answer_text.get_height()//2))
                screen.blit(number_enter_text,(SCREEN_WIDTH//2 - number_enter_text.get_width()//2,SCREEN_HEIGHT - 4* gap))
            if result_text:
                screen.blit(result_text,(SCREEN_WIDTH//2 - result_text.get_width()//2,gap * 2))

            length_text_2 = smaller_font.render(f"LENGTH: {str(length)}",True,BLACK)
            screen.blit(length_text_2,(SCREEN_WIDTH//2 - length_text_2.get_width()//2,SCREEN_HEIGHT - 6 * gap))
        else: 
            point = pygame.mouse.get_pos()
            buttons.update(point)
            screen.blit(game_over_text,(SCREEN_WIDTH//2 - game_over_text.get_width()//2,SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
            screen.blit(final_score_text,(SCREEN_WIDTH//2 - final_score_text.get_width()//2,SCREEN_HEIGHT//2 + final_score_text.get_height()//2))
            buttons.draw(screen)
        screen.blit(length_text,(0,0))
        screen.blit(high_scores_text,(SCREEN_WIDTH - high_scores_text.get_width(),0))
        pygame.display.update() 
        clock.tick(FPS)


def menu():


    title_font = pygame.font.SysFont("calibri",100,bold=True)

    title_text = title_font.render("NUMMEM",True,BLACK)
    top_gap = 50
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2,top_gap + title_text.get_height()//2))

    button_width = 575
    button_height = 100
    top_gap = 50

    start_button = Button(SCREEN_WIDTH//2 - button_width//2,top_gap * 2 + title_text.get_height(),button_width,button_height,"START",BLACK,RED,title_font)

    
    high_scores_button = Button(SCREEN_WIDTH//2 - button_width//2,top_gap * 3 + button_height + title_text.get_height(),button_width,button_height,"HIGH SCORES",BLACK,RED,title_font)

    buttons = pygame.sprite.Group(start_button,high_scores_button)

    mode_texts = ('NUMBERS','LETTERS','NUMBERS + LETTERS')
    

    mode_font = pygame.font.SysFont("calibri",50,bold=True)
    width = mode_font.render(mode_texts[-1],True,BLACK).get_width()
    mode_buttons = pygame.sprite.Group() 
    gap = (SCREEN_HEIGHT - (len(mode_texts) * button_height  + (len(mode_texts) - 1) * top_gap))//2
    button_width = width + 20
    for i,mode_text in enumerate(mode_texts):
        button = Button(SCREEN_WIDTH//2 - button_width//2,gap + i * (button_height + top_gap),button_width,button_height,mode_text,BLACK,RED,mode_font)
        mode_buttons.add(button)

    mode_title = title_font.render("MODE",True,BLACK)

    

    def mode():



        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    for i,button in enumerate(buttons):
                        if button.collided_on(point):
                            return i

            point = pygame.mouse.get_pos() 
            mode_buttons.update(point)


            screen.fill(BGCOLOR)
            screen.blit(mode_title,(SCREEN_WIDTH//2 - mode_title.get_width()//2,top_gap))
            mode_buttons.draw(screen)
            pygame.display.update()



    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                point = pygame.mouse.get_pos()


                for i,button in enumerate(buttons):
                    if button.collided_on(point):
                        if i == 0:
                            game_mode = mode()
                            game(game_mode)


                
        
        point = pygame.mouse.get_pos()
        buttons.update(point)
        screen.fill(BGCOLOR)
        
            
        buttons.draw(screen)
        screen.blit(title_text,title_rect)
        pygame.display.update()

        








if __name__ == "__main__":
    
    menu()
    #game()

