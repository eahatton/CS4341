import sys
sys.path.insert(0,'..bomberman')
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple
from itertools import count
from PIL import Image
import d3dshot


#PyTorch Imports

import torch


print(torch.cuda.is_available())