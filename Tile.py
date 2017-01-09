
class Tile:

    def __init__(self, hexa):
        self.connectors = nb_to_list(hexa)
        self.nb_rots = hexa_to_nb_rot(hexa)

    def rot(self):
        # Effectue une rotation de la tuile d'un quart de tour dans le sens trigonométrique
        self.connectors = [self.connectors[-1]] + self.connectors[:-1]
        self.nb_rots += 1
        self.nb_rots %= 4

    def get_hexa(self):
        # Renvoie l'hexadecimal correspondant à la tuile
        tile = self
        while tile.nb_rots != 0:
            tile = tile.rot()
        hexa = 0
        for i, b in enumerate(tile.connectors):
            if b:
                hexa += 2**i
        return hexa

def nb_to_list(nb):
    # Prend le nombre hexadécimal d'une tuile et renvoie une liste de boolean codant la présence ou non des 4 connecteurs
    result = []
    a = nb
    for _ in range(4):
        result.append(a % 2 == 1)
        a //= 2
    return result


def hexa_to_nb_rot(hexa):
    rot_families = [[0, 1, 3, 5, 7, 15], [2, 6, 10, 14], [4, 12, 13], [8, 9, 11]]
    for nb_rot, rot_family in enumerate(rot_families):
        if hexa in rot_family:
            return nb_rot