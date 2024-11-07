import pygame as PG
from pygame.math import Vector2
import math
from EnemyData import ENEMYDATA
import Constants as Con
class Enemy(PG.sprite.Sprite):

    def __init__(self, EnemyType, Waypoints, Images):
        PG.sprite.Sprite.__init__(self)
        self.Waypoints = Waypoints
        self.Pos = Vector2(self.Waypoints[0])
        self.TargetWaypoint = 1
        self.Health = ENEMYDATA.get(EnemyType)["Health"]
        self.Speed = ENEMYDATA.get(EnemyType)["Speed"]
        self.Angle = 0
        self.OriginalImage = Images.get(EnemyType)
        self.image = PG.transform.rotate(self.OriginalImage, self.Angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.Pos

    def update(self, World):
        self.Move(World)
        self.Rotate()
        self.CheckLife(World)

    def Move(self, World):
        #Define Waypoints
        #Target becomes next waypoint
        if self.TargetWaypoint < len(self.Waypoints):
            self.Target = Vector2(self.Waypoints[self.TargetWaypoint])
            self.Movement = self.Target - self.Pos
        else:
            #If they reach the end, they go kaboom
            self.kill()
            World.Health -=1
            World.MissedEnemies += 1
        #calculating distance
        Distance = self.Movement.length()
        if(Distance >= (self.Speed * World.GameSpeed)):
            self.Pos += self.Movement.normalize() * (self.Speed * World.GameSpeed)
        else:
            if Distance != 0:
                self.Pos += self.Movement.normalize() * Distance
            self.TargetWaypoint +=1
        self.rect.center = self.Pos

    def Rotate(self):
        #Calculate Distance
        Distance = self.Target - self.Pos
        self.Angle = math.degrees(math.atan2(-Distance[1], Distance[0]))
        #Rotation
        self.image = PG.transform.rotate(self.OriginalImage, self.Angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.Pos
    def CheckLife(self, World):
        if self.Health <= 0:
            World.KilledEnemies += 1
            World.Money += Con.KILLREWARD
            self.kill()