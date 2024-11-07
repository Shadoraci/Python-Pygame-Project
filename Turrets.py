import pygame as PG
import Constants
import math
from TurretData import TURRETDATA
class Turret(PG.sprite.Sprite):

    def __init__(self, SpriteSheets, TileX, TileY, ShotFX):
        PG.sprite.Sprite.__init__(self)
        self.UpgradeLevel = 1
        self.Range = TURRETDATA[self.UpgradeLevel - 1].get("Range")
        self.Cooldown = (TURRETDATA[self.UpgradeLevel - 1].get("Cooldown"))
        self.LastShotFired = PG.time.get_ticks()
        self.Selected = False
        self.Target = None

        #Positioning
        self.TileX = TileX
        self.TileY = TileY
        #Calculate Center Cords
        self.X = (self.TileX + 0.5) * Constants.TILESIZE
        self.Y = (self.TileY + 0.5) * Constants.TILESIZE
        #Sfx
        self.ShotFX = ShotFX
        #Animation
        self.SpriteSheets = SpriteSheets
        self.AnimationList = self.LoadImages(self.SpriteSheets[self.UpgradeLevel - 1])
        self.FrameIndex = 0
        self.UpdateTime = PG.time.get_ticks()
        #Update image
        self.Angle = 90
        self.OriginalImage = self.AnimationList[self.FrameIndex]
        self.Image = PG.transform.rotate(self.OriginalImage, self.Angle)
        self.Rect = self.Image.get_rect()
        self.Rect.center = (self.X, self.Y)

        #Create Ranged Circle
        self.RangeImage = PG.Surface((self.Range * 2, self.Range * 2))
        self.RangeImage.fill((0,0,0))
        self.RangeImage.set_colorkey((0,0,0))
        PG.draw.circle(self.RangeImage, "grey100", (self.Range, self.Range), self.Range)
        self.RangeImage.set_alpha(100)
        self.RangeRect = self.RangeImage.get_rect()
        self.RangeRect.center = self.Rect.center

    def update(self, EnemyGroup, World):
        #Search Target
        if self.Target:
            self.PlayAnimation()
        else:
            #Search for Target
            if PG.time.get_ticks() - self.LastShotFired > (self.Cooldown / World.GameSpeed):
                self.PickTarget(EnemyGroup)
    def PickTarget(self, EnemyGroup):
        #FindEnemy
        XDistance = 0
        YDistance = 0

        #Check Distance for Range
        for Enemy in EnemyGroup:
            if Enemy.Health > 0:
                XDistance = Enemy.Pos[0] - self.X
                YDistance = Enemy.Pos[1] - self.Y
                Distance = math.sqrt(XDistance ** 2 + YDistance ** 2)
                if Distance < self.Range:
                    self.Target = Enemy
                    self.Angle = math.degrees(math.atan2(-YDistance, XDistance))
                    print("Target Selected")
                    #Damage Enemy
                    self.Target.Health -= Constants.DAMAGE

                    self.ShotFX.play()
                    break
    def LoadImages(self, SpriteSheet):
        #Extract Frames from Spritemap
        Size = SpriteSheet.get_height()
        AnimationList = []
        for Steps in range(Constants.ANIMATIONSTEPS):
            TempImg = SpriteSheet.subsurface(Steps * Size, 0, Size, Size)
            AnimationList.append(TempImg)
        return AnimationList
    def PlayAnimation(self):
        self.OriginalImage = self.AnimationList[self.FrameIndex]
        #TimeCheck
        if PG.time.get_ticks() - self.UpdateTime > Constants.ANIMATIONDELAY:
            self.UpdateTime = PG.time.get_ticks()
            self.FrameIndex +=1
            if self.FrameIndex >= len(self.AnimationList):
                self.FrameIndex = 0
                self.LastShotFired = PG.time.get_ticks()
                self.Target = None
    def Upgrade(self):
        self.UpgradeLevel += 1
        self.Range = TURRETDATA[self.UpgradeLevel - 1].get("Range")
        self.Cooldown = TURRETDATA[self.UpgradeLevel - 1].get("Cooldown")
        #Upgrade Turret Image
        self.AnimationList = self.LoadImages(self.SpriteSheets[self.UpgradeLevel - 1])
        self.OriginalImage = self.AnimationList[self.FrameIndex]

        # Upgrade Ranged Circle
        self.RangeImage = PG.Surface((self.Range * 2, self.Range * 2))
        self.RangeImage.fill((0, 0, 0))
        self.RangeImage.set_colorkey((0, 0, 0))
        PG.draw.circle(self.RangeImage, "grey100", (self.Range, self.Range), self.Range)
        self.RangeImage.set_alpha(100)
        self.RangeRect = self.RangeImage.get_rect()
        self.RangeRect.center = self.Rect.center

    def Draw(self, surface):
        self.Image = PG.transform.rotate(self.OriginalImage, self.Angle - 90)
        self.Rect = self.Image.get_rect()
        self.Rect.center = (self.X, self.Y)
        surface.blit(self.Image, self.Rect)
        if self.Selected:
            surface.blit(self.RangeImage, self.RangeRect)
