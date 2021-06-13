import pygame,sys,random,time
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




def game():
    
    high_score_file_name = "high_scores.txt"
    
    with open(high_score_file_name,'r') as f:
        high_scores = list(map(int,f.readlines()))


    
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




    def generate_new_number_and_text():
        number = random.randint(0,9)
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
    

    number_enter_text = font.render("NUMBER 1",True,BLACK)
    result_text =result_start_time =  None
    
    smaller_font = pygame.font.SysFont("calibri",40)
    length_text = smaller_font.render(f"LENGTH: {str(length)}",True,BLACK)
    high_scores_text = smaller_font.render(f"HIGH SCORE: {str(high_scores[0])}",True,BLACK)
    start_timer()
    start_time = time.time()
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
            if incorrect:
                write_to_high_score_file_if_needed(length)
            length = length + 1 if not incorrect else 1
            number_enter_text = font.render(f"NUMBER 1",True,BLACK)
            user_answer = None
            length_text = smaller_font.render(f"LENGTH: {str(length)}",True,BLACK)
            current_length = 1
            result_start_time = None
            result_text = None
            if incorrect:
                incorrect = False
                start_timer()
            start_time = time.time()


        if not start_time and not gap_start:
            if user_answer:
                screen.blit(user_answer_text,(SCREEN_WIDTH//2 -user_answer_text.get_width()//2,SCREEN_HEIGHT- gap - user_answer_text.get_height()//2))
            screen.blit(number_enter_text,(SCREEN_WIDTH//2 - number_enter_text.get_width()//2,SCREEN_HEIGHT - 4* gap))
        if result_text:
            screen.blit(result_text,(SCREEN_WIDTH//2 - result_text.get_width()//2,gap * 2))
        
        screen.blit(length_text,(0,0))
        screen.blit(high_scores_text,(SCREEN_WIDTH - high_scores_text.get_width(),0))
        pygame.display.update() 
        clock.tick(FPS)


if __name__ == "__main__":
    
    game()

