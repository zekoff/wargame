'''
Created on Feb 24, 2012

@author: Zekoff
'''
import sys
import time
import random

class Wargame():
    def __init__(self):
        self.rand = random.Random()
        self.yesResponses = ['oui', 'sure', 'absolutely', 'definitely', 'affirmative', 'ok']
        self.enemies = ['Germans', 'Russians', 'Chinese', 'Italians', 'Canadians', 'Japanese', 'Indians', 'British', 'French']
    def start(self):
        self.write("Would you like to play a game?")
        if not self.getBooleanInput():
            exit()
        self.shortSleep()
        print ""
        self.field = PlayingField()
        self.player = Faction()
        self.player.setupHistory()
        self.player.setupStanceList()
        self.enemy = Faction()
        self.enemy.setupHistory()
        self.enemy.setupStanceList()
        # TODO: self.enemyAI = EnemyAI()
        self.year = random.choice(range(1910, 2150))
        self.month = random.choice(range(1, 12))
        self.write("The year is " + str(self.year) + ".")
        self.enemyName = random.choice(self.enemies)
        self.write("You are at war with the " + self.enemyName + ".")
        rand = random.Random()
        self.player.resources = rand.randint(850, 1150)
        self.enemy.resources = rand.randint(850, 1150)
        self.write("You have at your disposal " + str(self.player.resources) + " resources.")
        self.write("You will allocate these by percentage each month between offense,")
        self.write("defense, and espionage.")
        self.write("The location of your forces will be represented by an 'O' symbol on the map.")
        self.shortSleep()
        
        while not self.player.defeated and not self.enemy.defeated:
            self.nextTurn()
            if self.field.getNumberControlledTerritories("O") == 0:
                self.player.defeated = True
                self.write("Your forces have been annihilated.")
            if self.field.getNumberControlledTerritories("X") == 0:
                self.enemy.defeated = True
                self.write("You have conquered all territories.")
        
    def nextTurn(self):
        rand = random.Random()
        # Do turn-reset kind of stuff
        self.player.recordCurrentAllocationToHistory()
        self.enemy.recordCurrentAllocationToHistory()
        # Player resource increase
        playerResourcesFromTerritory = self.field.getNumberControlledTerritories("O") * 50
        playerResourcesFromTerritory *= (1 + (rand.random() / 2 - .25))
        playerAdditionalResources = 0
        if self.player.getCurrentStanceName() in ['balanced', 'conservative', 'peaceful']:
            playerAdditionalResources += .05
        if self.player.getCurrentStanceName() in ['conservative', 'peaceful']:
            playerAdditionalResources += .15
        if self.player.getCurrentStanceName() == 'peaceful':
            playerAdditionalResources += .3 
        playerResourcesFromTerritory *= 1 + playerAdditionalResources
        playerResourcesFromTerritory = int(playerResourcesFromTerritory)
        self.player.resources += playerResourcesFromTerritory
        # Enemy resource increase
        enemyResourcesFromTerritory = self.field.getNumberControlledTerritories("X") * 50
        enemyResourcesFromTerritory *= (1 + (rand.random() / 2 - .25))
        enemyAdditionalResources = 0
        if self.enemy.getCurrentStanceName() in ['balanced', 'conservative', 'peaceful']:
            enemyAdditionalResources += .05
        if self.enemy.getCurrentStanceName() in ['conservative', 'peaceful']:
            enemyAdditionalResources += .15
        if self.enemy.getCurrentStanceName() == 'peaceful':
            enemyAdditionalResources += .3 
        enemyResourcesFromTerritory *= 1 + enemyAdditionalResources
        enemyResourcesFromTerritory = int(enemyResourcesFromTerritory)
        self.enemy.resources += enemyResourcesFromTerritory
        # Increment date
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        # Set season
        if self.month in [12, 1, 2]:
            self.season = 'winter' # bonus to DEF
        elif self.month in [3, 4, 5]:
            self.season = 'spring' # bonus to resource gen
        elif self.month in [6, 7, 8]:
            self.season = 'summer' # bonus to attack chance
        elif self.month in [9, 10, 11]:
            self.season = 'fall' # bonus to ESP
        # go ahead and set enemy allocation for the turn
        # enemy AI
        # Display header
        print ""
        print ""
        print "+---------------------+"
        sys.stdout.write("| Year " + str(self.year) + ", Month ")
        if self.month > 9:
            sys.stdout.write(str(self.month) + " |\n")
        else:
            sys.stdout.write(str(self.month) + "  |\n")
        print "+---------------------+"
        # you control X provinces, providing you with X additional resources
        self.write("You control " + str(self.field.getNumberControlledTerritories("O")) + " territories,")
        self.write("providing you with " + str(playerResourcesFromTerritory) + " additional resources.")
        self.write("This gives you a total of " + str(self.player.resources) + " resources to deploy.")
        # the enemy controls X provinces, providing them...
        print ""
        self.write("You are taking a " + self.player.getCurrentStanceName() + " stance toward the " + self.enemyName + ".")
        # display bonuses from stance this turn
        if playerAdditionalResources > 0:
            self.write("You gain an additional " + str(int(playerAdditionalResources * 100)) + "% resources from territory")
            self.write("this month because of your stance.")
        # Any ESP perks that triggered this month
        
        print""
        # the enemy's stance toward you is...
        self.write("The enemy's stance toward you has been " + str(self.enemy.getCurrentStanceName()) + ".")
        # if stance is sneaky, show enemy resource amounts
        if self.player.getCurrentStanceName() in ['sneaky', 'devious']:
            self.write("Our spies report that the enemy has " + str(self.enemy.resources) + " resources to spend.")
        # if stance is devious, show exact allocation of enemy forces this round
        if self.player.getCurrentStanceName() == "devious":
            self.write("Our spies report that the enemy are allocating their resources")
            self.write("this month as follows:")
            self.write(str(self.enemy.OFF) + " offense, " + str(self.enemy.DEF) + " defense, " + str(self.enemy.ESP) + " espionage")
        print ""
        self.write("Battlefield control is as follows:")
        print ""
        self.field.printField()
        print ""
        self.shortSleep()
        done = False
        allocationSum = 0
        while not done:
            resourcesSet = False
            while not resourcesSet:
                self.write("Resource allocation:")
                self.write("Offense (%):")
                self.player.OFF = self.getPercentageInput()
                self.write("Defense (%):")
                self.player.DEF = self.getPercentageInput()
                self.write("Espionage (%):")
                self.player.ESP = self.getPercentageInput()
                allocationSum = self.player.OFF + self.player.DEF + self.player.ESP
                if allocationSum <= 100:
                    resourcesSet = True
                else:
                    self.write("You cannot allocate more than 100%.")
                    self.shortSleep()
        # you hold X resources in reserve.
            if allocationSum < 100:
                self.write("You will hold " + str(100 - allocationSum) + "% of your resources in reserve this month.")
            # OK?
            self.write("OK?")
            if self.getBooleanInput():
                done = True
        print ""
        # combat phase
        self.combatPhase()
        
    def combatPhase(self):
        playerAttackChance = .15
        if self.player.getCurrentStanceName() in ['balanced', 'offensive', 'bloodthirsty']:
            playerAttackChance += .1
        if self.player.getCurrentStanceName() in ['offensive', 'bloodthirsty']:
            playerAttackChance += .1
        if self.player.getCurrentStanceName() == 'bloodthirsty':
            playerAttackChance += .1
        potentialAttackVectors = self.field.getBorderTerritoriesList("O")
        attackLaunchedFrom = []
        for territory in potentialAttackVectors:
            if self.rand.random() < playerAttackChance:
                attackLaunchedFrom.append(territory)
        destinationTerritories = []
        if len(attackLaunchedFrom) > 0:
            for attackLocation in attackLaunchedFrom:
                dest = self.field.getTerritoryToAttack("O", attackLocation[0], attackLocation[1])
                destinationTerritories.append(dest)
            self.write("Your forces are attacking the following territories:")
            for i in range(len(attackLaunchedFrom)):
                self.write(str(attackLaunchedFrom[i]) + " -> " + str(destinationTerritories[i]))
        else:
            self.write("Your forces are not marching on any new territories this month.")
        print ""
        # at this point, player attack vectors are in attackLaunchedFrom[] and destinationTerritories[]
        
        enemyAttackChance = .15
        if self.enemy.getCurrentStanceName() in ['balanced', 'offensive', 'bloodthirsty']:
            enemyAttackChance += .1
        if self.enemy.getCurrentStanceName() in ['offensive', 'bloodthirsty']:
            enemyAttackChance += .1
        if self.enemy.getCurrentStanceName() == 'bloodthirsty':
            enemyAttackChance += .1
        potentialEnemyAttackVectors = self.field.getBorderTerritoriesList("X")
        enemyAttackLaunchedFrom = []
        for territory in potentialEnemyAttackVectors:
            if self.rand.random() < enemyAttackChance:
                enemyAttackLaunchedFrom.append(territory)
        enemyDestinationTerritories = []
        if len(enemyAttackLaunchedFrom) > 0:
            for attackLocation in enemyAttackLaunchedFrom:
                dest = self.field.getTerritoryToAttack("X", attackLocation[0], attackLocation[1])
                enemyDestinationTerritories.append(dest)
            self.write("Enemy forces are attacking the following territories:")
            for i in range(len(enemyAttackLaunchedFrom)):
                self.write(str(enemyAttackLaunchedFrom[i]) + " -> " + str(enemyDestinationTerritories[i]))
        else:
            self.write("Enemy forces are not marching on any new territories this month.")
        print ""
        # at this point, enemy attack vectors are in enemyAttackLaunchedFrom[] and enemyDestinationTerritories[]
        
        self.shortSleep()
        # determine how many player troops will attack each territory
        playerDeployment = dict()
        for location in destinationTerritories:
            if location not in playerDeployment:
                playerDeployment[location] = self.player.resources / len(attackLaunchedFrom) * self.player.OFF / 100
            else:
                playerDeployment[location] += self.player.resources / len(attackLaunchedFrom) * self.player.OFF / 100
        # determine enemy troops attacking each territory
        enemyDeployment = dict()
        for location in enemyDestinationTerritories:
            if location not in enemyDeployment:
                enemyDeployment[location] = self.enemy.resources / len(enemyAttackLaunchedFrom) * self.enemy.OFF / 100
            else:
                enemyDeployment[location] += self.enemy.resources / len(enemyAttackLaunchedFrom) * self.enemy.OFF / 100
        
        # determine which territories factions will defend
        enemyDefenseLocations = self.field.getBorderTerritoriesList("X")
        playerDefenseLocations = self.field.getBorderTerritoriesList("O")
        
        playerDefenseNumber = self.player.resources / len(playerDefenseLocations) * self.player.DEF / 100
        enemyDefenseNumber = self.enemy.resources / len(enemyDefenseLocations) * self.enemy.DEF / 100

        # player attacks
        for location, troopCount in playerDeployment.iteritems():
            self.write("** Attack on " + str(location) + " **")
            self.write(str(troopCount) + " resources were devoted to attacking location " + str(location) + ".")
            if location in enemyDefenseLocations:
                # enemy defending, do combat
                self.write("The enemy devoted " + str(enemyDefenseNumber) + " resources to defending this location.")
                # modify atk/def as necessary
                self.player.resources -= troopCount
                playerAdditionalAttack = 0
                if self.player.getCurrentStanceName() in ['offensive', 'bloodthirsty']:
                    playerAdditionalAttack += .1
                if self.player.getCurrentStanceName() == 'bloodthirsty':
                    playerAdditionalAttack += .15
                if playerAdditionalAttack > 0:
                    self.write("Your " + self.player.getCurrentStanceName() + " stance results in a " + str(int(playerAdditionalAttack * 100)) + "% bonus")
                    self.write("to your attack effectiveness.")
                troopCount *= 1 + playerAdditionalAttack
                enemyAdditionalDefense = 0
                if self.enemy.getCurrentStanceName() in ['balanced', 'defensive', 'entrenched']:
                    enemyAdditionalDefense += .1
                if self.enemy.getCurrentStanceName() in ['defensive', 'entrenched']:
                    enemyAdditionalDefense += .2
                if self.enemy.getCurrentStanceName() == 'entrenched':
                    enemyAdditionalDefense += .4
                if enemyAdditionalDefense > 0:
                    self.write("The enemy's " + self.enemy.getCurrentStanceName() + " stance results in a " + str(int(enemyAdditionalDefense * 100)) + "% bonus")
                    self.write("to their defense effectiveness.")
                enemyTempDefense = enemyDefenseNumber
                enemyTempDefense *= 1 + enemyAdditionalDefense
                if troopCount > enemyTempDefense:
                    # we won
                    self.write("Our forces emerged victorious! We now control " + str(location) + ".")
                    self.enemy.resources -= enemyDefenseNumber
                    self.field.locations[location[0]][location[1]] = "O"
                else:
                    # we lost
                    self.write("Our forces were outmatched. The enemy retains control over this location.")
            else:
                self.write("Combat was uncontested, and our forces now claim " + str(location) + ".") 
                self.field.locations[location[0]][location[1]] = "O"
            print ""
        
        # player defends
        for location, troopCount in enemyDeployment.iteritems():
            self.write("-- Defense at " + str(location) + " --")
            self.write("The enemy attacked " + str(location) + " with " + str(troopCount) + " resources.")
            if location in playerDefenseLocations:
                # enemy defending, do combat
                self.write("We defended this location with " + str(playerDefenseNumber) + " resources.")
                # modify atk/def as necessary
                self.enemy.resources -= troopCount
                enemyAdditionalAttack = 0
                if self.enemy.getCurrentStanceName() in ['offensive', 'bloodthirsty']:
                    enemyAdditionalAttack += .1
                if self.enemy.getCurrentStanceName() == 'bloodthirsty':
                    enemyAdditionalAttack += .15
                if enemyAdditionalAttack > 0:
                    self.write("The enemy's " + self.enemy.getCurrentStanceName() + " stance results in a " + str(int(enemyAdditionalAttack * 100)) + "% bonus")
                    self.write("to their attack effectiveness.")
                troopCount *= 1 + enemyAdditionalAttack
                playerAdditionalDefense = 0
                if self.player.getCurrentStanceName() in ['balanced', 'defensive', 'entrenched']:
                    playerAdditionalDefense += .1
                if self.player.getCurrentStanceName() in ['defensive', 'entrenched']:
                    playerAdditionalDefense += .2
                if self.player.getCurrentStanceName() == 'entrenched':
                    playerAdditionalDefense += .4
                if playerAdditionalDefense > 0:
                    self.write("Your " + self.player.getCurrentStanceName() + " stance results in a " + str(int(playerAdditionalDefense * 100)) + "% bonus")
                    self.write("to your defense effectiveness.")
                playerTempDefense = playerDefenseNumber
                playerTempDefense *= 1 + playerAdditionalDefense
                if troopCount > playerTempDefense:
                    # we lost
                    self.write("Enemy forces emerged victorious, and they now control " + str(location) + ".")
                    self.player.resources -= playerDefenseNumber
                    self.field.locations[location[0]][location[1]] = "X"
                else:
                    # we won
                    self.write("The enemy was outmatched! We retain control over this location.")
            else:
                self.write("Combat was uncontested, and enemy forces now claim " + str(location) + ".") 
                self.field.locations[location[0]][location[1]] = "X"
            print ""
                
    # TODO: How to handle the case where both factions attack an uncontested territory in the same turn?
    # Current enemy just overrides the territory b/c it goes 2nd and you weren't defending
    # Conservative/peaceful stance grants increase to resources per territory
    # Balanced stance gives small bonus to everything
    # Offensive stances: higher chance to launch attack
    # Defensive stances: increased ability to defend
    # Espionage stances: faster increase toward ESP perks
        
    def write(self, content):
        for l in content:
            sys.stdout.write(l)
            time.sleep(.012)
        sys.stdout.write("\n")
    def getBooleanInput(self):
        sys.stdout.write("> ")
        response = raw_input()
        response = response.lower()
        if response == "" or response[0] == "y" or response in self.yesResponses:
            return True
        else:
            return False
    def shortSleep(self):
        time.sleep(1.3)
    def getPercentageInput(self):
        done = False
        response = ""
        while not done:
            sys.stdout.write("> ")
            response = raw_input()
            if response == "":
                response = 0
                done = True
            else:
                try:
                    response = int(response)
                    if response > 100 or response < 0:
                        raise ValueError
                    done = True
                except ValueError:
                    print ""
                    self.write("Enter an integer between 0 and 100 indicating the percentage to allocate.")
        return response
        
class Faction:
    def __init__(self):
        self.historicalDataWindowSize = 5
        self.OFF = 33
        self.DEF = 33
        self.ESP = 33
        self.stance = 'neutral'
        self.resources = 1000
        self.stanceList = []
        self.allocationHistory = []
        self.defeated = False
    def getStance(self, OFF, DEF, ESP):
        bestStanceFitness = 2000 # lower is better
        bestFitnessIndex = 0
        counter = -1
        for stance in self.stanceList:
            counter += 1
            tempFitness = 0
            tempFitness += abs(stance.targetOFF - OFF)
            tempFitness += abs(stance.targetDEF - DEF)
            tempFitness += abs(stance.targetESP - ESP)
            if tempFitness < bestStanceFitness:
                bestStanceFitness = tempFitness
                bestFitnessIndex = counter
        return self.stanceList[bestFitnessIndex]
    def setupStanceList(self):
        self.stanceList.append(Stance('peaceful', 0, 0, 0))
        self.stanceList.append(Stance('conservative', 20, 20, 20))
        self.stanceList.append(Stance('balanced', 33, 33, 33))
        self.stanceList.append(Stance('offensive', 60, 20, 20))
        self.stanceList.append(Stance('defensive', 20, 60, 20))
        self.stanceList.append(Stance('sneaky', 20, 20, 60))
        self.stanceList.append(Stance('bloodthirsty', 80, 10, 10))
        self.stanceList.append(Stance('entrenched', 10, 80, 10))
        self.stanceList.append(Stance('devious', 10, 10, 80))
    def setupHistory(self):
        for i in range(self.historicalDataWindowSize):
            self.allocationHistory.append((0, 0, 0))
    def getHistoricalAllocation(self):
        totalOFF = 0
        totalDEF = 0
        totalESP = 0
        for i in range(len(self.allocationHistory)):
            tempOFF, tempDEF, tempESP = self.allocationHistory[i]
            totalOFF += tempOFF
            totalDEF += tempDEF
            totalESP += tempESP
        totalOFF /= len(self.allocationHistory)
        totalDEF /= len(self.allocationHistory)
        totalESP /= len(self.allocationHistory)
        return totalOFF, totalDEF, totalESP
    def recordCurrentAllocationToHistory(self):
        currentAllocation = (self.OFF, self.DEF, self.ESP)
        self.allocationHistory.append(currentAllocation)
        del(self.allocationHistory[0])
    def getCurrentStanceName(self):
        # Convenience method
        h = self.getHistoricalAllocation()
        stance = self.getStance(h[0], h[1], h[2])
        return stance.name
    
class Stance:
    def __init__(self, name, OFF, DEF, ESP):
        self.targetOFF = OFF
        self.targetDEF = DEF
        self.targetESP = ESP
        self.name = name
        
class PlayingField:
    def __init__(self, width=7, height=7):
        self.width = width
        self.height = height
        if self.width < 3:
            self.width = 3
        if self.height < 3:
            self.height = 3
        self.locations = []
        for i in range(self.width):
            self.locations.append([])
            for j in range(self.height):
                self.locations[i].append([])
                self.locations[i][j] = "-"
        self.setupBases()
    def setupBases(self):
        self.locations[self.width / 2][0] = "X"
        self.locations[self.width / 2 - 1][0] = "X"
        self.locations[self.width / 2 + 1][0] = "X"
        self.locations[self.width / 2][1] = "X"
        self.locations[self.width / 2][self.height - 1] = "O"
        self.locations[self.width / 2 - 1][self.height - 1] = "O"
        self.locations[self.width / 2 + 1][self.height - 1] = "O"
        self.locations[self.width / 2][self.height - 2] = "O"
    def printField(self):
        for row in range(self.height):
            sys.stdout.write(str(row) + "   ")
            for column in range(self.width):
                sys.stdout.write(self.locations[column][row])
                sys.stdout.write(" ")
            sys.stdout.write("\n")
        sys.stdout.write("\n    ")
        for column in range(self.width):
            sys.stdout.write(str(column) + " ")
        sys.stdout.write("\n")
    def getBorderTerritoriesList(self, owner='O'):
        territoryList = []
        for i in range(self.width):
            for j in range(self.height):
                north = True
                east = True
                south = True
                west = True
                if self.locations[i][j] == owner:
                    # Check if it borders non-friendly
                    east = self.territoryIsFriendly(owner, i + 1, j)
                    west = self.territoryIsFriendly(owner, i - 1, j)
                    north = self.territoryIsFriendly(owner, i, j - 1)
                    south = self.territoryIsFriendly(owner, i, j + 1)
                if not north or not east or not south or not west:
                    territoryList.append((i, j))
        return territoryList
    def territoryIsFriendly(self, owner, i, j):
        if i < 0 or j < 0:
            return True
        try:
            if owner == self.locations[i][j]:
                return True
            return False
        except IndexError:
            return True
    def getTerritoryToAttack(self, owner, i, j):
        if self.locations[i][j] != owner:
            raise RuntimeError
        potentialAttackAreas = []
        # east
        if not self.territoryIsFriendly(owner, i + 1, j):
            potentialAttackAreas.append((i + 1, j))
        # west
        if not self.territoryIsFriendly(owner, i - 1, j):
            potentialAttackAreas.append((i - 1, j))
        # north
        if not self.territoryIsFriendly(owner, i, j - 1):
            potentialAttackAreas.append((i, j - 1))
        #south
        if not self.territoryIsFriendly(owner, i, j + 1):
            potentialAttackAreas.append((i, j + 1))
        target = random.choice(potentialAttackAreas)
        if len(target) < 1:
            raise RuntimeError('No valid targets')
        return target
    def getNumberControlledTerritories(self, owner):
        count = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.locations[i][j] == owner:
                    count += 1
        return count

if __name__ == '__main__':
    game = Wargame()
    game.start()
