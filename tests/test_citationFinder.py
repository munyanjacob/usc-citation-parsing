import sys
sys.path.append('../src')

def t(x):
    return x + 1

def test_default():
    assert t(2) == 3