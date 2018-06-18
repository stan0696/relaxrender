import  numpy as np
from relaxrender.points import Vector,Point3D,Point,Points
from relaxrender.raycasting import SimpleReverseRayCasting
from .math import dist, sphere_sampling, ray_in_triangle
from relaxrender.example_meshs import CenterSquareLight
from relaxrender.mesh import Mesh
from .triangle import Triangles, Triangle
__all__ = ['importer_sample']


class importer_sample(SimpleReverseRayCasting):
    def __init__(self, context):
        super().__init__(context)

    def cast_ray(self, start_vector, ray_history, mesh, power):
        p3d = start_vector.start
        nearest_dist = None
        nearest_ipoint = None
        nearest_triangle = None
        for tri in range(mesh.triangles.size()):
            result_ipoint = ray_in_triangle(start_vector, mesh.triangles[tri])
            if result_ipoint is not None:
                ppdist = dist(p3d, result_ipoint)
                if nearest_dist is None or ppdist < nearest_dist:
                    nearest_dist = ppdist
                    nearest_triangle = tri
                    nearest_ipoint = result_ipoint

        ret_power = mesh.textures[tri].damping_rate() * power

        if nearest_dist is None:
            return None, 0
        else:
            ray_history.append((p3d, nearest_ipoint, nearest_triangle))
            return self.randiance(mesh.triangles[tri], ret_power,ray_history)





    def  randiance(self, triangle,ret_power,ray_history):
        vnorm = triangle.norm.end.data - triangle.norm.start.data
        vector2 = triangle.p1.data - triangle.p2.data
        np.cross(vnorm, vector2)
        random1 = np.random.random()
        random2 = np.random.random()

        NewRay = np.cos(2 * np.pi * random1) * np.sqrt(random1) * vector2 + \
             np.sin(2 * np.pi * random2) * np.sqrt(random2) * np.cross(vnorm, vector2) + \
             np.sqrt(1 - random2) * vnorm
        x, y, z = sphere_sampling(1)
        newray=Vector(NewRay,
                      Point3D(NewRay.data[0] + x,
                              NewRay.data[1] + y,
                              NewRay.data[2] + z, ))
        for i in range(len(ray_history)):
            if np.abs(np.dot(NewRay, NewRay)) > 1 - 1e-6:
                ret_power=ret_power+1
        return newray,ret_power

