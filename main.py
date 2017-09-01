import pickle
from time import time

# start = time()
# generator = Generator(50000)
# print("generated in {}s".format(time()-start))
# generator.generate()
# #generator.print()
#
# start = time()
# with open("generator.bin", "wb") as f:
#     pickle.dump(generator, f)
# print("saved in {}s".format(time()-start))

start = time()
with open("generator.bin", "rb") as f:
    generator = pickle.load(f)
print("loaded in {}s".format(time() - start))

print(generator.users[0])

generator.track('69db3a58-0d3c-11e7-adfc-141877340e97', absolute_timestamps=True)
# generator.save(absolute_timestamps=True)
# generator.track('9e898732-a289-11e6-bc55-14187733e19e', absolute_timestamps=True)
