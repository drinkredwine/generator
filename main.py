from generate import Generator

# 5k is probably a limit of customer API
generator = Generator(2000)
generator.generate()
#generator.print()
generator.save()
#generator.track()
