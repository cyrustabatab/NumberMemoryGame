import pygame,sys,random,time
pygame.init()

SCREEN_WIDTH = SCREEN_HEIGHT = 800
FPS = 60
BGCOLOR = (255,) * 3
BLACK = (0,) *3
GREEN = (0,255,0)
RED = (255,0,0)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()


pygame.display.set_caption("Number Memory Game")




def game():
    
    

    def generate_new_number_and_text():
        number = random.randint(0,9)
        number_text = font.render(str(number),True,BLACK)
        return number,number_text
    font = pygame.font.SysFont("calibri",80)
    

    number,number_text = generate_new_number_and_text()
    numbers = [number]
    
    current_length = 1
    length = 1
    user_answer = ''
    gap = 50

    start_time = time.time()
    enter_start_time = None

    user_entered_length = 0
    incorrect = False



    while True:
        
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not start_time and  event.type == pygame.KEYDOWN:
                if not user_answer and not enter_start_time and pygame.K_0 <= event.key <= pygame.K_9:
                    user_answer = chr(event.key)
                    user_answer_text = font.render(user_answer,True,BLACK)
                elif user_answer:
                    if event.key == pygame.K_BACKSPACE:
                        user_answer = None
                    elif event.key == pygame.K_RETURN:
                        answer = int(user_answer)
        

                        print(answer,numbers[user_entered_length])
                        user_answer_text = font.render(user_answer,True,GREEN if answer == numbers[user_entered_length] else RED)
                        incorrect = answer != numbers[user_entered_length]
                        print(incorrect)
                        user_entered_length += 1
                        enter_start_time =time.time()



        
        screen.fill(BGCOLOR)
        if start_time and current_time - start_time >= 1:
            if current_length == length:
                start_time = None
            else:
                number,number_text = generate_new_number_and_text()
                numbers.append(number)
                start_time = time.time()
                current_length += 1

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
                enter_start_time = None
                user_answer = ''
            elif user_entered_length == len(numbers) or incorrect:
                number,number_text = generate_new_number_and_text()
                user_entered_length = 0
                numbers = [number]
                incorrect = False
                user_answer = None
                length += 1
                current_length = 1
                start_time = time.time()
                enter_start_time = None




        if not start_time and user_answer:
            screen.blit(user_answer_text,(SCREEN_WIDTH//2 -user_answer_text.get_width()//2,SCREEN_HEIGHT- gap - user_answer_text.get_height()//2))
        pygame.display.update() 
        clock.tick(FPS)


if __name__ == "__main__":
    
    game()

