from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add(settings={"arch": "armv7"})
    builder.add(settings={"arch": "armv8"})
    builder.add(settings={"arch": "x86"})
    builder.add(settings={"arch": "x86_64"})
    builder.run()
