import pygame as PG
from EnemyData import ENEMYSPAWNDATA
import random
import Constants as Con
class World():
    def __init__(self, Data, MapImage):
        self.WaveLevel = 1
        self.GameSpeed = 1
        self.Health = Con.HEALTH
        self.Money = Con.MONEY
        self.LevelData = Data
        self.Image = MapImage
        self.Waypoints = []
        self.TileMap = []
        self.EnemyList = []
        self.SpawnedEnemies = 0
        self.KilledEnemies = 0
        self.MissedEnemies = 0
    def DataProcessing(self):
        #Cycling Through Data
        for Layer in self.LevelData["layers"]:
            if Layer["name"] == "tilemap":
                self.TileMap = Layer["data"]
                print(self.TileMap)
            elif Layer["name"] == "waypoints":
                for Object in Layer["objects"]:
                    WaypointData = Object["polyline"]
                    self.WaypointProcessing(WaypointData)

    def WaypointProcessing(self, Data):
        #Iteration of Waypoints
        for Point in Data:
            TempX = Point.get("x")
            TempY = Point.get("y")
            self.Waypoints.append((TempX, TempY))
    def ProcessEnemies(self):
        Enemies = ENEMYSPAWNDATA[self.WaveLevel - 1]
        for EnemyType in Enemies:
            EnemiesToSpawn = Enemies[EnemyType]
            print(EnemiesToSpawn)
            for Enemy in range(EnemiesToSpawn):
                print(EnemyType)
                self.EnemyList.append(EnemyType)
        #Randomize Enemy Spawning
        random.shuffle(self.EnemyList)
    def CheckLevelCompletion(self):
        if (self.KilledEnemies + self.MissedEnemies) == len(self.EnemyList):
            return True
    def ResetLevel(self):
        #Reset enemy variables
        self.EnemyList = []
        self.SpawnedEnemies = 0
        self.KilledEnemies = 0
        self.MissedEnemies = 0
    def draw(self, surface):
        surface.blit(self.Image, (0,0))