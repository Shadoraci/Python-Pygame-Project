import Constants
import pygame as PG
import Constants as Con
from Buttons import Button
import Turrets
from EnemyMain import Enemy
from WorldMain import World
import json
#intiatlize pygame and 'start the game'
PG.init()

#frame rate limitation
Clock = PG.time.Clock()

#create the game winow
Screen = PG.display.set_mode((Con.SCREEN_WIDTH + Con.SIDE_PANEL,Con.SCREEN_HEIGHT))
#title of game window
PG.display.set_caption("Tristana's Journey Through Red Jungle")

#Game Variables
GameOver = False
#-1 is a loss & 1 is a win
GameResult = 0
LevelStarted = False
LastEnemySpawn = PG.time.get_ticks()
PlacingTurrets = False
SelectedTurret = None

#Load Sprites
TurretSpriteSheets = []
for SpriteNum in range(1,Constants.TURRETLEVELS + 1):
    TurretSheet = PG.image.load(f'Assets/Images/Turrets/turret_{SpriteNum}.png').convert_alpha()
    TurretSpriteSheets.append(TurretSheet)

MapImage = PG.image.load('Assets/Images/Map/level.png').convert_alpha()
CursorTurret = PG.image.load('Assets/Images/Turrets/Cursor_Turret.png').convert_alpha()
BuyTurretImage = PG.image.load('Assets/Images/Buttons/buy_turret.png').convert_alpha()
CancelImage = PG.image.load('Assets/Images/Buttons/cancel.png').convert_alpha()
UpgradeTurretImage = PG.image.load('Assets/Images/Buttons/upgrade_turret.png').convert_alpha()
BeginImage = PG.image.load('Assets/Images/Buttons/begin.png').convert_alpha()
RestartImage = PG.image.load('Assets/Images/Buttons/restart.png').convert_alpha()
FastImage = PG.image.load('Assets/Images/Buttons/fast_forward.png').convert_alpha()
HeartImage = PG.image.load('Assets/Images/GUI/heart.png').convert_alpha()
CoinImage = PG.image.load('Assets/Images/GUI/coin.png').convert_alpha()
ExitButton = PG.image.load('Assets/Images/GUI/png-exit-icon-crystal-7.png').convert_alpha()
ShotFX = PG.mixer.Sound('Assets/Sounds/shot.wav')
ShotFX.set_volume(0.8)
BGMusic = PG.mixer.Sound('Assets/Sounds/rainyday.mp3')
BGMusic.set_volume(0.3)
EnemyImages = {
    "Teemo": PG.image.load('Assets/Images/EnemySprites/Teemo.png').convert_alpha(),
    "Tristana": PG.image.load('Assets/Images/EnemySprites/Tristana.png').convert_alpha(),
    "Poppy": PG.image.load('Assets/Images/EnemySprites/Poppy.png').convert_alpha(),
    #I can add more enemies here
}
#File Loading for Level Data
with open('Assets/Images/Map/LevelData.tmj') as DataFile:
    WorldData = json.load(DataFile)

#Create World
InitialWorld = World(WorldData, MapImage)
InitialWorld .DataProcessing()
InitialWorld .ProcessEnemies()
BGMusic.play(loops=True)

#Fonts for Text
TextFont = PG.font.SysFont("Consolas", 24, bold = True)
LargeFont = PG.font.SysFont("Consolas", 36)

#Function for text output
def DrawText(Text, Font, TextColor, X, Y):
    Image = Font.render(Text, True, TextColor)
    Screen.blit(Image, (X, Y))

def DisplayData():
    PG.draw.rect(Screen, "maroon", (Con.SCREEN_WIDTH, 0, Con.SIDE_PANEL, Con.SCREEN_HEIGHT))
    PG.draw.rect(Screen, "grey0", (Con.SCREEN_WIDTH, 0, Con.SIDE_PANEL, 400), 2)
    #Display Data
    DrawText("LEVEL " + str(InitialWorld.WaveLevel), TextFont, "white", Con.SCREEN_WIDTH + 10, 10)
    Screen.blit(HeartImage, (Con.SCREEN_WIDTH + 10, 35))
    DrawText(str(InitialWorld.Health), TextFont, "red", Con.SCREEN_WIDTH + 50, 40)
    Screen.blit(CoinImage, (Con.SCREEN_WIDTH + 10, 65))
    DrawText(str(InitialWorld.Money), TextFont, "gold",Con.SCREEN_WIDTH + 50, 70)




#Create Turrets
def CreateTurret(MousePOS):
    MouseTileX = MousePOS[0] // Constants.TILESIZE
    MouseTileY = MousePOS[1] // Constants.TILESIZE
    #Calculate # of Tiles
    MouseTileNum = ((MouseTileY * Con.COLS) + MouseTileX)
    #Checking Placeable Tiles
    if InitialWorld .TileMap[MouseTileNum] == 7:
        #Is there a turret?
        FreeSpace = True
        for Turret in TurretGroup:
            if (MouseTileX, MouseTileY) == (Turret.TileX, Turret.TileY):
                FreeSpace = False
        if FreeSpace == True:
            SingleTurret = Turrets.Turret(TurretSpriteSheets, MouseTileX, MouseTileY, ShotFX)
            TurretGroup.add(SingleTurret)
            InitialWorld .Money -= Con.BUYCOST
            print(TurretGroup)
def SelectTurret(MousePOS):
    MouseTileX = MousePOS[0] // Constants.TILESIZE
    MouseTileY = MousePOS[1] // Constants.TILESIZE
    for Turret in TurretGroup:
        if (MouseTileX, MouseTileY) == (Turret.TileX, Turret.TileY):
            return Turret

def ClearSelection():
    for Turret in TurretGroup:
        Turret.Selected = False

#Turret Creation
TurretGroup = PG.sprite.Group()

#enemy creation
EnemyGroup = PG.sprite.Group()


#Create Buttons
TurretButton = Button(Con.SCREEN_WIDTH + 30, 120, BuyTurretImage, True)
CancelButton = Button(Con.SCREEN_WIDTH + 50, 180, CancelImage, True)
UpgradeButton = Button(Con.SCREEN_WIDTH + 5, 180, UpgradeTurretImage, True)
BeginButton = Button(Con.SCREEN_WIDTH + 60, 300, BeginImage, True)
RestartButton = Button(310, 300, RestartImage, True)
FastForward = Button(Con.SCREEN_WIDTH + 50, 300, FastImage, False)
ExitButton = Button(Con.SCREEN_WIDTH + 90, 400, ExitButton, True)
#Game Runtime --------------------------------------------------------------------------------------
Run = True
while Run:

    Clock.tick(Con.FPS)
    # Updating Section
    # ----------------
    if GameOver == False:
        if InitialWorld .Health <= 0:
            GameOver = True
            GameResult = -1
        #Check if player has won
        if InitialWorld.WaveLevel > Con.TOTALLEVELS:
            GameResult = 1
            GameOver = True
        #PG.draw.lines(Screen, "grey0", False, World.Waypoints)
        EnemyGroup.update(InitialWorld)
        TurretGroup.update(EnemyGroup, InitialWorld)

        #Highlight Selected Turret
        if SelectedTurret:
            SelectedTurret.Selected = True
    #-----------------
    # Drawing Section
    # ----------------

    #Draw Level
    InitialWorld.draw(Screen)

    DisplayData()

    #Drawing Groups
    EnemyGroup.draw(Screen)
    for Turret in TurretGroup:
        Turret.Draw(Screen)

    if GameOver == False:

        #Spawn Enemies on level start
        if LevelStarted == False:
            if BeginButton.draw(Screen):
                LevelStarted = True
        else:
            #Fast Forward Game
            InitialWorld.GameSpeed = 1
            if FastForward.draw(Screen):
                InitialWorld.GameSpeed = 2
            if PG.time.get_ticks() - LastEnemySpawn > (Con.SPAWNCOOLDOWN / InitialWorld.GameSpeed):
                if(InitialWorld .SpawnedEnemies < len(InitialWorld .EnemyList)):
                    EnemyType = InitialWorld .EnemyList[InitialWorld .SpawnedEnemies]
                    SingleEnemy = Enemy(EnemyType, InitialWorld .Waypoints, EnemyImages)
                    EnemyGroup.add(SingleEnemy)
                    print(Enemy)
                    InitialWorld .SpawnedEnemies += 1
                    LastEnemySpawn = PG.time.get_ticks()

        #Checking if Wave is finished and starts a new one
        if InitialWorld .CheckLevelCompletion() == True:
            InitialWorld .Money += Con.WAVEREAWRD
            InitialWorld .WaveLevel += 1
            LevelStarted = False
            LastEnemySpawn = PG.time.get_ticks()
            InitialWorld .ResetLevel()
            InitialWorld .ProcessEnemies()

        DrawText(str(Con.BUYCOST), TextFont, "grey100", Con.SCREEN_WIDTH + 215, 135)
        Screen.blit(CoinImage, (Con.SCREEN_WIDTH + 260, 130))

        #Drawing Buttons
        if TurretButton.draw(Screen):
            PlacingTurrets = True
            #Cancel Button Shown when Placing
        if PlacingTurrets == True:
            #Show Cursor Turret Onscreen
            CursorRect = CursorTurret.get_rect()
            CursorPOS = PG.mouse.get_pos()
            CursorRect.center = CursorPOS
            if CursorPOS[0] <= Con.SCREEN_WIDTH:
                Screen.blit(CursorTurret, CursorRect)
            if CancelButton.draw(Screen):
                PlacingTurrets = False
        if SelectedTurret:
            if SelectedTurret.UpgradeLevel < Con.TURRETLEVELS:
                DrawText(str(Con.UPGRADECOST), TextFont, "grey100", Con.SCREEN_WIDTH + 215, 195)
                Screen.blit(CoinImage, (Con.SCREEN_WIDTH + 260, 190))
                if UpgradeButton.draw(Screen):
                    if InitialWorld .Money >= Con.UPGRADECOST:
                        SelectedTurret.Upgrade()
                        InitialWorld .Money -= Con.UPGRADECOST
    else:
        PG.draw.rect(Screen, "dodgerblue", (200,200,400,200), border_radius = 30)
        if GameResult == -1:
            DrawText("GAME OVER", LargeFont, "grey0", 310, 230)
        elif GameResult == 1:
            DrawText("YOU WIN!!!", LargeFont, "grey0", 315, 230)
        #Restart Level
        if RestartButton.draw(Screen):
            GameOver = False
            LevelStarted = False
            PlacingTurrets = False
            SelectedTurret = None
            LastEnemySpawn = PG.time.get_ticks()
            InitialWorld = World(WorldData, MapImage)
            InitialWorld.DataProcessing()
            InitialWorld.ProcessEnemies()

            #Empty Groups
            EnemyGroup.empty()
            TurretGroup.empty()

    #-----------------

    #event handler
    for event in PG.event.get():
        #quit program
        if event.type == PG.QUIT:
            Run = False
        #OnMouseClick
        if event.type == PG.MOUSEBUTTONDOWN and event.button == 1:
            #GrabbingMouseCords
            MousePOS = PG.mouse.get_pos()
            #Checking Game Area
            if MousePOS[0] < Constants.SCREEN_WIDTH and MousePOS[1] < Constants.SCREEN_HEIGHT:
               SelectedTurret = None
               ClearSelection()
               if(PlacingTurrets == True):
                   #Enough Money?
                   if InitialWorld .Money >= Con.BUYCOST:
                        CreateTurret(MousePOS)
               else:
                   SelectedTurret = SelectTurret(MousePOS)
    #Updating Display
    PG.display.flip()
PG.quit()