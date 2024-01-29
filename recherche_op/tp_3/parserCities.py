def get_matrice_from_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        matrice = []
        # skip first 7 lines
        lines = lines[7:]
        for line in lines:
            matrice.append([float(i) for i in line.split()])
        return matrice


def get_cities_positions_from_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        cities = []
        # skip first 6 lines and last one
        lines = lines[6:-1]
        for line in lines:
            infos = [float(i) for i in line.split()]
            cities.append([infos[1], infos[2]])
        return cities
