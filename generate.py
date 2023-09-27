#!/usr/bin/env python

def generate():
     """
     generate constraint for the einstein riddle
     we define the variable h_ijk as house i with option k of a property j (for example, nationality is a property, German is a choice)
     since there are 5 houses, each house has 5 properties, each property has 5 choices, there should be in total 5^3=125 variables
     convention:
     property 1: red, green, white, yellow, blue
     property 2: nationality: brit, swede, dane, norwegian, german
     property 3: beverage: tea, coffee, milk, beer, water
     property 4: cigar: pall mall, dunhill, prince, blends, bluemasters
     property 5: pet: dog, birds, cats, horse, fish
     """
     cnf = open("einstein.cnf", 'w+')
     var_dict = {}
     count = 1
     var_count = 125
     cnf.write("p cnf 125 1117 \n")
     clause_count = 0
     for house in range(1,6):
          for properties in range(1,6):
               for choices in range(1,6):
                    var_dict[(house, properties, choices)] = count
                    count += 1
     print (var_dict)
     #each attribute must appear exactly once for each house
     for properties in range(1,6):
          for choices in range(1,6):
                    #at least: for each property, each choice should appear at least once among all houses
                    cnf.write(str(var_dict[(1, properties, choices)]) + " " + str(var_dict[(2, properties, choices)]) + " " + str(var_dict[(3, properties, choices)]) + " " + str(var_dict[(4, properties, choices)]) + " " + str(var_dict[(5, properties, choices)]) + " 0\n")
                    clause_count += 1
                    #at most: for each property, each choice should appear at most once
                    for house in range(1,6):
                         for house2 in range(1,6):
                              if house != house2:
                                   cnf.write(str(-var_dict[(house, properties, choices)]) + " " + str(-var_dict[(house2, properties, choices)]) + " 0\n")
                                   clause_count += 1
     #each house has exactly one choice for each property
     for properties in range(1,6):
          for house in range(1,6):
               cnf.write(str(var_dict[(house, properties, 1)]) + " " + str(var_dict[(house, properties, 2)]) + " " + str(var_dict[(house, properties, 3)]) + " " + str(var_dict[(house, properties, 4)]) + " " + str(var_dict[(house, properties, 5)]) + " 0\n")
               clause_count += 1
               for choice in range(1,6):
                    for choice2 in range(1,6):
                         if choice != choice2:
                              cnf.write(str(-var_dict[(house, properties, choice)]) + " " + str(-var_dict[(house, properties, choice2)]) + " 0\n")
                              clause_count += 1
     #encode the hints
     for house in range(1,6):
          cnf.write(str(var_dict[(house, 1, 1)]) + " " + str(-var_dict[(house, 2, 1)]) + " 0\n") #brit -> red
          cnf.write(str(var_dict[(house, 5, 1)]) + " " + str(-var_dict[(house, 2, 2)]) + " 0\n") #swede -> dog
          cnf.write(str(var_dict[(house, 3, 1)]) + " " + str(-var_dict[(house, 2, 3)]) + " 0\n") #dane -> tea
          cnf.write(str(var_dict[(house, 3, 2)]) + " " + str(-var_dict[(house, 1, 2)]) + " 0\n") #green -> coffee
          cnf.write(str(var_dict[(house, 5, 2)]) + " " + str(-var_dict[(house, 4, 1)]) + " 0\n") #pall mall -> birds
          cnf.write(str(var_dict[(house, 4, 2)]) + " " + str(-var_dict[(house, 1, 4)]) + " 0\n") #yellow -> dunhill
          cnf.write(str(var_dict[(house, 3, 4)]) + " " + str(-var_dict[(house, 4, 5)]) + " 0\n") #bluemaster -> beer
          cnf.write(str(var_dict[(house, 4, 3)]) + " " + str(-var_dict[(house, 2, 5)]) + " 0\n") #german -> prince
          clause_count += 8
     for house in range(1,5):
          cnf.write(str(var_dict[(house+1, 1, 3)]) + " " + str(-var_dict[(house, 1, 2)]) + " 0\n") #green on the left of white
          clause_count += 1
     for house in range(2, 5):
          cnf.write(str(-var_dict[(house, 4, 4)]) + " " + str(var_dict[(house-1, 5, 3)]) + " " +  str(var_dict[(house+1, 5, 3)]) + " 0\n") #blend next to cat
          cnf.write(str(-var_dict[(house, 5, 4)]) + " " + str(var_dict[(house-1, 4, 2)]) + " " +  str(var_dict[(house+1, 4, 2)]) + " 0\n") #horse next to dunhill
          cnf.write(str(-var_dict[(house, 2, 4)]) + " " + str(var_dict[(house-1, 1, 5)]) + " " +  str(var_dict[(house+1, 1, 5)]) + " 0\n") #norwegian next to blue
          cnf.write(str(-var_dict[(house, 4, 4)]) + " " + str(var_dict[(house-1, 3, 5)]) + " " +  str(var_dict[(house+1, 3, 5)]) + " 0\n") #blends next to water
          clause_count += 4
          
     cnf.write(str(-var_dict[(5, 1, 2)]) + " 0\n" )#green cannot be the last house
     cnf.write(str(var_dict[(3, 3, 3)]) + " 0\n")#man in center drinks milk
     cnf.write(str(var_dict[(1, 2, 4)]) + " 0\n")#norwegian in first house
     cnf.write(str(-var_dict[(5, 4, 4)]) + " " + str(var_dict[(4, 5, 3)]) + " 0\n") #blend is 5 -> cat is 4
     cnf.write(str(-var_dict[(1, 4, 4)]) + " " + str(var_dict[(2, 5, 3)]) + " 0\n") #blend is 1 -> cat is 2
     cnf.write(str(-var_dict[(5, 5, 4)]) + " " + str(var_dict[(4, 4, 2)]) + " 0\n") #horse is 5 -> dunhill is 4
     cnf.write(str(-var_dict[(1, 5, 4)]) + " " + str(var_dict[(2, 4, 2)]) + " 0\n") #horse is 1 -> dunhill is 2
     cnf.write(str(-var_dict[(5, 2, 4)]) + " " + str(var_dict[(4, 1, 5)]) + " 0\n") #norwegian is 5 -> blue is 4
     cnf.write(str(-var_dict[(1, 2, 4)]) + " " + str(var_dict[(2, 1, 5)]) + " 0\n") #norwegian is 1 -> blue is 2
     cnf.write(str(-var_dict[(5, 4, 4)]) + " " + str(var_dict[(4, 3, 5)]) + " 0\n") #blend is 5 -> water is 4
     cnf.write(str(-var_dict[(1, 4, 4)]) + " " + str(var_dict[(2, 3, 5)]) + " 0\n") #blend is 1 -> water is 2
     clause_count += 11

generate()
