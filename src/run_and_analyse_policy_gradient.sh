#!/bin/sh

# Ad hoc script to run a particular policy gradient algorithm several times over.
# C-c C-v ed from bash history.
# Run from the current directory only!

CLASS="AveragedPolicyGradient"
NUMTRAIN=1000 # Train the bot 1000 times
NUMTRIALS=30 # Repeat experiment 30 times
GRAPH_TITLE="Averaged Policy Gradient"


function RepeatExperiment() {
  AGENT="$1"
  AGENT_PARAMS="$2"
  FILE_TEMPLATE="$3-$AGENT"
  for i in `seq -w 1 $NUMTRIALS`
  do
    OUT_FILE="data/${FILE_TEMPLATE}_$i.txt"
    echo 'python main.py' $NUMTRAIN $CLASS 'TicTacToe:' $AGENT_PARAMS:$AGENT '>' $OUT_FILE
    python main.py $NUMTRAIN $CLASS "TicTacToe:$AGENT_PARAMS:$AGENT" > $OUT_FILE
  done
}

echo "Generating data"
mkdir data

RepeatExperiment "OptimalAgent" "false" "first"
RepeatExperiment "RandomAgent" "false" "first"
RepeatExperiment "ScanAgent" "false" "first"

RepeatExperiment "OptimalAgent" "true" "second"
RepeatExperiment "RandomAgent" "true" "second"
RpeatExperiment "ScanAgent" "true" "second"


# Convert the win loss data into percentages
cd data
python ../../scripts/transform-to-percentages.py *.txt


# Add line numbers to the scripts
cd percentages
mkdir new
map 'cat -n @i > new/@i' `\ls *.txt`
mv new/* .


# Average all the runs, remove the last column (number of values with the
# given key), and sort the resultant by the keys.
../../../scripts/avg first-Optim*  | awk '{print $1 " " $2}' | sort -n > ../../../first-OptimalAgent.txt
../../../scripts/avg first-Rand*   | awk '{print $1 " " $2}' | sort -n > ../../../first-RandomAgent.txt
../../../scripts/avg first-Scan*   | awk '{print $1 " " $2}' | sort -n > ../../../first-ScannerAgent.txt

../../../scripts/avg second-Optim* | awk '{print $1 " " $2}' | sort -n > ../../../second-OptimalAgent.txt
../../../scripts/avg second-Rand*  | awk '{print $1 " " $2}' | sort -n > ../../../second-RandomAgent.txt
../../../scripts/avg second-Scan*  | awk '{print $1 " " $2}' | sort -n > ../../../second-ScannerAgent.txt

# Plot the data
cd ../../../
./scripts/plot "$GRAPH_TITLE - Percentage of games not lost (as first player)" 'Number of Runs' 'Percentage of games not lost' 'Optimal Agent, Random Agent, Scanner Agent' first-OptimalAgent.txt,first-RandomAgent.txt,first-ScannerAgent.txt  first.eps

./scripts/plot "$GRAPH_TITLE - Percentage of games not lost (as second player)" 'Number of Runs' 'Percentage of games not lost' 'Optimal Agent, Random Agent, Scanner Agent' second-OptimalAgent.txt,second-RandomAgent.txt,second-ScannerAgent.txt  second.eps

mv first.eps Report/$CLASS-first.eps
mv second.eps Report/$CLASS-second.eps

# Remove the averaged data files
rm *.txt
