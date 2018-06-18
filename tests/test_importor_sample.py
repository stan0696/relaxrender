import unittest
import numpy as np
import relaxrender.points as rp
import relaxrender.color as color
import relaxrender.mesh as mesh
import relaxrender.example_scene as example
import relaxrender.raycasting as raycasting
import relaxrender.context as ctx
import relaxrender.screenwriter as sw
import relaxrender.importer_sample as ims


class TestImportorSample(unittest.TestCase):

    def test_importor_sample(self):
        scene = example.cornell_box

        render = ims.importer_sample(ctx.Context())
        input_xy, output_color = render.drive_raycasting(scene)


        writer = sw.NormalizedWriter(ctx.Context())
        writer.write(input_xy, output_color, 'output_test1.jpg')