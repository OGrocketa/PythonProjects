import pygame
from sys import exit
from random import randint,choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load("Graphics/Player/player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("Graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load("Graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "fly":
            fly_frame_1 = pygame.image.load("Graphics/Fly/Fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("Graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load("Graphics/Snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("Graphics/Snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= obstacles_speed
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks()/100 - start_time)
    score_surf = test_font.render(f"Score: {current_time}",False,(64,64,64))
    score_rect = score_surf.get_rect(center = (SCREEN_WIDTH/2,50))
    screen.blit(score_surf,score_rect)
    return current_time




def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FRAME_RATE = 60
game_active = False
start_time = 0
score = 0
obstacles_speed = 15
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("DA PUNK RUNNA")
clock = pygame.time.Clock()
test_font = pygame.font.Font("Fonts/slkscr.ttf",50)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()



sky_surf = pygame.image.load("Background/Sky.png").convert_alpha()
ground_surf = pygame.image.load("Background/ground.png").convert_alpha()

sky_width, sky_height = sky_surf.get_size()


#Intro Screen
player_stand = pygame.image.load("Graphics/Player/player_stand.png")
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

game_name = test_font.render("Da PUNK RUNNA", False, (111,196,169))
game_name_rect = game_name.get_rect(center = (SCREEN_WIDTH/2,80))

game_instruction = test_font.render("Press SPACE to start", False, (111,196,169))
game_instruction_rect = game_instruction.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT-80))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
            
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)

    if game_active:
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf,(0,sky_height))

        score = display_score()

        #Player
        player.draw(screen)
        player.update()

        #Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        #Collision
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name,game_name_rect)
        
        player_gravity = 0

        if score > 0:
            score_text = test_font.render(f"Score: {score}",False, (111,196,169))
            score_text_rect = score_text.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT-80))
            screen.blit(score_text,score_text_rect)
        else:
            screen.blit(game_instruction,game_instruction_rect)


    pygame.display.update()
    clock.tick(FRAME_RATE)