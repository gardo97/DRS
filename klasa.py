import pygame,sys
from podesavanja import *
from igrac import *
from igrac2 import *
from enemy import *

pygame.init()
vec=pygame.math.Vector2

class App:
    def __init__(self):
        pygame.display.set_caption('PACMAN DRS')
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock=pygame.time.Clock()
        self.running=True
        self.state='start'
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30
        self.walls = []
        self.coins=[]
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.p_pos2 = None
        self.load()
        self.igrac = Igrac(self, vec(self.p_pos))
        self.igrac2 = Igrac2(self,vec(self.p_pos2))
        self.make_enemies()
        self.konstanta = 2860
        self.nivo = 1

    def run(self):
        while self.running:
            if self.state=='start':
                self.start_events()
                self.start_azuriranje()
                self.start_crtanje()
            elif self.state=='playing':
                self.playing_events()
                self.playing_azuriranje()
                self.playing_crtanje()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_azuriranje()
                self.game_over_crtanje()
            elif self.state == 'next level':
                self.next_level()
                self.next_level_azuriranje()
                self.next_level_crtanje()
            else:
                self.running=False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

#####################################################################

    def draw_text(self,words,screen,pos,size,colour,font_name,centered=False):
        font=pygame.font.SysFont(font_name,size)
        text=font.render(words,False,colour)
        text_size=text.get_size()
        if centered:
            pos[0]=pos[0]-text_size[0]//2
            pos[1]=pos[1]-text_size[1]//2
        screen.blit(text,pos)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        #Otvaranje fajla zidovi

        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1" :
                      self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char == "L":
                        self.p_pos2 = [xidx,yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
                                                      self.cell_width, self.cell_height))
            #  print(len(self.walls))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background,  GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))
        #for coin in self.coins:
        #    pygame.draw.rect(self.background,  (115, 65, 185), (coin.x*self.cell_width, coin.y*self.cell_height, self.cell_width, self.cell_height))

    def reset(self):
        self.igrac.lives = 3
        self.igrac2.lives= 3
        self.igrac.current_score = 0
        self.igrac2.current_score= 0
        self.igrac.grid_pos = vec(self.igrac.starting_pos)
        self.igrac2.grid_pos=vec(self.igrac2.starting_pos)
        self.igrac.pix_pos = self.igrac.get_pix_pos()
        self.igrac2.pix_pos = self.igrac2.get_pix_pos()
        self.igrac.direction *= 0
        self.igrac2.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx,yidx))
        self.state = "playing"


#####################################################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                self.state='playing'

    def start_azuriranje(self):
        pass

    def start_crtanje(self):
        self.screen.fill(BLACK)
        self.draw_text('Klikni space za pocetak igre',self.screen,[WIDTH//2,HEIGHT//2-50],START_TEXT_SIZE,(170,132,58),START_FONT,centered=True)
        self.draw_text('Dva igraca',self.screen,[WIDTH//2,HEIGHT//2+50],START_TEXT_SIZE,(44,167,198),START_FONT,centered=True)
        pygame.display.update()

#####################################################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
            if event.type == pygame.KEYDOWN:
                if ((self.igrac.current_score+self.igrac2.current_score)% self.konstanta) == 0:
                    self.state="next level"
                    self.igrac.current_score+=10
                    self.igrac2.current_score+=10
                    self.konstanta+=2880
                    self.nivo+=1
                if event.key == pygame.K_LEFT:
                    self.igrac.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.igrac.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.igrac.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.igrac.move(vec(0, 1))
                if event.key == pygame.K_a:
                    self.igrac2.move(vec(-1,0))
                if event.key == pygame.K_d:
                    self.igrac2.move(vec(1, 0))
                if event.key == pygame.K_w:
                    self.igrac2.move(vec(0, -1))
                if event.key == pygame.K_s:
                    self.igrac2.move(vec(0, 1))


    def playing_azuriranje(self):
        self.igrac.update()
        self.igrac2.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.igrac.grid_pos:
                self.remove_life()
            elif enemy.grid_pos == self.igrac2.grid_pos:
                self.remove_life2()

    def playing_crtanje(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background,(TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        #self.draw_grid()
        self.draw_text('Nivo: {}'.format(self.nivo), self.screen, [WIDTH//2-30,HEIGHT-30], 18, WHITE, START_FONT, centered = False)
        self.draw_text('Zivoti IGRACA 1:', self.screen, [15, HEIGHT - 30], 18, WHITE, START_FONT, centered=False)
        self.draw_text('Zivoti IGRACA 2:', self.screen, [WIDTH//2+63, HEIGHT - 30], 18, WHITE, START_FONT, centered=False)
        self.draw_text('Trenutni skor: {}'.format(self.igrac.current_score), self.screen, [60,0], 18, WHITE, START_FONT, centered = False)
        self.draw_text('Trenutni skor 2: {}'.format(self.igrac2.current_score), self.screen, [WIDTH//2+60, 0], 18, WHITE, START_FONT, centered=False)
        self.igrac.draw()
        self.igrac2.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.igrac.lives -= 1
        if self.igrac.lives == 0:
            self.state = "game over"
        else:
            self.igrac.grid_pos = vec(self.igrac.starting_pos)
            self.igrac.pix_pos = self.igrac.get_pix_pos()
            self.igrac.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def remove_life2(self):
        self.igrac2.lives -= 1
        if self.igrac2.lives == 0:
            self.state = "game over"
        else:
            self.igrac2.grid_pos = vec(self.igrac2.starting_pos)
            self.igrac2.pix_pos = self.igrac2.get_pix_pos()
            self.igrac2.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    ##################################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_azuriranje(self):
        pass

    def game_over_crtanje(self):
        self.screen.fill(BLACK)
        if (self.igrac2.current_score > self.igrac.current_score):
            self.draw_text("GAME OVER",self.screen,[WIDTH//2,100],52,RED,"arial",centered=True)
            self.draw_text("Pobednik:IGRAC 2", self.screen, [WIDTH // 2, 150], 46, RED, "arial", centered=True)
        elif (self.igrac2.current_score == self.igrac.current_score):
            self.draw_text("GAME OVER",self.screen,[WIDTH//2,100],52,RED,"arial",centered=True)
            self.draw_text("Pobednik:Nereseno", self.screen, [WIDTH // 2, 150], 46, RED, "arial", centered=True)
        else:
            self.draw_text("GAME OVER",self.screen,[WIDTH//2,100],52,RED,"arial",centered=True)
            self.draw_text("Pobednik:IGRAC 1", self.screen, [WIDTH // 2, 150], 46, RED, "arial", centered=True)

        self.draw_text("Klikni escape da izadjes iz igre",self.screen,[WIDTH//2,HEIGHT//1.5],36,(190,190,190),"arial",centered=True)
        self.draw_text("Klikni space da ponovo igras",self.screen,[WIDTH//2,HEIGHT//2],36,(190,190,190),"arial",centered=True)
        pygame.display.update()

    #####################################################

    def next_level(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key== pygame.K_SPACE:
                self.reset2()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def next_level_azuriranje(self):
        pass

    def next_level_crtanje(self):
        self.screen.fill(BLACK)
        self.draw_text("Presli ste nivo", self.screen, [WIDTH // 2, 100], 52, RED, "arial", centered=True)
        self.draw_text("Klikni escape da izadjes iz igre", self.screen, [WIDTH // 2, HEIGHT // 1.5], 36,
                       (190, 190, 190), "arial", centered=True)
        self.draw_text("Klikni space za sledeci nivo", self.screen, [WIDTH // 2, HEIGHT // 2], 36, (190, 190, 190),
                       "arial", centered=True)
        pygame.display.update()

    def reset2(self):
        self.igrac.lives = 3
        self.igrac2.lives = 3
        self.igrac.grid_pos = vec(self.igrac.starting_pos)
        self.igrac2.grid_pos = vec(self.igrac2.starting_pos)
        self.igrac.pix_pos = self.igrac.get_pix_pos()
        self.igrac2.pix_pos = self.igrac2.get_pix_pos()
        self.igrac.direction *= 0
        self.igrac2.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0
            ##################enemy.speed += 0.1

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"