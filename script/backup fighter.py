import pygame

class Fighter():


    def __init__(self,x,y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.vel_x = 200
        self.jump = False
        self.dash = False
        self.dash_checker_right = 0
        self.dash_checker_left = 0
        self.state = 'move'
        self.check_right = False
        self.check_left = False
        
    def move(self, screen_width, screen_height):
        speed = 10
        adjust_speed = 30
        gravity = 2
        dx = 0
        dy = 0

        #getinput 
        key = pygame.key.get_pressed()
        print( self.rect.x, self.rect.y, self.dash, self.dash_checker_left, self.dash_checker_right, self.state)


        #movement
        if self.state == 'move':
            if key[pygame.K_a]:
                dx = -speed
                self.check_left = False
                self.check_right = True

            if key[pygame.K_d]:
                dx = speed
                self.check_left = True
                self.check_right = False

        #jump
        if key[pygame.K_w] and self.state != 'jump':
            self.state = 'jump'

        if key[pygame.K_w] and self.state == 'jump' and self.jump == False:
            self.vel_y = -30
            self.jump = True
            
            
        #apply gravity
        self.vel_y += gravity
        dy += self.vel_y


        #dash
        if key[pygame.K_SPACE] and self.state != 'dash':
            self.state == 'dash'
            if key[pygame.K_SPACE]and self.state == 'dash' and self.dash == False:
                if self.check_right == False and self.check_left == False:
                    dx = speed - speed
                elif self.check_right == True and self.check_left == False:
                    dx = speed - (adjust_speed * 2)
                    self.dash_checker_left += dx
                    self.dash == True 
                elif self.check_left == True and self.check_right == False:
                    dx = speed + adjust_speed
                    self.dash_checker_right += dx
                    self.dash == True 
                else:
                    dx = speed - speed           
            
            

        #control player on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.state = 'move'
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        if self.dash_checker_right == 200:
            self.dash_checker_right = 0
            self.rect.x += dx
            self.dash = False
        if self.dash_checker_left == -200:
            self.dash_checker_left = 0
            self.rect.x += dx
            self.dash = False

        #if self.dash_checker_left < -200:
    
            #self.dash = False
            #self.state = 'move'


       # if dx != speed:
            #self.dash = 0

        self.rect.x += dx

        self.rect.y += dy            


    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

