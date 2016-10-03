from generate import Generator

# 5k is probably a limit of customer API
generator = Generator(5000)
generator.generate()
#generator.print()
generator.save()
#generator.track()
