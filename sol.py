#!/usr/bin/env python3

from Z2_util import mult_inverse_and_vec
from constants import *
from gen_candidate import gen_candidate, gen_indexes_in_confusion
import sys


confusion_dict = gen_indexes_in_confusion(256)

def gen_candidates_from_confusion_at_input(confusion_at_input):

    candidates = [[]]

    for c in confusion_at_input:

        if c not in confusion_dict:
            return []

        index1, index2 = confusion_dict[c]

        if index2 is None:
            for candidate in candidates:
                candidate.append(index1)
        
        else: # index 2 is not None
            new_candidates = []

            for candidate in candidates:
                clone = candidate.copy()
                candidate.append(index1)
                clone.append(index2)
                new_candidates.append(clone)

            candidates.extend(new_candidates)

    return candidates


def reverse_iterations(candidate, remaining_iterations = 256):

    if remaining_iterations == 0:
        return candidate
    
    confusion_at_input = mult_inverse_and_vec(candidate)    
    new_candidates_list = gen_candidates_from_confusion_at_input(confusion_at_input)


    for new_candidate in new_candidates_list:
        result = reverse_iterations(new_candidate, remaining_iterations-1)
        if result is not None:
            return result

    return None


def main():

    if len(sys.argv) >= 2 and sys.argv[1] == "debug":
        debug()
    
    else:
        result = None
        while result is None:
            candidate = gen_candidate()
            result = reverse_iterations(candidate)
        
        print(result)


def debug():
    pass


if __name__ == "__main__":
    main()