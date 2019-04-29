# Programming Assignment 2 (Code name: NET BUSTER)

## Authors:
### Sam MacLean
### Kendall Nicley
### Parker [Lastname forgot]

## General things
There are multiple text files that we use in our code.  

* pub.txt, priv.txt, map.txt
  * List of public nodes, private nodes, and mappings between the two respectively.
* rounds\_dump.txt
  * Two and a half days of rounds on all public nodes, this will probably zipped up
* round\_one.txt
  * A single round extracted from the rounds_dump.txt file


## Part 1
The two files for part1 are `part1.py` and `kpart1.py`  
   `kpart1.py` is Kendall's version of the statistical analysis attack.

## Part 2
The program for part2 is `part2.py` and gathers all data it can about the network.

It can be run with the following arguments:
1. `[nothing]` No argument will print a comma seperated list of all nodes
2. `pub` will print a comma seperated list of all public nodes
3. `priv` will print a comma seperated list of all private nodes
4. `map` will print out a mapping of all nodes to it's connected peers
  * This is in a special format that is used by our code, it will be converted later for part 4

## Part 3 
There are multiple programs for part 3

1. `part3_harvester.py` the threaded program for dumping rounds to stdout
  * Redirected to rounds\_dump.txt
2. `part3_a.py` Builds sender/reciever pairs from the file `rounds_dump.txt` and prints to stdout
3. `part3_c.py` Reads from stdin for sender/reciever output, takes on argument which are the nodes that it should build friend relationships with

## Part 4
Programs for part 4
1. `part4_a.py` Builds private sender/reciever pairs from the file `rounds_dump.txt` and prints to stdout
2. `part4_c.py` The exact same as `part3_c.py` just copied for verboseness
