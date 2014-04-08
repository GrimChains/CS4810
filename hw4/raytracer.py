__author__ = 'Frank Manns'

import sys
import Image
import math


class Sphere:
    def __init__(self, center, radius, color):
        if not isinstance(center, tuple):
            raise TypeError("center must be of type 'tuple'")
        if not isinstance(color, tuple):
            raise TypeError("color must be of type 'tuple'")
        self.center = center
        self.color = color
        self.radius = radius

    def normal_to_point(self, point):
        if not isinstance(point, tuple):
            raise TypeError("point must be of type 'tuple'")
        return normalize_vector(vector_bn_points(self.center, point))


class Plane:
    def __init__(self, vertices, color):
        if not isinstance(vertices, tuple):
            raise TypeError("vertices must be a tuple of floats")
        if len(vertices) != 4:
            raise ValueError("4 vertices expected. Received " + str(len(vertices)))
        if not isinstance(color, tuple):
            raise TypeError("color must be of type 'tuple'")
        self.vertices = vertices
        self.color = color
        self.normal = normalize_vector(self.vertices[0:3])

    def normal_to_point(self, point):
        return self.normal


def transform(x, y):
    s = (2.0*x - width) / max(width, height)
    t = (height - 2.0*y) / max(width, height)
    return s, t


def ray_sphere(p0, d, sph):
    """ http://www.csee.umbc.edu/~olano/435f02/ray-sphere.html """

    pc = sph.center
    r = sph.radius

    p0c = subtract(p0, pc)

    a = dot_product(d, d)
    b = dot_product(map(lambda k: 2*k, d), p0c)
    c = dot_product(p0c, p0c) - r**2

    try:
        t1 = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
        p1 = add(map(lambda k: t1*k, d), p0)
    except ValueError:
        t1 = None
    try:
        t2 = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
        p2 = add(map(lambda k: t2*k, d), p0)
    except ValueError:
        t2 = None

    return t1, t2


def ray_plane(p0, d, plane):
    """ Checks for collisions between a ray and plane """
    n = plane.normal
    D = plane.vertices[3]
    nR0 = dot_product(n, p0)
    nRd = dot_product(n, d)
    try:
        t = -(D + nR0) / nRd
        if t < 0:
            return None
        else:
            return t
    except ZeroDivisionError:
        return None


def rays_from_eye():
    # shoot a ray for each pixel in the image
    for y in range(0, height):
        for x in range(0, width):
            s, t = transform(x, y)
            direction = add(forward, map(lambda k: k*s, right))
            direction = add(direction, map(lambda k: k*t, up))

            collision = find_nearest_collision(eye, direction)
            collision_site = collision[0]
            collision_object = collision[1]
            if collision_site is not None:
                # invert normal if it points away from eye
                normal = collision_object.normal_to_point(collision_site)
                if dot_product(normal, direction) > 0:
                    normal = tuple(map(lambda k: k*-1, normal))
                color = (0, 0, 0)

                # remove current object from object lists
                if isinstance(collision_object, Sphere):
                    spheres.remove(collision_object)
                else:
                    planes.remove(collision_object)

                # shoot a ray from the collision site to all sun lights
                for light in sunlights:
                    dir = normalize_vector(light[0])
                    collision = find_nearest_collision(collision_site, dir)
                    if collision[0] is None:
                        object_color = collision_object.color
                        light_color = light[1]
                        dp = dot_product(normal, dir)
                        if dp < 0:
                            continue

                        current_color = (object_color[0]*light_color[0]*dp, object_color[1]*light_color[1]*dp,
                                         object_color[2]*light_color[2]*dp)
                        color = add(color, current_color)

                # shoot a ray from the collision site to all bulb lights
                for bulb in bulbs:
                    dir = vector_bn_points(collision_site, bulb[0])
                    collision = find_nearest_collision(collision_site, dir, point_light=True)
                    if collision[0] is None:
                        object_color = collision_object.color
                        light_color = bulb[1]
                        dir = normalize_vector(dir)
                        dp = dot_product(normal, dir)
                        if dp < 0:
                            continue

                        current_color = (object_color[0]*light_color[0]*dp, object_color[1]*light_color[1]*dp,
                                         object_color[2]*light_color[2]*dp)
                        color = add(color, current_color)

                color = convert_color(color)
                putpixel((x, y), color)

                # reinsert the current object
                if isinstance(collision_object, Sphere):
                    spheres.append(collision_object)
                else:
                    planes.append(collision_object)


def find_nearest_collision(origin, direction, point_light=False):
    """
        Input: Origin point and direction vector of ray
        Returns: point of nearest collision (if any) and the object
        that the ray collided with.
     """
    collisions = []
    # check for collisions with spheres
    for sphere in spheres:
        t1, t2 = ray_sphere(origin, direction, sphere)
        if t1 is not None and t1 > 0:
            collisions.append((t1, sphere))
        if t2 is not None and t2 > 0:
            collisions.append((t2, sphere))
    # check for collisions with planes
    for plane in planes:
        t = ray_plane(origin, direction, plane)
        if t is not None:
            collisions.append((t, plane))
    try:
        t = min(collisions)  # raises ValueError if collisions is empty
        collision = add(map(lambda k: t[0]*k, direction), origin)
        if point_light and t[0] > 1:
            return None, None
        else:
            return collision, t[1]
    except ValueError:
        return None, None


def convert_color(norm_color):
    return tuple(map(lambda a: int(a*255), norm_color))


def normalize_vector(v):
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return v[0]/length, v[1]/length, v[2]/length


def cross_product(a, b):
    cx = a[1]*b[2]-a[2]*b[1]
    cy = a[2]*b[0]-a[0]*b[2]
    cz = a[0]*b[1]-a[1]*b[0]
    return cx, cy, cz


def vector_bn_points(p1, p2):
    return p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]


def dot_product(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def subtract(a, b):
    return a[0]-b[0], a[1]-b[1], a[2]-b[2]


def add(a, b):
    return a[0]+b[0], a[1]+b[1], a[2]+b[2]


if __name__ == "__main__":
    inputFile = open(sys.argv[1], "r")
    firstLine = inputFile.readline().split()
    width = int(firstLine[1])
    height = int(firstLine[2])
    outputFileName = firstLine[3]

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    putpixel = img.im.putpixel
    eye = (0, 0, 0)
    forward = (0, 0, -1)
    right = (1, 0, 0)
    up = (0, 1, 0)

    sunlights = []
    bulbs = []

    spheres = []
    planes = []

    for line in inputFile:
        lineArray = line.split()
        if len(lineArray) == 0:
            continue

        # View port
        if lineArray[0] == "eye":
            eye = map(lambda c: float(c), lineArray[1:])
        if lineArray[0] == "forward":
            forward = map(lambda c: float(c), lineArray[1:])
            right = normalize_vector(cross_product(forward, up))
            up = normalize_vector(cross_product(right, forward))
        if lineArray[0] == "up":
            right = normalize_vector(cross_product(forward, map(lambda c: float(c), lineArray[1:])))
            up = normalize_vector(cross_product(right, forward))

        # Lights
        if lineArray[0] == "sun":
            dir = map(lambda c: float(c), lineArray[1:4])
            clr = tuple(map(lambda c: float(c), lineArray[4:7]))
            sunlights.append((dir, clr))
        if lineArray[0] == "bulb":
            pt = map(lambda c: float(c), lineArray[1:4])
            clr = tuple(map(lambda c: float(c), lineArray[4:7]))
            bulbs.append((pt, clr))

        # Objects
        if lineArray[0] == "sphere":
            sphere_center = tuple(map(lambda k: float(k), lineArray[1:4]))
            sphere_radius = float(lineArray[4])
            sphere_color = tuple(map(lambda k: float(k), lineArray[5:8]))
            spheres.append(Sphere(sphere_center, sphere_radius, sphere_color))
        if lineArray[0] == "plane":
            plane_vertices = tuple(map(lambda k: float(k), lineArray[1:5]))
            plane_color = tuple(map(lambda k: float(k), lineArray[5:8]))
            planes.append(Plane(plane_vertices, plane_color))
    rays_from_eye()
    img.save(outputFileName)