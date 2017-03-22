from generate import Generator

# 5k is probably a limit of customer API
generator = Generator(1000)
generator.generate()
#generator.print()
# generator.save(absolute_timestamps=True)
generator.track('9e898732-a289-11e6-bc55-14187733e19e', absolute_timestamps=True)
