import pygame,sys,random,time
pygame.init()

SCREEN_WIDTH = SCREEN_HEIGHT = 800
FPS = 60
BGCOLOR = (255,) * 3
BGCOLOR = (30,144,255)
BLACK = (0,) *3
GREEN = (0,255,0)
RED = (255,0,0)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()


pygame.display.set_caption("Number Memory Game")




def game():
    
    
    negative_sound = pygame.mixer.Sound("negative.wav")
    positive_sound = pygame.mixer.Sound("positive.wav")
    win_sound = pygame.mixer.Sound("win.mp3")
    lose_sound = pygame.mixer.Sound('Retro_No hope.ogg')



    def generate_new_number_and_text():
        number = random.randint(0,9)
        number_text = number_font.render(str(number),True,BLACK)
        return number,number_text
    font = pygame.font.SysFont("calibri",80)
    number_font = pygame.font.SysFont("calibri",200)

    correct_text = font.render("CORRECT!",True,GREEN)
    incorrect_text = font.render("INCORRECT!",True,RED)

    number,number_text = generate_new_number_and_text()
    numbers = [number]

    current_length = 1
    length = 1
    user_answer = ''
    gap = 50

    start_time = time.time()
    enter_start_time = gap_start =  None

    user_entered_length = 0
    incorrect = False
    

    number_enter_text = font.render("NUMBER 1",True,BLACK)
    result_text =result_start_time =  None
        
    length_text = font.render(f"LENGTH: {str(length)}",True,BLACK)

    while True:
        
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not start_time and not gap_start and  event.type == pygame.KEYDOWN:
                if not user_answer and not enter_start_time and pygame.K_0 <= event.key <= pygame.K_9:
                    user_answer = chr(event.key)
                    user_answer_text = font.render(user_answer,True,BLACK)
                elif user_answer and not enter_start_time and not result_start_time:
                    if event.key == pygame.K_BACKSPACE:
                        user_answer = None
                    elif event.key == pygame.K_RETURN:
                        answer = int(user_answer)
        

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


        
        screen.fill(BGCOLOR)
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
                number_enter_text = font.render(f"NUMBER {user_entered_length + 1}",True,BLACK)
                enter_start_time = None
                user_answer = ''
        elif result_start_time and current_time - result_start_time >= 3:
            number,number_text = generate_new_number_and_text()
            user_entered_length = 0
            numbers = [number]
            length = length + 1 if not incorrect else 1
            incorrect = False
            number_enter_text = font.render(f"NUMBER 1",True,BLACK)
            user_answer = None
            length_text = font.render(f"LENGTH: {str(length)}",True,BLACK)
            current_length = 1
            start_time = time.time()
            result_start_time = None
            result_text = None


        if not start_time and not gap_start:
            if user_answer:
                screen.blit(user_answer_text,(SCREEN_WIDTH//2 -user_answer_text.get_width()//2,SCREEN_HEIGHT- gap - user_answer_text.get_height()//2))
            screen.blit(number_enter_text,(SCREEN_WIDTH//2 - number_enter_text.get_width()//2,SCREEN_HEIGHT - 4* gap))
        if result_text:
            screen.blit(result_text,(SCREEN_WIDTH//2 - result_text.get_width()//2,gap * 2))
        
        screen.blit(length_text,(0,0))
        pygame.display.update() 
        clock.tick(FPS)


if __name__ == "__main__":
    
    game()

