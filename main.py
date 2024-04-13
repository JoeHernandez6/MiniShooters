import pygame
import levels
import math
pygame.init()

current_time=int(pygame.time.get_ticks()/1000)
LVL1=levels.level_1
LVL1_BOSS=levels.main_boss
LVL1_END=levels.end
tile_size=64#"C:\Users\xxsharkyxx1234\OneDrive\Documents\Mini_Shooter\sprites"
penguin_misile_left=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites\penguin_misile_left.png")
penguin_misile_right= pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/penguin_misile_right.png")
turtle_misile_left=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/turtle_misile_left.png")
turtle_misile_right=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/turtle_misile_right.png")
penguin_left_image=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/penguin_walk_left.png")
penguin_left_image=pygame.transform.scale(penguin_left_image, (tile_size-10, tile_size-10))
penguin_right_image= pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/penguin_walk_right.png")
penguin_right_image=pygame.transform.scale(penguin_right_image, (tile_size-5, tile_size-10))
turtle_left_image=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/turtle_walk_left.png")
turtle_left_image=pygame.transform.scale(turtle_left_image, (tile_size-10, tile_size-10))
turtle_right_image=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/turtle_walk_right.png")
turtle_right_image=pygame.transform.scale(turtle_right_image, (tile_size-10, tile_size-10))

lvl_list=[LVL1,LVL1_BOSS,LVL1_BOSS]
lvl=1
windowX=1280
windowY=704
window=pygame.display.set_mode((windowX,windowY))
pygame.display.set_caption('Mini Shooters')
ice_background=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/snowy_mountains.jpg")
ice_background=pygame.transform.scale(ice_background,(windowX,windowY))
font=pygame.font.Font('OneDrive\Documents\Mini_Shooter\Smoothy Butter.otf', 128)

WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
GRAY=(122,122,122)
VIOLET=(238,130,238)
clock=pygame.time.Clock()
fps=40
steps=13
backwardx_wall=200
forwardx_wall=1080
main_group=pygame.sprite.Group()
plataform_group=pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_list= pygame.sprite.Group()
enemy_list= pygame.sprite.Group()
explosion_list=pygame.sprite.Group()
portal_list=pygame.sprite.Group()
enemy_bullet_list=pygame.sprite.Group()
end_text_list=pygame.sprite.Group()

class Time_text(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        formatted_time = "{:02d}:{:02d}".format(minutes, seconds)
        self.sentence=f"{formatted_time}"
        self.text=font.render(self.sentence, True, VIOLET)
    def update(self):
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        formatted_time = "{:02d}:{:02d}".format(minutes, seconds)
        self.sentence=f"{formatted_time}"
        self.text=font.render(self.sentence, True, VIOLET)
        window.blit(self.text, (510,0))


class end_text(pygame.sprite.Sprite):
    def __init__(self,int):
        super().__init__()
        if int==1:
            self.text=font.render("you beat the game", True, VIOLET, BLACK)
            self.rect=self.text.get_rect()
            self.rect.center = (windowX / 2, (windowY / 2)-100)
        elif int ==2:
            self.text=font.render(f"Time: {end_time}", True, VIOLET, BLACK)
            self.rect=self.text.get_rect()
            self.rect.center = (windowX / 2, (windowY / 2)+100)
        end_text_list.add(self)

    def update(self):
        window.blit(self.text, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,right_image,left_image):
        super().__init__()
        self.right_image=right_image
        self.left_image=left_image
        self.image=self.right_image
        self.rect= self.image.get_rect()
        self.distanceX=0
        self.distanceY=0
        self.right_dir=True
        self.is_colliding=False
        self.rect.x=x
        self.rect.y=y
        self.restart=False
        self.reload_time=int(pygame.time.get_ticks()/1000)-3
        self.shoot=True
        
        
    def gravity(self):
        if self.rect.y > windowY and self.distanceY > 0:
            self.distanceY = 0
            self.rect.y = windowY - self.rect.height
        else:
            self.distanceY += 3
    def move(self,x,y):
        self.distanceX+=x
        self.distanceY+=y
        if self.distanceX<0:
            self.image=self.left_image
            self.right_dir=False
        if self.distanceX>0:
            self.image=self.right_image
            self.right_dir=True
            
    
    def jump(self):
        if self.is_colliding:
            self.distanceY -= 32
            self.is_colliding = False
    def update(self,current_time):
        self.rect.x+=self.distanceX
        self.rect.y+=self.distanceY
        plat_collide=pygame.sprite.spritecollide(self,plataform_group,False)
        for plat in plat_collide:
            if self.distanceY > 0:
                self.distanceY = 0
                self.rect.bottom = plat.rect.top
            elif self.distanceY < 0:
                self.rect.top = plat.rect.bottom
                self.distanceY = 0
            self.is_colliding = True
        for plat in plataform_group:
            if plat.rect.colliderect(self.rect.x - steps, self.rect.y , self.rect.width, self.rect.height):
                if self.distanceX < 0:
                    self.rect.left = plat.rect.right + steps
            elif plat.rect.colliderect(self.rect.x + steps, self.rect.y,self.rect.width, self.rect.height):
                if self.distanceX > 0:
                    self.rect.right = plat.rect.left - steps
        reload_rect=pygame.draw.rect(window,BLACK,(self.rect.x+2,self.rect.y-25,50,10))
        if current_time-self.reload_time>=3:
            self.shoot=True
            time_rect=pygame.draw.rect(window,WHITE,(self.rect.x+2,self.rect.y-25,50,10))
        else:
            self.shoot=False
            time_rect=pygame.draw.rect(window,WHITE,(self.rect.x+2,self.rect.y-25,(50/3)*(current_time-self.reload_time),10))



    
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,main_list,sub_list,image_int):
        super().__init__()
        if image_int ==1:
            ground_pic=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/ground.png")
            self.image=pygame.transform.scale(ground_pic,(tile_size,tile_size))
            sub_list.add(self)
        elif image_int== 2:
            grass_pic=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/grass.png")
            self.image=pygame.transform.scale(grass_pic,(tile_size,tile_size))
            sub_list.add(self)
        self.rect=self.image.get_rect()
        self.rect.y=y
        self.rect.x=x
        main_list.add(self)
def create_world(map):
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == 1:
                Platform(col * tile_size,row*tile_size,main_group,plataform_group,1)
            elif map[row][col] == 2:
                Platform(col * tile_size,row*tile_size,main_group,plataform_group,2)
            elif map[row][col]==3:
                global penguin
                penguin= Player(col * tile_size, row * tile_size,penguin_right_image,penguin_left_image)
                player_group.add(penguin)
            elif map[row][col]==4:
                global turtle
                turtle= Player(col * tile_size, row * tile_size,turtle_right_image,turtle_left_image)
                player_group.add(turtle)
            
            elif map[row][col] == 5:
                Enemy(col*tile_size,row*tile_size, 5,100,False)

            elif map[row][col]==7:
                global ninja_boss
                ninja_boss=Ninja_Boss(col*tile_size,row*tile_size)

            else:
                pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self,dir,spawn,player):
        super().__init__()
        self.direction=dir
        if self.direction=="right"and player=="penguin":
            self.image=pygame.transform.scale(penguin_misile_right,(40,20))
        elif self.direction=='left' and player=="penguin":
            self.image=pygame.transform.scale(penguin_misile_left,(40,20))
        elif self.direction=="right"and player=="turtle":
            self.image=pygame.transform.scale(turtle_misile_right,(40,20))
        elif self.direction=="left"and player=="turtle":
            self.image=pygame.transform.scale(turtle_misile_left,(40,20))
        
        self.rect=self.image.get_rect()
        self.rect.x=spawn[0]
        self.rect.y=spawn[1]
        bullet_list.add(self)
    def update(self):
        if self.direction=="left":
            self.rect.x-=20
        elif self.direction == "right":
            self.rect.x+=20
        if self.rect.x< -23 or self.rect.x>windowX+23:
            self.kill()
class Enemy(pygame.sprite.Sprite):
  def __init__(self, x, y, image_int,distance,enemybullet):
    super().__init__()
    if image_int == 5:
      self.left=pygame.image.load('OneDrive\Documents\Mini_Shooter\sprites/camel_left_walk.png')
      self.left = pygame.transform.scale(self.left, (tile_size, tile_size))
      self.right=pygame.image.load('OneDrive\Documents\Mini_Shooter\sprites/camel_right_walk.png')
      self.right = pygame.transform.scale(self.right, (tile_size, tile_size))
      self.image = self.left
      self.enemy_bullet_demage=enemybullet

     
    #load more enemy pics later
  
    self.rect = self.image.get_rect() # Set a reference to the image rect
    self.rect.x = x 
    self.rect.y = y 
    
    #Track distance traveled by enemy
    self.travel_x = 0 # travel along X
    self.travel_y = 0 # travel along Y
    #add a collision detection variable
    self.is_colliding = False
    enemy_list.add(self)
    #add variable to keep track of how many steps enemy moves
    self.enemySteps = 0
    self.distance=distance


  #update enemy position
  def update(self):
    global explosion
    if self.enemy_bullet_demage==True:
        for bullet in enemy_bullet_list:
            if bullet.int==2:
                if pygame.sprite.collide_rect(self,bullet):
                    
                    bullet.kill()
                    explosion=Explosion(self.rect.x,self.rect.y)
                    self.kill()
    for bullet in bullet_list:
        if pygame.sprite.spritecollide(bullet, enemy_list, True):
            
            if bullet.direction=="right":
                explosion=Explosion(bullet.rect.x-(bullet.rect.width/10) ,bullet.rect.topright[1]-bullet.rect.height)
            if bullet.direction=="left":
                explosion=Explosion(bullet.rect.x-(bullet.rect.width/2) ,bullet.rect.topright[1]-bullet.rect.height)
            bullet.kill()
        
    self.rect.x += self.travel_x
    self.rect.y += self.travel_y
    distance = self.distance
    speed = 4

    if 0 <= self.enemySteps <= distance/2:
      self.image=self.right
      self.travel_x = speed
    
    elif distance/2 <= self.enemySteps < distance:
      self.image=self.left
      self.travel_x = -speed
    else:
      self.enemySteps = 0

    self.enemySteps += 1

    

    plat_collide = pygame.sprite.spritecollide(self, plataform_group, False)
    for plat in plat_collide:
      if self.travel_y > 0:
        self.travel_y = 0
        self.rect.bottom = plat.rect.top
    for plat in plataform_group:
      if plat.rect.colliderect(self.rect.x - speed, self.rect.y, self.rect.width, self.rect.height):
        if self.travel_x < 0:
          self.rect.left = plat.rect.right + speed
          self.enemySteps = 0     
      elif plat.rect.colliderect(self.rect.x + speed, self.rect.y, self.rect.width, self.rect.height): 
        if self.travel_x > 0:
          self.rect.right = plat.rect.left - speed
          self.enemySteps = 1 + distance/2

  #Track new ENEMY position on the y-axis to show gravity effect
    self.rect.y += self.travel_y
    
  #enemy gravity code 
    if self.rect.y > windowY and self.travel_y > 0:
      self.travel_y = 0
      self.rect.y = windowX - self.rect.height
    else:
      self.travel_y += 3     
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/colliding_explosion.png")
        self.image=pygame.transform.scale(self.image,(tile_size,tile_size))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.time_start=int(pygame.time.get_ticks()/1000)
        explosion_list.add(self)
    def update(self,current_time):
        if current_time-self.time_start>=2:
            self.kill()
        else:
            pass
    
class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/portal.png")
        self.image=pygame.transform.scale(self.image, (tile_size,tile_size*2))
        self.rect=self.image.get_rect()
        self.map=lvl_list[lvl-1]
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == 6:
                    self.rect.x=col*tile_size+full_scroll
                    self.rect.y=row*tile_size
                else:
                    continue
        portal_list.add(self)
    def update(self):
        n=0
        for player in player_group:
            if pygame.sprite.spritecollide(player, portal_list, False):
                n+=1
        if n==2:
                for player in player_group:
                    player.kill()
                for enemy in enemy_list:
                    enemy.kill()
                for tile in main_group:
                    tile.kill()
                for explosion in explosion_list:
                    explosion.kill()
                global lvl
                lvl+=1
                create_world(lvl_list[lvl-1])
                global full_scroll
                full_scroll=0
                for p in player_group:
                    p.restart=True
                enemy_list.draw(window)
                self.kill()
        else:
            pass
class Ninja_Boss(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.health=20
        self.image_left=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/ninja_left.png")
        self.image_left=pygame.transform.scale(self.image_left,(tile_size,tile_size))
        self.image_right=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/ninja_right.png")
        self.image_right=pygame.transform.scale(self.image_right,(tile_size,tile_size))
        self.image=self.image_left
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.dir="left"
        self.shoot_time=int(pygame.time.get_ticks()/1000)-4
        self.star_time=int(pygame.time.get_ticks()/1000)-2
        self.camel_time=int(pygame.time.get_ticks()/1000)-3
        self.heal_time=int(pygame.time.get_ticks()/1000)
        self.heal_turns=0
        self.is_colliding = True
        enemy_list.add(self)
        self.distanceY=0
    def attack(self):
        if self.dir == "right":
            for player in player_group:
                
                Ninja_bullets(player.rect.x,0-tile_size-5,2,"right")
        elif self.dir == "left":
            for player in player_group:
                
                Ninja_bullets(player.rect.x,0-tile_size-5,2,"left")
            self.star_time=int(pygame.time.get_ticks()/1000)


    def shoot(self):
        if self.dir == "right":
            
            Ninja_bullets(self.rect.midright[0],self.rect.midright[1],1,"right")
        elif self.dir == "left":
            
            Ninja_bullets(self.rect.midleft[0],self.rect.midleft[1],1,"left")
        self.shoot_time=int(pygame.time.get_ticks()/1000)
    
    def camel(self):
        Enemy(self.rect.topleft[0]-tile_size+4,self.rect.topleft[1],5,16*64,True)
        self.camel_time=int(pygame.time.get_ticks()/1000)

    def heal(self):
        
        self.health+=(1000/60)/1000
        self.heal_turns-=1
        if self.heal_turns==0:
            self.heal_time=int(pygame.time.get_ticks()/1000)



    def update(self):
        self.rect.y+=self.distanceY
        if current_time-self.shoot_time>=5:
            self.shoot()
        if current_time-self.star_time>=5:
            self.attack()
        if current_time-self.camel_time>=5:
            self.camel()
        if current_time-self.heal_time>=20 and self.heal_turns==0:
            self.heal_turns=120
        if self.heal_turns!=0:
            self.heal()
        
        
        plat_collide=pygame.sprite.spritecollide(self,plataform_group,False)
        for plat in plat_collide:
            for plat in plat_collide:
                if self.distanceY > 0:
                    self.distanceY = 0
                    self.rect.bottom = plat.rect.top

        self.rect.y+=self.distanceY

        if self.rect.y > windowY and self.distanceY > 0:
            self.distanceY = 0
            self.rect.y = windowY - self.rect.height
        else:
            self.distanceY += 3
        for bullet in bullet_list:
            bullet_collision= pygame.sprite.spritecollide(self, bullet_list, False)
            for collision in bullet_collision:
                self.health-=1
                bullet.kill()
        if self.health<=0:
            self.kill()
        if self.health>=25:
            self.health=25
        rect=pygame.draw.rect(window,WHITE,(self.rect.x-18,self.rect.y-25,100,10))
        if self.heal_turns==0:
            health_rect=pygame.draw.rect(window,GREEN,(self.rect.x-18,self.rect.y-25,(100/20)*self.health,10))
        else:
            health_rect=pygame.draw.rect(window,VIOLET,(self.rect.x-18,self.rect.y-25,(100/20)*self.health,10))


        
            

class Ninja_bullets(pygame.sprite.Sprite):
    def __init__(self,x,y,int,dir):
        super().__init__()
        if int==1:
            self.dir=dir
            self.image=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/ninja_bullet.png")
            self.image=pygame.transform.scale(self.image, (40,20))
            self.rect=self.image.get_rect()
            self.rect.x=x
            self.rect.y=y
            self.int=1
        elif int==2:
            self.ninja_star_1=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/ninja_star.png")
            self.ninja_star_1=pygame.transform.scale(self.ninja_star_1,(tile_size,tile_size))
            self.ninja_star_2=pygame.image.load("OneDrive\Documents\Mini_Shooter\sprites/sideways_ninja_star.png")
            self.ninja_star_2=pygame.transform.scale(self.ninja_star_2,(tile_size,tile_size))
            self.image_list=[self.ninja_star_1,self.ninja_star_2]
            self.int=2
            self.case=0
            self.image=self.image_list[self.case]
            self.rect=self.image.get_rect()
            self.rect.x=x
            self.rect.y=y
        enemy_bullet_list.add(self)
    def update(self):
        global explosion
        if self.int==1:
            if self.dir=="left":
                self.rect.x-=20
            elif self.dir== "right":
                self.rect.x+=20
            if self.rect.x< -23 or self.rect.x>windowX+23:
                self.kill()
            collision=pygame.sprite.spritecollide(self, plataform_group, False)
            for collision in collision:
                if self.dir=="right":
                    explosion=Explosion(self.rect.x-(self.rect.width/10) ,self.rect.topright[1]-self.rect.height)
                if self.dir=="left":
                    
                    explosion=Explosion(self.rect.x-(self.rect.width/2) ,self.rect.topright[1]-self.rect.height)
                self.kill()
            
        elif self.int==2:
            self.image=self.image_list[self.case]
            self.rect.y+=5
            if self.rect.y>windowY+tile_size+5:
                self.kill()
            collision=pygame.sprite.spritecollide(self, plataform_group, False)
            for collision in collision:
                explosion=Explosion(self.rect.center[0] ,self.rect.center[1])
                self.kill()
            self.case+=1
            if self.case>=2:
                self.case-=self.case
            


                



        

        
full_scroll=0
time_text=Time_text()
create_world(lvl_list[lvl-1])
end=False
game=True
projectile=False
while game:
    if end!=True:
        window.blit(ice_background,(0,0))
        current_time=int(pygame.time.get_ticks()/1000)
        time_text.update()
        for player in player_group:
            if player.rect.y>windowY:
                for player in player_group:
                    # player.move(-player.distanceX,0)
                    player.kill()
                for enemy in enemy_list:
                    enemy.kill()
                for bullet in enemy_bullet_list:
                    bullet.kill()
                for tile in main_group:
                    tile.kill()
                for explosion in explosion_list:
                    explosion.kill()
                for portal in portal_list:
                    portal.kill()
                lvl=1
                create_world(LVL1)
                full_scroll=0
                for p in player_group:
                    p.restart=True
                enemy_list.draw(window)
            if player.rect.x <= backwardx_wall:
                scroll = backwardx_wall - player.rect.x
                full_scroll+=backwardx_wall - player.rect.x
                player.rect.x = backwardx_wall
                for p in plataform_group:
                    p.rect.x += scroll
                for p in enemy_list:
                    p.rect.x += scroll
                for p in enemy_bullet_list:
                    p.rect.x += scroll
                for p in explosion_list:
                    p.rect.x += scroll
                for p in portal_list:
                    p.rect.x += scroll
                for p in player_group:
                    if p!=player:
                        p.rect.x+=scroll
            if player.rect.x >= forwardx_wall:
                scroll = forwardx_wall - player.rect.x
                full_scroll+= forwardx_wall - player.rect.x
                player.rect.x = forwardx_wall
                for p in plataform_group:
                    p.rect.x += scroll
                for p in enemy_list:
                    p.rect.x += scroll
                for p in enemy_bullet_list:
                    p.rect.x += scroll
                for p in explosion_list:
                    p.rect.x += scroll
                for p in portal_list:
                    p.rect.x += scroll
                for p in player_group:
                    if p!=player:
                        p.rect.x+=scroll
        main_group.draw(window)
        if len(enemy_list) == 0 and len(portal_list)==0:
            n=0
            for row in range(len(lvl_list[lvl-1])):
                for col in range(len(lvl_list[lvl-1][row])):
                    if lvl_list[lvl-1][row][col]==6:
                        n+=1
            if n==0:
                pass
            else:
                portal= Portal()
        for portal in portal_list:
            portal.update()
        portal_list.draw(window)
        for bullet in bullet_list:
            bullet_plat_collision=pygame.sprite.spritecollide(bullet, plataform_group, False)
            for collision in bullet_plat_collision:
                if bullet.direction=="right":
                    explosion=Explosion(bullet.rect.x-(bullet.rect.width/10) ,bullet.rect.topright[1]-bullet.rect.height)
                if bullet.direction=="left":
                    explosion=Explosion(bullet.rect.x-(bullet.rect.width/2) ,bullet.rect.topright[1]-bullet.rect.height)
                bullet.kill()
            bullet.update()
        bullet_list.draw(window)
        for enemy in enemy_list:
            enemy.update()
        enemy_list.draw(window)
        for player in player_group:
            bullet_collision=pygame.sprite.spritecollide(player, enemy_bullet_list, False)
            for collision in bullet_collision:
                for player in player_group:
                    # player.move(-player.distanceX,0)
                    player.kill()
                for enemy in enemy_list:
                    enemy.kill()
                for bullet in enemy_bullet_list:
                    bullet.kill()
                for tile in main_group:
                    tile.kill()
                for explosion in explosion_list:
                    explosion.kill()
                for portal in portal_list:
                    portal.kill()
                lvl=1
                create_world(LVL1)
                full_scroll=0
                for p in player_group:
                    p.restart=True
                enemy_list.draw(window)

        for bullet in enemy_bullet_list:
            bullet.update()
        enemy_bullet_list.draw(window)
        for p in player_group:
            p.gravity()
            
            collision= pygame.sprite.spritecollide(p, enemy_list, False)
            for collisions in collision:
                for player in player_group:
                    # player.move(-player.distanceX,0)
                    player.kill()
                for enemy in enemy_list:
                    enemy.kill()
                for bullet in enemy_bullet_list:
                    bullet.kill()
                for tile in main_group:
                    tile.kill()
                for explosion in explosion_list:
                    explosion.kill()
                for portal in portal_list:
                    portal.kill()
                lvl=1
                create_world(LVL1)
                full_scroll=0
                for p in player_group:
                    p.restart=True
                enemy_list.draw(window)
            p.update(current_time)
        for player in player_group:
            if player.restart == True:
                player.move(-player.distanceX,0)
            restart=False
        player_group.draw(window)
        for e in explosion_list:
            e.update(current_time)
        if lvl==3:
            end_time=int(pygame.time.get_ticks()/1000)
            minutes = int(end_time // 60)
            seconds = int(end_time % 60)
            formatted_time = "{:02d}:{:02d}".format(minutes, seconds)
            end_time=formatted_time
            text=end_text(1)
            text=end_text(2)
            end=True
        explosion_list.draw(window)
        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                game==False
            if event.type == pygame.KEYDOWN:
                if event.key == ord("q"):
                   pygame.quit()
                   game==False
                if event.key == ord("a"):
                    penguin.move(-steps,0)
                
                if event.key == ord("d"):
                    penguin.move(steps,0)
                if event.key == ord("w"):
                    penguin.jump()

                if event.key == ord("s"):
                    if penguin.shoot==True:
                        if penguin.right_dir == True:
                            bullet=Bullet("right",penguin.rect.midright,"penguin")
                        elif penguin.right_dir == False:
                            bullet=Bullet("left",penguin.rect.midleft,"penguin")
                        penguin.reload_time=int(pygame.time.get_ticks()/1000)
                
                if event.key == ord("j"):
                    turtle.move(-steps,0)
                
                if event.key == ord("l"):
                    turtle.move(steps,0)
                if event.key == ord("i"):
                    turtle.jump()
                if event.key == ord("k"):
                    if turtle.shoot==True:
                        if turtle.right_dir == True:
                            bullet=Bullet("right",turtle.rect.midright,"turtle")
                        elif turtle.right_dir == False:
                            bullet=Bullet("left",turtle.rect.midleft,"turtle")
                        turtle.reload_time=int(pygame.time.get_ticks()/1000)

            if event.type == pygame.KEYUP:
                if event.key == ord("a"):
                    if penguin.restart:
                        penguin.restart=False
                    else:
                        penguin.move(steps,0)
                if event.key == ord("d"):
                    if penguin.restart:
                        penguin.restart=False
                    else:
                        penguin.move(-steps,0)
                        restart=False


                if event.key == ord("j"):
                    if turtle.restart:
                        turtle.restart=False
                    else:
                        turtle.move(steps,0)
                if event.key == ord("l"):
                    if turtle.restart:
                        turtle.restart=False
                    else:
                        turtle.move(-steps,0)
                        restart=False
    else:
        window.blit(ice_background,(0,0))
        for t in end_text_list:
            t.update()
        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == ord("q"):
                    pygame.quit()
                    game==False
                game==False