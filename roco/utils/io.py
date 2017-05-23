"""
Some IO utilities for roco.
"""

from os.path import join

from yaml import safe_load

from roco import ROCO_DIR

def load_yaml(file_name):
    if file_name[-5:] != '.yaml':
        file_name += '.yaml'

    fqn = join(ROCO_DIR, 'library', file_name)
    with open(fqn, 'r') as fd:
        return safe_load(fd)
