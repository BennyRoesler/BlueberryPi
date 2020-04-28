import random
import os

#not needed. only to randomly print ascii art

dir = 'ascii_art'
filename = random.choice(os.listdir(dir))
path = os.path.join(dir, filename)

art = open(path, "r")
print(art.read())