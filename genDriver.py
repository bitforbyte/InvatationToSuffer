import sys
import generateInfo as gi

def main(argv):
    numRounds = 250
    mg = gi.MixGen(4, 260, 2, 32, numRounds)
    mg.createRounds(True)
    

if __name__ == "__main__":
    main(sys.argv[1:])