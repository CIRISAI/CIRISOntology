#!/usr/bin/env python3
"""The frozen deterministic seed formula.

Path-MC prereg:
    seed = 202608220000 + 1000000*L + 10000*N + 100*config_index + 10*batch + replica
    replica = 0,1 ; branch-specific dephased runs add 1,000,000,000*(branch+1)
Annihilating prereg: "the same deterministic seed formula as the prior path-MC prereg, plus
50,000,000,000 to distinguish this estimator."
"""
ANNIHILATING_OFFSET = 50_000_000_000
BRANCH_OFFSET = 1_000_000_000


def seed(L, N, config_index, batch, replica):
    return (202608220000 + 1_000_000 * L + 10_000 * N + 100 * config_index
            + 10 * batch + replica + ANNIHILATING_OFFSET)


def seed_pair(L, N, config_index, batch):
    return (seed(L, N, config_index, batch, 0), seed(L, N, config_index, batch, 1))
