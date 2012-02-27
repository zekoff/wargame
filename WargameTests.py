'''
Created on Feb 25, 2012

@author: Zekoff
'''
import unittest
from Wargame import Faction, PlayingField


class Test(unittest.TestCase):

    def testFactionExists(self):
        faction = Faction()
        self.assertIsInstance(faction, Faction)
        
    def testFactionStanceList(self):
        faction = Faction()
        self.assertTrue(isinstance(faction.stanceList, list))

    def testFactionHasStanceList(self):
        faction = Faction()
        self.assertEqual(len(faction.stanceList), 0)
        
    def testFactionSetupStanceListPutsSomeElementsInList(self):
        faction = Faction()
        faction.setupStanceList()
        self.assertTrue(len(faction.stanceList) > 0)
        
    def testFactionStanceListContainsBalanced(self):
        faction = Faction()
        faction.setupStanceList()
        hasBalanced = False
        for stance in faction.stanceList:
            if stance.name == 'balanced':
                hasBalanced = True
        self.assertTrue(hasBalanced)
        
    def testGetsCorrectStance(self):
        faction = Faction()
        faction.setupStanceList()
        currentStance = faction.getStance(33, 33, 33)
        self.assertEqual(currentStance.name, 'balanced')
        
    def testGetsCorrectStance2(self):
        faction = Faction()
        faction.setupStanceList()
        currentStance = faction.getStance(20, 20, 20)
        self.assertEqual(currentStance.name, 'conservative')
        
    def testGetsCorrectStance3(self):
        faction = Faction()
        faction.setupStanceList()
        currentStance = faction.getStance(71, 15, 15)
        self.assertEqual(currentStance.name, 'bloodthirsty')
        
    def testPlayingFieldExists(self):
        field = PlayingField()
        self.assertIsInstance(field, PlayingField)
        
    def testPlayingFieldInitializesCorrectly(self):
        field = PlayingField()
        self.assertEqual(field.locations[3][0], 'X')
        
    def testPlayingFieldInitializesCorrectly2(self):
        field = PlayingField()
        self.assertEqual(field.locations[1][6], '-')
        
#    def testPrintField(self):
#        field = PlayingField()
#        field.printField()
#        
#    def testPrintNonDefaultField(self):
#        field = PlayingField(10, 8)
#        field.printField()
    
    def testHistoryInitsFive(self):
        faction = Faction()
        faction.setupHistory()
        self.assertEqual(len(faction.allocationHistory), 5)
        
    def testHistorialAllocation(self):
        faction = Faction()
        for i in range(4):
            faction.allocationHistory.append((0, 0, 0))
        faction.allocationHistory.append((100, 100, 100))
        history = faction.getHistoricalAllocation()
        self.assertEqual(history[0], 20)
        
    def testHistoricalAllocationAndStance(self):
        faction = Faction()
        faction.setupStanceList()
        for i in range(4):
            faction.allocationHistory.append((0, 0, 0))
        faction.allocationHistory.append((100, 100, 100))
        history = faction.getHistoricalAllocation()
        stance = faction.getStance(history[0], history[1], history[2])
        self.assertEqual(stance.name, 'conservative')
        
    def testBorderDetect(self):
        field = PlayingField()
        tlist = field.getBorderTerritoriesList('O')
        self.assertEqual(len(tlist), 3)
        
    def testBorderDetect2(self):
        field = PlayingField()
        field.locations[3][3] = 'X'
        tlist = field.getBorderTerritoriesList('X')
        self.assertEqual(len(tlist), 4)
        
    def testRecordCurrentAllocationMethodExists(self):
        faction = Faction()
        faction.setupHistory()
        faction.OFF = 30
        faction.DEF = 40
        faction.ESP = 30
        faction.recordCurrentAllocationToHistory()
        self.assertEqual(faction.allocationHistory[len(faction.allocationHistory) - 1], (30, 40, 30))
        
    def testPushingAllocationRemovesOldest(self):
        faction = Faction()
        faction.setupHistory()
        faction.OFF = 30
        faction.DEF = 40
        faction.ESP = 30
        faction.recordCurrentAllocationToHistory()
        self.assertEqual(len(faction.allocationHistory), faction.historicalDataWindowSize)
        
    def testGetTerritoryToAttack(self):
        field = PlayingField()
        target = field.getTerritoryToAttack('X', 3, 1)
        self.assertTrue(target in [(3, 2), (2, 1), (4, 1)])
        
    def testGetTerritoryToAttack2(self):
        field = PlayingField()
        target = field.getTerritoryToAttack('X', 3, 1)
        self.assertTrue(target not in [(4, 3)])
        
    def testGetNumberControlledTerritories(self):
        field = PlayingField()
        number = field.getNumberControlledTerritories('O')
        self.assertEqual(number, 4)
        
    def testBorderTerritories(self):
        field = PlayingField()
        field.locations[2][3] = "O"
        field.locations[2][2] = "O"
        field.locations[3][2] = "O"
        field.locations[4][2] = "O"
        field.locations[3][3] = "O"
        number = len(field.getBorderTerritoriesList("O"))
        self.assertEqual(number, 8)
        
    def testEspionageDictExists(self):
        faction = Faction()
        self.assertIsInstance(faction.espionageGoal, dict)
        
    def testNewEspionageGoalResets(self):
        faction = Faction()
        faction.setNewEspionageGoal()
        self.assertEqual(faction.espionageGoal['complete'], False)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
