# All of the code was written independently by myself

import pygame
import sys
import random
import time

class Card(pygame.sprite.Sprite):
    def __init__(self, value, mode):
        super().__init__()
        if mode == 'red':
                self.image = pygame.image.load('cardback.jpg')
        elif mode == 'blue':
            self.image = pygame.image.load('bluecard.png')
        elif mode == 'black':
            self.image = pygame.image.load('blackcard.png')
        self.rect = self.image.get_rect(top = 0)
        self.flipped = False
        self.solved = False
        self.value = value

def verify_click(cards):
    counter = 0
    for card in cards:
        xpos = pygame.mouse.get_pos()[0] > card.rect.left and pygame.mouse.get_pos()[0] < card.rect.right
        ypos = pygame.mouse.get_pos()[1] > card.rect.top and pygame.mouse.get_pos()[1] < card.rect.bottom
        if xpos and ypos:
            return counter
        else:
            counter += 1
    return -1

def verify_button(buttons):
    counter = 0
    for button in buttons:
        xpos = pygame.mouse.get_pos()[0] > button.left and pygame.mouse.get_pos()[0] < button.right
        ypos = pygame.mouse.get_pos()[1] > button.top and pygame.mouse.get_pos()[1] < button.bottom
        if xpos and ypos:
            return counter
        else:
            counter += 1
    return -1

def shuffle(cards):
    return random.shuffle(cards)

#Flips card only if it has not already been solved. 
def flip(card):
    if not card.flipped:
        image = f"card-{card.value}.png"
        card.image = pygame.image.load(image)
        screen.blit(card.image, card.rect)
        card.flipped = True
        return True
    return False

def check_win(cards, num_cards):
    counter = 0
    for card in cards:
        if card.solved:
            counter += 1
    return True if counter == num_cards else False

def check_match(card1, card2):
    if card1.value == card2.value:
        card1.solved = True
        card2.solved = True

def place_cards(cards, num_cards):
    if num_cards == 6:
        xpos = 75
        ypos = 300
        for card in cards:
            card.rect.center = (xpos, ypos)
            screen.blit(card.image, card.rect)
            xpos += 130
    elif num_cards == 12:
        xpos = 75
        ypos = 200
        for card in cards:
            card.rect.center = (xpos, ypos)
            screen.blit(card.image, card.rect)
            if xpos > 700:
                xpos = 75
                ypos += 200
            else:
                xpos += 130
    else:
        xpos = 75
        ypos = 200
        for card in cards:
            card.rect.center = (xpos, ypos)
            screen.blit(card.image, card.rect)
            if xpos > 700:
                xpos = 75
                ypos += 150
            else:
                xpos += 130

def reset_cards(cards, mode):
    for card in cards:
        if not card.solved:
            card.flipped = False
            if mode == 'red':
                card.image = pygame.image.load('cardback.jpg')
            elif mode == 'blue':
                card.image = pygame.image.load('bluecard.png')
            elif mode == 'black':
                card.image = pygame.image.load('blackcard.png')
            screen.blit(card.image, card.rect)

def num_solved(cards):
    counter = 0
    for card in cards:
        if card.solved:
            counter += 1
    return counter

pygame.init()
game_mode = 'start'
screen = pygame.display.set_mode((800, 600))
screen.fill('darkgreen')
background = pygame.image.load('table.jpg')
background = pygame.transform.scale(background, (800, 600))
screen.blit(background, (0,0))
pygame.display.set_caption('Memory Game')
clock = pygame.time.Clock()
reset = False

card_surf = pygame.image.load('cardback.jpg')
card_rect = card_surf.get_rect(center = (100, 100))

large_font = pygame.font.Font('font.ttf', 100)
small_font = pygame.font.Font('font.ttf', 50)
tiny_font = pygame.font.Font('font.ttf', 25)

moves_counter = 0
num_cards = 0
cards = []
card_values = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
cards_flipped = 0
stored_cards = [0,0]
reset = False
card_type = 'red'

while True:
    if (game_mode == 'play'):
        screen.blit(background, (0,0))
        place_cards(cards, num_cards)
        if moves_counter == 0:
            moves_tracker = large_font.render(f'Moves O',True ,'white')
        elif moves_counter % 10 == 0 and moves_counter != 0:
            moves_tracker = large_font.render(f'Moves {moves_counter // 10}O',True ,'white')
        else:
            moves_tracker = large_font.render(f'Moves {moves_counter}',True ,'white')
        screen.blit(moves_tracker, (200, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                card_num = verify_click(cards)
                if card_num != -1 and not cards[card_num].flipped:
                    flip(cards[card_num])
                    cards_flipped += 1
                    stored_cards[cards_flipped - 1] = cards[card_num]
                    if cards_flipped == 2:
                        pygame.display.update()
                        time.sleep(1)
                        moves_counter += 1
                        cards_flipped = 0
                        check_match(stored_cards[0], stored_cards[1])
                        reset_cards(cards, card_type)
                        stored_cards = [0,0]
                    if check_win(cards, num_cards):
                        game_mode = 'end'
    elif (game_mode == 'start'):
        if reset:
            moves_counter = 0
            num_cards = 0
            cards = []
            card_values = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
            cards_flipped = 0
            stored_cards = [0,0]
            reset = False
        screen.blit(background, (0,0))
        welcome_message = small_font.render(f'Welcome to Memory Match',True ,'white')
        screen.blit(welcome_message, (75, 25))

        easy_img = small_font.render('Easy',True ,'black')
        easy_rect = pygame.draw.rect(screen, (225,225,225), pygame.Rect(300, 125, 200, 100))
        screen.blit(easy_img,(345, 147))

        medium_img = small_font.render(f'Medium',True ,'black')
        medium_rect = pygame.draw.rect(screen, (225,225,225), pygame.Rect(300, 275, 200, 100))
        screen.blit(medium_img,(310, 295))

        hard_img = small_font.render(f'Hard',True ,'black')
        hard_rect = pygame.draw.rect(screen, (225,225,225), pygame.Rect(300, 425, 200, 100))
        screen.blit(hard_img,(342, 445))

        options_img = tiny_font.render('Options',True ,'black')
        options_rect = pygame.draw.rect(screen, (225,225,225), pygame.Rect(635, 515, 150, 75))
        screen.blit(options_img,(665, 540))
        buttons = [easy_rect, medium_rect, hard_rect, options_rect]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mode = verify_button(buttons)
                if mode != -1 and mode != 3:
                    num_cards = (mode + 1) * 6
                    card_values = card_values[:num_cards]
                    shuffle(card_values)
                    for i in range(num_cards):
                        cards.append(Card(card_values[i], card_type))
                    game_mode = 'play'
                elif mode == 3:
                    game_mode = 'setup'

    elif (game_mode == 'end'):
        screen.blit(background, (0,0))
        winner_img = large_font.render('Congrats!',True ,'yellow')
        screen.blit(winner_img,(170, 20))


        if moves_counter % 10 == 0 and moves_counter != 0:
            counter_img = small_font.render(f'You won in {moves_counter // 10}O moves!',True ,'white')
        else:
            counter_img = small_font.render(f'You won in {moves_counter} moves!',True ,'white')
        screen.blit(counter_img,(160, 135))

        replay_img = small_font.render(f'Replay?',True ,'black')
        replay_rect = pygame.draw.rect(screen, (225,225,225), pygame.Rect(300, 275, 200, 100))
        screen.blit(replay_img,(310, 295))
        buttons = [replay_rect]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if verify_button(buttons) == 0:
                    reset = True
                    game_mode = 'start'

    elif (game_mode == 'setup'):
        screen.blit(background, (0,0))
        return_img = tiny_font.render('Return',True ,'black')
        return_rect = pygame.draw.rect(screen, (225,225,225), pygame.Rect(635, 515, 150, 75))
        screen.blit(return_img,(670, 537))

        title_img = large_font.render('Options', True, 'white')
        screen.blit(title_img, (225, 0))

        red_card = pygame.image.load('cardback.jpg')
        screen.blit(red_card, (100, 200))
        blue_card = pygame.image.load('bluecard.png')
        screen.blit(blue_card, (350, 200))
        black_card = pygame.image.load('blackcard.png')
        screen.blit(black_card, (600, 200))

        red_img = tiny_font.render(f'Red',True ,'black')
        red_rect = pygame.draw.rect(screen, (225,225,225), pygame.Rect(100, 360, 100, 50))
        screen.blit(red_img,(130, 370))

        blue_img = tiny_font.render(f'Blue',True ,'black')
        blue_rect = pygame.draw.rect(screen, (225,225,225), pygame.Rect(350, 360, 100, 50))
        screen.blit(blue_img,(377, 370))

        black_img = tiny_font.render(f'Black',True ,'black')
        black_rect = pygame.draw.rect(screen, (225,225,225), pygame.Rect(600, 360, 100, 50))
        screen.blit(black_img,(620, 370))


        buttons = [return_rect, red_rect, blue_rect, black_rect]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mode = verify_button(buttons)
                if mode == 0:
                    game_mode = 'start'
                elif mode == 1:
                    card_type = 'red'
                elif mode == 2:
                    card_type = 'blue'
                elif mode == 3:
                    card_type = 'black'

    pygame.display.update()
    clock.tick(60)
