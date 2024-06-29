#!/usr/bin/env python

from sys import argv
from typing import Callable, List

import matplotlib.pyplot as plt
import numpy as np
from rich import print


class Hash:
    """Define a list of hash functions."""

    @staticmethod
    def _loselose_(key: str):
        """loselose hash function."""

        hashv = 0
        for c in key:
            hashv += ord(c)

        return hashv

    @staticmethod
    def _djb2_(key: str):
        """djb2 hash function."""

        hashv = 5381
        for c in key:
            hashv = ((hashv << 5) + hashv) + ord(c)

        return hashv

    @staticmethod
    def _sdbm_(key: str):
        """sdbm hash function."""

        hashv = 0
        for c in key:
            hashv = ord(c) + (hashv << 6) + (hashv << 16) - hashv

        return hashv

    @staticmethod
    def _fnv1a_(key: str):
        """fnv-1a hash function."""

        hashv = 2166136261
        fnv_prime = 16777619
        for c in key:
            hashv ^= ord(c)
            hashv *= fnv_prime

        return hashv

    @staticmethod
    def _jenkins_(key: str):
        """jenkins hash function."""

        hashv = 0
        for c in key:
            hashv += ord(c)
            hashv += hashv << 10
            hashv ^= hashv >> 6

        hashv += hashv << 3
        hashv ^= hashv >> 11
        hashv += hashv << 15

        return hashv

    @staticmethod
    def _myhash_(key: str):
        """myhash function (terrible)."""

        hashv = 0
        for c in key:
            hashv += ord(c) * 29

        return hashv


def main(words: List[str], hashfn: Callable[[str], int], buckets: int, step: int):
    """Plot distributions of hashfn."""

    words_hashes = np.array([hashfn(word) % buckets for word in words])
    unique, counts = np.unique(words_hashes, return_counts=True)
    colldict = dict(zip(unique, counts))
    collisions = 0

    for hash in words_hashes:
        if colldict[hash] > 1:
            collisions += 1

    print(f"Total collisions of [b]{hashfn.__name__.split('_')[1]}[/]: {collisions}")

    bins = range(0, buckets + step, step)
    hist, edges = np.histogram(words_hashes, bins=bins)
    labels = [f"{edges[i]}-{edges[i+1]}" for i in range(len(edges) - 1)]

    plt.bar(labels, hist)
    plt.xlabel("Bucket Index Range")
    plt.ylabel("Occurrences")
    plt.title(
        f"{len(words)} words against {hashfn.__name__.split('_')[1]} hash fun"
        f"ction | {buckets=} -- {step=}"
    )

    plt.show()


if __name__ == "__main__":
    hashesfuncs = {
        "loselose": Hash._loselose_,
        "djb2": Hash._djb2_,
        "sdbm": Hash._sdbm_,
        "fnv1a": Hash._fnv1a_,
        "jenkins": Hash._jenkins_,
        "myhash": Hash._myhash_,
    }

    with open("./stuff.txt", "r") as f:
        try:
            main(
                [x.split("\n")[0] for x in f.readlines()],
                hashesfuncs[argv[1]],
                int(argv[2]),
                int(argv[3]),
            )
        except KeyError:
            print("Hash function not found!")
            print(f"Available: {hashesfuncs.keys()}")
