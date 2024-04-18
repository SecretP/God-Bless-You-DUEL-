import pygame
#import subsurface

class Fighter():


    def __init__(self, player, x, y, data, sprite_sheet, animation_steps, damage_1, damage_2, atk_01_fx, atk_02_fx, hit_fx):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False
        self.animation_list = self.load_image(sprite_sheet, animation_steps)
        self.state = 0 #0:idle 1:run 2:jump 3:attack_1 4:attack_2 5:hit 6:death *****number is row******
        self.frame_index = 0
        self.image = self.animation_list[self.state][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.dash = False
        self.check_right = False
        self.check_left = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 1
        self.attack_damage_1 = damage_1
        self.attack_damage_2 = damage_2
        self.health = 100
        self.dash_cooldown = 0
        self.hit = False
        self.alive = True
        self.atk_01_fx = atk_01_fx
        self.atk_02_fx = atk_02_fx
        self.hit_fx = hit_fx


    def load_image(self, sprite_sheet, animation_steps):
        #extract images from sprite
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)  
        return animation_list
        
    def move(self, screen_width, screen_height, surface, target, round_over):
        speed = 9
        adjust_speed = 30
        gravity = 2
        dx = 0
        dy = 0
        floor_distance = 20
        self.running = False
        self.attack_type = 0


        #getinput 
        key = pygame.key.get_pressed()
    
        #can only perform other action if not currently attacking
        if self.attacking == False and self.hit == False and self.alive == True and round_over == False:
            #check player 1 controls
            if self.player == 1:
                #movement
                if key[pygame.K_a]:
                    dx = -speed
                    #facing_right
                    self.check_left = False
                    self.check_right = True
                    self.running = True

                if key[pygame.K_d]:
                    dx = speed
                    #facing_left
                    self.check_left = True
                    self.check_right = False
                    self.running = True
                    
                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
    #                self.dash_cooldown -= 50
    #                print(self.dash_cooldown)
                
                #attack
                if key[pygame.K_SPACE] or key[pygame.K_r]:
                    
                    #determine which attack type was used
                    if key[pygame.K_SPACE]:
                        self.attack_type = 1    
                        self.attack(target, self.attack_damage_1) #surface come with hitbox
                        self.atk_01_fx.play()

                    if key[pygame.K_r]:
                        self.attack_type = 2
                        self.attack(target, self.attack_damage_2) #surface come with hitbox
                        self.atk_02_fx.play()

                #dash
    #            if key[pygame.K_LCTRL]:
    #               self.dash_cooldown -= 50
    #                if self.check_right == True and self.check_left == False and self.dash_cooldown < 100:
    #                    dx = speed
    #                elif self.check_right == True and self.check_left == False and self.dash == True and self.dash_cooldown == 100:
    #                    dx = 1 * (speed + (adjust_speed*4))
    #                    #self.dash = False
    #                    self.dash_cooldown -= 50
    #                elif self.check_right == False and self.check_left == True and self.dash == True and self.dash_cooldown == 100:
    #                    dx = -1 * (speed + (adjust_speed*2))
    #                    self.dash_cooldown -= 50
    #                    #self.dash = False
    #                elif self.check_right == False and self.check_left == True and self.dash_cooldown < 100:
    #                    dx = -speed
            
            #check player 2 controls
            elif self.player == 2:
                #movement
                if key[pygame.K_LEFT]:
                    dx = -speed
                    #facing_right
                    self.check_left = False
                    self.check_right = True
                    self.running = True

                if key[pygame.K_RIGHT]:
                    dx = speed
                    #facing_left
                    self.check_left = True
                    self.check_right = False
                    self.running = True
                    
                #jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
    #                self.dash_cooldown -= 50
    #                print(self.dash_cooldown)
                
                #attack
                if key[pygame.K_KP1] or key[pygame.K_KP3]:
                    #determine which attack type was used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                        self.attack(target, self.attack_damage_1) #surface come with hitbox
                        self.atk_01_fx.play()
                       # self.attack(target, self.attack_damage_1) #surface come with hitbox
      
                    if key[pygame.K_KP3]:
                        self.attack_type = 2
                        self.attack(target, self.attack_damage_2) #surface come with hitbox
                        self.atk_02_fx.play()
                    
                
                

#        if self.dash_cooldown == 0:
#            self.dash = False           
#        self.dash_cooldown += 10
#        if self.dash_cooldown > 100:
#            self.dash = True
#            self.dash_cooldown = 100
#            print(self.dash_cooldown)
#        if self.dash_cooldown < 0:
#            self.dash_cooldown = 0
#            self.dash = False
#            print(self.dash_cooldown)


        #apply gravity
        self.vel_y += gravity
        dy += self.vel_y



        #lock player on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - floor_distance:  
            self.vel_y = 0
            self.jump = False
            dy = screen_height - floor_distance - self.rect.bottom

        #confirm left or right
        if self.check_right == True and self.check_left == False:
            self.flip = True
        elif self.check_left == True and self.check_right == False:
            self.flip = False

        if self.attack_cooldown > 0:
            self.attack_cooldown -=1    

       # if dx != speed:
            #self.dash = 0
        self.rect.x += dx
        self.rect.y += dy         


    #animation update
    def update(self):
        #check what state player perform
        if self.health <=0:
            self.health = 0
            self.alive = False
            self.update_state(6)
        elif self.hit == True:
            self.update_state(5)
            #self.hit_fx.play()
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_state(3)
            elif self.attack_type == 2:
                self.update_state(4)    
        elif self.jump == True:
            self.update_state(2)
        elif self.running == True:
            self.update_state(1)
        else:
            self.update_state(0)

        animation_cooldown = 40 
        #update image
        self.image = self.animation_list[self.state][self.frame_index]
        #check if enough time has passed since the last updtate
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.state]):
            #self.before_hit =  len(self.animation_list[self.state]) - 1
            #if the player is death then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.state]) - 1
            else: 
                self.frame_index = 0
                #check if an attack was executed
                if self.state == 3 or self.state == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                #Check if damage was taken
                if self.state == 5:
                    self.hit = False
                    #if the player was in the middle of an attack  
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, target, damage): #surface come with hitbox
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                print("hit")
                target.health -= damage
                target.hit = True
            #hide hitbox# pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_state(self, new_state):
        #check is a new state if different to the previous one
        if new_state != self.state:
            self.state = new_state
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
#    def dash(self, surface)
#        self.dash = True
#        if self.check_right == False and self.check_left == False:
#            dx = speed - speed
#        elif self.check_right == True and self.check_left == False:
#            dx = speed - (adjust_speed+ 30)
#        elif self.check_left == True and self.check_right == False:
#            dx = speed + adjust_speed
#       else:
#           dx = speed - speed


    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #hide hitbox# pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

        