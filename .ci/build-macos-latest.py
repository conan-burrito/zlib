from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add(settings={"os.version": "10.13"})
    builder.add()
    builder.run()
