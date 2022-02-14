#!/usr/bin/env python3

from random import randint
from constants import *


def gen_indexes_in_confusion(n=len(confusion)):
    index_dict = {}
    for i, num in enumerate(confusion[:n]):
        if num in index_dict:
            index_dict[num][1] = i
        else:
            index_dict[num] = [i, None]
    
    return index_dict


def gen_candidate():

    indexes_in_confusion = gen_indexes_in_confusion()

    candidate = bytearray()
    for i in range(16):

        while True:
            first_index = randint(0, 255)
            first_val = confusion[first_index]

            second_val = TARGET_STR[i]^first_val
            if second_val not in indexes_in_confusion:
                continue

            _, second_index = indexes_in_confusion[second_val]
            if second_index is None or second_index < 256:
                continue

            second_index -= 256

            candidate.append(first_index)
            candidate.append(second_index)
            break
    
    return candidate



def __debug():
    candidate = gen_candidate()
    print(list(candidate))


if __name__ == '__main__':
    __debug()