from generate import Generator

# 5k is probably a limit of customer API
generator = Generator(50000)
generator.generate()
#generator.print()
generator.save(absolute_timestamp=True)
generator.track('9e898732-a289-11e6-bc55-14187733e19e', absolute_timestamps=True)
