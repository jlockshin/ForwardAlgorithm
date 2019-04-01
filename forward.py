import argparse
from math import log

# Parse in the arguments for the program:
parser = argparse.ArgumentParser()

# n is the number of normal states
parser.add_argument('-n', dest='n', required=True,
                    help='Use flag for number of states input',
                    default=True)

# s is a sequence of A, C, G, T
parser.add_argument('-s', dest='sequence', required=True,
                    help='Use flag for sequence input',
                    default=False)

# e is the emission probabilities
parser.add_argument('-e', dest='emissions', required=True,
                    help='Use flag for emissions input',
                    default=False)

# t is the transition probabilities
parser.add_argument('-t', dest='transitions', required=True,
                    help='Use flag for transitions input',
                    default=False)

args, unknown = parser.parse_known_args()


# Read in input info
def read_probabilities(file):
    """ Reads input files containing probabilities"""
    f = open(file, "r")
    probabilities = []
    for line in f:
        lines = [i for i in line.rstrip().split(" ")]
        probabilities.append(lines)
    f.close()
    return probabilities


def forward(sequence, states, transition_probs, emission_probs):
    """ Performs the forward algorithm
        Returns the dictionary of states and state probabilities
        As well as the total probability of the sequence """

    # Initialization
    fwd_dict = [{}]

    for s in range(states + 2):
        fwd_dict[0][s] = 0

    fwd_dict[0][0] = 1

    # Forward algorithm:
    # Loop through characters in the sequence
    for char in range(len(sequence)):

        fwd_dict.append({})

        # Loop through regular states plus 1 beginning and 1 end state (2 silent states total)
        for curr_state in range(states + 2):

            # Find the emission probability
            e_prob = 0
            for e in emission_probs:
                if int(e[0]) == curr_state and e[1] == sequence[char]:
                    e_prob = float(e[2])

            # Find the transition probability
            total = 0
            for state in range(states + 2):
                trans_prob = 0
                for t in transition_probs:
                    if int(t[0]) == state and int(t[1]) == curr_state:
                        trans_prob = float(t[2])

                # Add the probability to the dictionary
                total += (fwd_dict[char][state] * trans_prob)
                fwd_dict[char+1][curr_state] = total * e_prob

    # Termination step
    prob = 0
    final_state = states + 1

    for i in range(states + 1):
        for t in transition_probs:
            if int(t[0]) == i and int(t[1]) == final_state:
                trans_prob = float(t[2])

        # Calculate the total probability
        prob += (fwd_dict[len(sequence)][i] * trans_prob)

    return fwd_dict, prob


def print_log_prob(sequence, n, forward_seq):
    """ Prints L number of lines, with n columns per line """

    # Loop through number of characters in the sequence
    for l in range(1, len(sequence) + 1):
        state_probs = []

        # Loop through number of regular states:
        for i in range(1, n + 1):
            # Calculate the log probabilities
            if forward_seq[l][i] == 0:
                state_probs.append(-1000000.00)
            else:
                logP = round(log(forward_seq[l][i], 2), 2)
                state_probs.append(logP)

        # Print the probabilities in the appropriate format
        line = ""
        for prob in state_probs:
            line += str(prob) + " "
        print(line)


# Set commandline arguments to variables
n = args.n
sequence = args.sequence

# Read in the probability files
transitions = read_probabilities(args.transitions)
emissions = read_probabilities(args.emissions)

# Perform forward algorithm
forward_sequence, probability = forward(sequence, int(n), transitions, emissions)

# Print L + 1 lines
print_log_prob(sequence, int(n), forward_sequence)
print("%.2f" % log(probability))
