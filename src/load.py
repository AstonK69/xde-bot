import yaml

if __name__ == '__main__':
    print('You ran the load file lol')
    exit()

path = f"{__file__}".replace("\\", "/")
path = path.replace("/load.py", "")

config = open(f"{path}/config.yaml")
config = yaml.load(config, Loader=yaml.FullLoader)
token = config.get("token")
cooldown = config.get("cooldown")


class Colours:
    standard = 0xc40e1a
    standard = 0xff0000
    blue = 0x0000ff
    green = 0x77dd77
    yellow = 0xeb9226
    astonblue = 0x00d5ff
