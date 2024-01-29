import numpy as np
from random import randint, random
import matplotlib.pyplot as plt


class City():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"

    def distance(self, city):
        return np.sqrt((self.x - city.x)**2 + (self.y - city.y)**2)


class Graph():
    def __init__(self, filename=None, matrice_distance=None, cities_position=None):
        self.cities = []
        self.matrice_distance = np.array([])

        if (filename is not None):
            data = np.genfromtxt(
                filename, delimiter=';', skip_header=1, dtype=np.float64)

            for d in data:
                self.cities.append(City(d[0], d[1]))

        if (cities_position is not None):
            for c in cities_position:
                self.cities.append(City(c[0], c[1]))

        if (matrice_distance is None):
            self.matrice_distance = np.zeros(
                (len(self.cities), len(self.cities)))
            for i in range(len(self.cities)):
                for j in range(len(self.cities)):
                    if (i != j):
                        distance = self.cities[i].distance(self.cities[j])
                        self.matrice_distance[i][j] = distance
                    else:
                        self.matrice_distance[j][i] = np.inf
        else:
            self.matrice_distance = np.array(matrice_distance)

        # print matrice distance shape
        print("matrice distance shape is", self.matrice_distance.shape)

    def __str__(self):
        return f"Graph with {len(self.cities)} cities"

    def copy(self):
        g = Graph(self.filename)
        return g

    def get_distance(self, chemin):
        distance = 0
        for i in range(len(chemin)):
            from_city = int(chemin[i])
            to_city = int(chemin[(i + 1) % len(chemin)])
            # try:
            distance += self.matrice_distance[from_city][to_city]
            # except:
            # print("from", from_city, "to", to_city)
        return distance

    def swap_with_next(self, chemin, i):
        new_chemin = chemin.copy()
        new_chemin[i], new_chemin[(
            i + 1) % len(chemin)] = new_chemin[(i + 1) % len(chemin)], new_chemin[i]
        return new_chemin

    def swap_indexes(self, chemin, i, j):
        new_chemin = chemin.copy()
        new_chemin[i], new_chemin[j] = new_chemin[j], new_chemin[i]
        return new_chemin

    def move_city_at(self, chemin, city_id, i):
        new_chemin = chemin.copy()
        new_chemin = np.delete(new_chemin, city_id)
        new_chemin = np.insert(new_chemin, i, city_id)
        return new_chemin

    def voisinage_2_opt(self, chemin, coupure1, coupure2):
        if (coupure1 > coupure2):
            coupure1, coupure2 = coupure2+1, coupure1-1

        new_chemin = chemin.copy()
        cut = new_chemin[coupure1:coupure2+1][::-1]
        # put cut between coupure1 and coupure2
        new_chemin = np.concatenate(
            (new_chemin[:coupure1], cut, new_chemin[coupure2+1:]))
        return new_chemin

    def random_voisinage(self, chemin):
        random_transfo = randint(0, 3)
        if random_transfo == 0:
            return self.swap_with_next(chemin, randint(0, len(chemin) - 1))
        elif random_transfo == 1:
            return self.swap_indexes(chemin, randint(0, len(chemin) - 1), randint(0, len(chemin) - 1))
            # return self.move_city_at(chemin, randint(0, len(chemin) - 1), randint(0, len(chemin) - 1))
        elif random_transfo == 2:
            return self.swap_indexes(chemin, randint(0, len(chemin) - 1), randint(0, len(chemin) - 1))
        elif random_transfo == 3:
            return self.voisinage_2_opt(chemin, randint(0, len(chemin) - 1), randint(0, len(chemin) - 1))

    def random_voisinage_smart(self, chemin, same_pairs=[]):
        random_transfo = randint(0, 2)
        if random_transfo == 0:
            return self.swap_with_next(chemin, randint(0, len(chemin) - 1))
        elif random_transfo == 1:
            # take random pair of cities that is not in same_pairs
            i = randint(0, len(chemin) - 1)
            j = randint(0, len(chemin) - 1)
            while (i, j) in same_pairs or (j, i) in same_pairs:
                i = randint(0, len(chemin) - 1)
                j = randint(0, len(chemin) - 1)
            return self.swap_indexes(chemin, i, j)
        elif random_transfo == 2:
            return self.voisinage_2_opt(chemin, randint(0, len(chemin) - 1), randint(0, len(chemin) - 1))

    def verif_dupli(self, chemin):
        unique, counts = np.unique(chemin, return_counts=True)
        if len(unique) != sum(counts):
            print("duplicate in chemin")
        return False

    def best_chemin_stupid(self, chemin, max_iter=100):
        best_chemin = chemin.copy()
        best_distance = self.get_distance(chemin)
        for i in range(max_iter):
            new_chemin = self.random_voisinage(best_chemin)
            self.verif_dupli(new_chemin)
            new_distance = self.get_distance(new_chemin)
            if new_distance < best_distance:
                best_chemin = new_chemin
                best_distance = new_distance
        return best_chemin

    def best_chemin_less_stupid(self, chemin, max_iter=100):
        best_chemin = chemin.copy()
        best_distance = self.get_distance(chemin)

        greedy_paths = []
        for i in range(len(self.cities)):
            chemin = self.best_chemin_greedy(i)
            greedy_paths.append(chemin)

        # find all pairs of cities that are next to each other in all greedy paths
        same_pairs = []
        pairs_per_path = {}
        for p in range(len(greedy_paths)):
            pairs_per_path[p] = []
            for i in range(len(greedy_paths[p])):
                pair = (greedy_paths[p][i], greedy_paths[p]
                        [(i+1) % len(greedy_paths[p])])
                same_pairs.append(pair
                                  )

        # print("same_pairs", same_pairs)
        # remove any pair that is not in all greedy paths
        for pair in same_pairs:
            for p in range(len(greedy_paths)):
                if pair not in pairs_per_path[p] and pair[::-1] not in pairs_per_path[p]:
                    try:
                        same_pairs.remove(pair)
                        same_pairs.remove(pair[::-1])
                    except:
                        pass

        # print("same_pairs", same_pairs)

        for i in range(max_iter):
            new_chemin = self.random_voisinage_smart(best_chemin)
            self.verif_dupli(new_chemin)
            new_distance = self.get_distance(new_chemin)
            if new_distance < best_distance:
                best_chemin = new_chemin
                best_distance = new_distance
        return best_chemin

    def best_chemin_greedy(self, start=0):
        chemin = []
        chemin.append(start)
        cities_left = [i for i in range(len(self.cities))]
        cities_left.remove(start)
        while len(cities_left) > 0:
            last_city = chemin[-1]
            best_city = cities_left[0]
            best_distance = self.matrice_distance[last_city][best_city]
            for city in cities_left:
                distance = self.matrice_distance[last_city][city]
                if distance < best_distance:
                    best_city = city
                    best_distance = distance
            chemin.append(best_city)
            cities_left.remove(best_city)
        return chemin

    def best_start_greedy(self):
        best_chemin = []
        best_distance = np.inf
        for i in range(len(self.cities)):
            chemin = self.best_chemin_greedy(i)
            distance = self.get_distance(chemin)
            if distance < best_distance:
                best_chemin = chemin
                best_distance = distance
        return best_chemin

    def recuit_simule(self, temperature_initiale=10000, L=5, alpha=0.9, K=1000):
        # set temp
        temperature = temperature_initiale
        # init chemin with greedy one
        chemin_actuel = self.best_start_greedy()
        # init best chemin by first one
        meilleur_chemin = chemin_actuel
        best_distance = self.get_distance(chemin_actuel)

        k = 0
        while k < K:
            for i in range(L):
                chemin_voisin = self.random_voisinage(chemin_actuel)
                distance_voisin = self.get_distance(chemin_voisin)

                delta = distance_voisin - best_distance

                # option is better or same
                if (delta <= 0):
                    chemin_actuel = chemin_voisin
                    if (distance_voisin < best_distance):
                        best_distance = distance_voisin
                        meilleur_chemin = chemin_voisin
                        k = 0
                    else:
                        k += 1
                # option is worse but we take it
                elif np.random.uniform(0, 1) <= np.exp((best_distance-distance_voisin)/temperature):
                    chemin_actuel = chemin_voisin
                    k += 1
                # option is worse and we don't take it
                else:
                    k += 1

            # reduce temperature
            temperature = temperature * alpha
            chemin_actuel = meilleur_chemin

        return meilleur_chemin

    def get_diff(self, chemin1, chemin2):
        diff = []
        for i in range(len(chemin1)):
            if chemin1[i] != chemin2[i]:
                # print("diff at", i, "is", chemin1[i], "vs", chemin2[i])
                diff.append(i)

        return diff

    def draw_arrow(self, from_city, to_city, color='red'):
        # get vector (x, y) from from_city to to_city
        x = (self.cities[to_city].x - self.cities[from_city].x)
        y = (self.cities[to_city].y - self.cities[from_city].y)

        # reduce length of vector by 0.1px
        x = x * 0.9
        y = y * 0.9

        plt.arrow(self.cities[from_city].x, self.cities[from_city].y,
                  x, y, head_width=0.01, head_length=0.01, fc=color, ec=color)

    def show_chemin(self, chemin, step=0, color='red'):

        cities_in_chemin = [self.cities[i] for i in chemin]

        plt.scatter([c.x for c in cities_in_chemin],
                    [c.y for c in cities_in_chemin])

        for i in range(len(chemin)):
            from_city = int(chemin[i])
            to_city = int(chemin[(i + 1) % len(chemin)])
            self.draw_arrow(from_city, to_city, color)
            # wait 0.5s
            if (step > 0):
                plt.pause(step)
        plt.show()

    def show_graph(self):
        plt.show()

    def get_chemin_ant_algorithm(self, num_ants, num_iterations, alpha, beta, evaporation_rate):
        # Initialize pheromone levels
        pheromones = np.ones_like(self.matrice_distance)

        for iteration in range(num_iterations):
            ant_paths = []

            for ant in range(num_ants):
                current_city = np.random.randint(len(self.cities))
                path = [current_city]

                while len(path) < len(self.cities):
                    # Calculate probabilities for the next city based on pheromone levels and distances
                    probabilities = self.calculate_probabilities(
                        current_city, path, pheromones, alpha, beta)

                    # Choose the next city using the probabilities
                    next_city = np.random.choice(
                        len(self.cities), p=probabilities)

                    # Move to the next city
                    path.append(next_city)
                    current_city = next_city

                ant_paths.append(path)

            # Update pheromone levels
            pheromones = self.update_pheromones(
                pheromones, ant_paths, evaporation_rate)

        # Find the best path based on pheromone levels
        best_path = min(ant_paths, key=lambda path: self.get_distance(path))
        return best_path

    def calculate_probabilities(self, current_city, path, pheromones, alpha, beta):
        unvisited_cities = [city for city in range(
            len(self.cities)) if city not in path]
        probabilities = np.zeros(len(self.cities))

        for city in unvisited_cities:
            pheromone_factor = pheromones[current_city][city] ** alpha
            distance_factor = 1 / \
                (self.matrice_distance[current_city][city] ** beta)
            total_factor = pheromone_factor * distance_factor
            probabilities[city] = total_factor

        # Normalize probabilities to make them sum to 1
        probabilities /= probabilities.sum()

        return probabilities

    def update_pheromones(self, pheromones, ant_paths, evaporation_rate):
        pheromones *= (1 - evaporation_rate)  # Evaporation

        for path in ant_paths:
            for i in range(len(path) - 1):
                from_city = path[i]
                to_city = path[i + 1]
                pheromones[from_city][to_city] += 1 / self.get_distance(path)

        return pheromones

    def calculate_most_centered_city(self):
        # Calculate the center of the cities
        center_x = sum([city.x for city in self.cities]) / len(self.cities)
        center_y = sum([city.y for city in self.cities]) / len(self.cities)

        # Find the city closest to the center
        center_city = min(self.cities, key=lambda city: city.distance(
            City(center_x, center_y)))

        city_position = self.cities.index(center_city)
        print("center city is", center_city, "at position", city_position)
        return center_city, city_position

    def split_cities_into_parts(self, n):
        # get the most centered city
        center_city, city_position = self.calculate_most_centered_city()

        # split into n parts
        parts = [[] for _ in range(n)]

        # from the center as the center of a circle, split the cities into n parts
        for city in self.cities:
            # calculate angle between center city and current city relative to the x axis
            angle = np.arctan2(city.y - center_city.y, city.x - center_city.x)
            # calculate the part number (0 to n-1) according to the angle
            part = int(np.floor(angle / (2 * np.pi / n)))
            # add the city to the part
            parts[part].append([city.x, city.y])

        # make sure each part has the center city as first city
        for part in parts:
            # remove the center city from the part
            if ([center_city.x, center_city.y] in part):
                part.remove([center_city.x, center_city.y])
            # add the center city as first city of the part
            part.insert(0, [center_city.x, center_city.y])
        return parts, city_position

    def get_n_optimal_paths(self, n):
        # Split the cities into n parts
        parts, city_position = self.split_cities_into_parts(n)
        print("parts", parts[0], "\n\n", parts[1])
        # Calculate the optimal path for each part
        optimal_paths = []
        for part in parts:
            sub_g = Graph(cities_position=part)
            path = sub_g.best_chemin_greedy(start=0)
            optimal_paths.append(self.convert_path(part, path))

        return optimal_paths

    def convert_path(self, local_city_list, path):
        pos = [[c.x, c.y] for c in self.cities]
        global_path = []
        for city_index in path:
            # look index of city in local_city_list in global_city_list
            print("looking for index of",
                  local_city_list[city_index], "in current city list")
            global_path.append(pos.index(
                local_city_list[city_index]))
        return global_path

    def show_multiples_paths(self, chemins, step=0):
        colors = ['red', 'green', 'blue', 'yellow',
                  'orange', 'purple', 'pink', 'brown', 'black']

        plt.scatter([c.x for c in self.cities],
                    [c.y for c in self.cities])

        for c_i in range(len(chemins)):
            chemin = chemins[c_i]
            for i in range(len(chemin)):
                from_city = int(chemin[i])
                to_city = int(chemin[(i + 1) % len(chemin)])
                self.draw_arrow(from_city, to_city, colors[c_i % len(colors)])
                # wait 0.5s
                if (step > 0):
                    plt.pause(step)
        plt.show()
