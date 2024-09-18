import java
import jmri

# Sets up an Inglenook Shunting Puzzle to sort trucks on sidings

# The program can be run in simulation mode first (advised) to get an idea of what will happen
 
# 1) Run the Toplevel InglenookShuntingPuzzle.py (this file)

# 2) Read the help accessed from the menu to get an idea of what the puzzle does 

InglenookShuntingPuzzle = jmri.util.FileUtil.getExternalFilename('program:jython//InglenookShuntingPuzzle.py')
execfile(InglenookShuntingPuzzle)