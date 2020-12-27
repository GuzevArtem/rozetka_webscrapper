import random
import math
import datetime
import matplotlib.pyplot as plt

def get_rand_value_in_range(min_extent, max_extent):
    val = []
    for min, max in zip(min_extent, max_extent):
        val.append(random.random()*(max-min)+min)
    return val


def distance(a, b):
    res = 0.0
    for x, y in zip(a, b):
        res += (y-x)**2
    return math.sqrt(res)


class Point:
    def __init__(self, value):
        self.value = value
        self.cluster = None


class Centroid: #aka cluster
    def __init__(self, center):
        self.center = center #point
        self.points = [] #array of points
    
    def distance(self, point):
        return distance(self.center.value, point.value)
    
    def recalculate_center(self):
        total_count = len(self.points)
        if total_count <= 0:
            total_count = 1.0
        total_sum = [ 0.0 for _ in self.center.value ]
        for p in self.points:
            for i in range(len(self.center.value)):
                total_sum[i] += p.value[i]
        self.center.value = [ s/total_count for s in total_sum ]
    
    def add_point(self, point):
        self.points.append(point)
        
    def calc_variation(self):
        variation = 0.0
        for p in self.points:
            variation += distance(self.center.value, p.value)
        return variation
        
    def equals(a, b):
        if a is None and b is None:
            return None
        if a is None or b is None:
            return False
        for x, y in zip(a.center.value, b.center.value):
            if x != y:
                return False
        return True


class ClusterWorker:
    def __init__(self, points, total_clusters_count, min_extent, max_extent):
        self.min_extent = min_extent
        self.max_extent = max_extent
        self.points = points if len(points) == 0 or isinstance(points[0], Point) else [ Point(p) for p in points ]
        self.clusters = [Centroid(Point(get_rand_value_in_range(self.min_extent, self.max_extent))) for _ in range(total_clusters_count)]
        self.iteration = 0
        
    def clear_clusters_points(self):
        for c in self.clusters:
            c.points = []
        
    def append_by_distance(self):
        for p in self.points:
            min_distance = float("inf")
            nearest_cluster = None
            for c in self.clusters:
                distance = c.distance(p)
                if distance < min_distance:
                    min_distance = distance
                    nearest_cluster = c
            nearest_cluster.add_point(p)
            
    def recalculate_centroids(self):
        for c in self.clusters:
            c.recalculate_center()
            
    def check_cluster_changes(self):
        total_points_changed = 0
        for c in self.clusters:
            for p in c.points:
                if not Centroid.equals(p.cluster, c):
                    total_points_changed += 1
                    p.cluster = c
        return total_points_changed
    
    def calc_total_variation(self):
        variation = 0.0
        for c in self.clusters:
            variation += c.calc_variation()
        return variation
    
    def iterate(self, max_iteration, minimum_changes = 0):
        self.clear_clusters_points()
        self.append_by_distance()
        self.recalculate_centroids()
        total_changed = self.check_cluster_changes()
        self.iteration += 1
        return total_changed > minimum_changes and self.iteration < max_iteration

    def solve(self, iterations_limit):
        variation_history = []
        global_start = datetime.datetime.now()
        time_start = global_start
        while self.iterate(iterations_limit):
            variation = self.calc_total_variation()
            variation_history.append(variation)
            time_end = datetime.datetime.now()
            print("Iteration: ", self.iteration, "/", iterations_limit , "Variation:", variation, "Iteration time:", time_end - time_start, "Total time spent:", time_end - global_start, end="\r")
            time_start = datetime.datetime.now()
        print("Total iterations: ", self.iteration, "/", iterations_limit, "Variation:", variation, "Time spent:", datetime.datetime.now() - global_start)

        return self.clusters, variation_history

    def plot(clusters, 
             colors = [
                        'blue',
                        'green',
                        'red',
                        'cyan',
                        'magenta',
                        'yellow',
                        'black',
                        #'white', #invisible on plot
                        'lightblue',
                        'darkgrey'
                      ]):

        num = 0
        for c in clusters:
            xs = [x.value[0] for x in c.points]
            ys = [x.value[1] for x in c.points]
            plt.scatter(xs, ys, c=colors[num%len(colors)])
            plt.scatter(c.center.value[0], c.center.value[1], c=colors[(num+1)%len(colors)], marker = "x")
            num += 1
        plt.show()





