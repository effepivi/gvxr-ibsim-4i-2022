from pathlib import Path
from typing import Tuple, cast
import numpy as np
import solid as scad
import os
from subprocess import run

class Phantom():
	geometry: scad.OpenSCADObject

class RandomSpheres(Phantom):
	"""Generates a phantom of randomly placed spheres in a jittered grid."""

	def __init__(
		self,
		spheres=10):

		# determine the size and and spacing of the circles around the box.
		spacing = 1.0 / np.ceil(np.sqrt(spheres))
		radius = spacing / 4

		# Create a grid for sphere locations
		_x = np.arange(0, 1, spacing) + spacing / 2
		x, y, = np.meshgrid(_x, _x)

		# Flatten
		x = np.ravel(x)
		y = np.ravel(y)

		# jutter by random amount
		jitters = radius * (np.random.rand(2, spheres) - 0.5) * 2

		# place the circles
		geo = scad.translate((x[0] + jitters[0, 0], y[0] + jitters[1, 0], 0))(scad.sphere(radius))
		for i in range(1, spheres):
			center = (x[i] + jitters[0, i], y[i] + jitters[1, i], 0)
			geo += scad.translate(center)(scad.sphere(radius))
		self.geometry = geo

def dogaPoints(n_sizes=8, size_ratio=0.5, n_shuffles=8) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
		# Seed a latin square, use integers to prevent rounding errors
		top_row = np.array(range(0, n_sizes), dtype=int)
		lsquare = np.empty([n_sizes, n_sizes], dtype=int)
		for i in range(0, n_sizes):
			lsquare[:, i] = np.roll(top_row, i)

		# Create model
		period = (np.arange(0, n_sizes) / n_sizes + 1 / (2 * n_sizes)) * 0.7
		radii = (1 - 1e-10) / (2 * n_sizes) * (size_ratio ** lsquare) * 0.7

		# Location scale
		x, y = np.meshgrid(period, period)
		x += 0.3 / 2
		y += 0.3 / 2

		return (radii, x, y)

class DogaSpheres(Phantom):
	def __init__(self, n_sizes=5, size_ratio=0.5, n_shuffles=5, res=20):
		radii, _x, _y = dogaPoints(n_sizes, size_ratio, n_shuffles)
		print(radii)
		geo = None
		for (k, x, y) in zip(radii.flatten(), _x.flatten(), _y.flatten()):
			if geo is None:
				geo = scad.translate((x, y, 0))(scad.sphere(k,segments=res))
			else:
				geo += scad.translate((x, y, 0))(scad.sphere(k,segments=res))

		assert geo

		self.radii = radii
		self.x = _x
		self.y = _y
		self.geometry = scad.translate((-0.5, -0.5, 0))(geo)

class RandomMatSpheres(DogaSpheres):
	def __init__(self, size=1, n_sizes=5, size_ratio=0.5, n_shuffles=5, res=20):
		radii, _x, _y = dogaPoints(n_sizes, size_ratio, n_shuffles)
		rads = np.unique(radii)

		spheres = []
		for i in range(0, rads.shape[0]):
			spheres.append(None)

		for (k, x, y) in zip(radii.flatten(), _x.flatten(), _y.flatten()):
			i = int(np.where(rads == k)[0])
			if spheres[i] is None:
				spheres[i] = scad.translate((x, y, 0))(scad.sphere(k,segments=res))
			else:
				spheres[i] += scad.translate((x, y, 0))(scad.sphere(k,segments=res))

		for i, sphere in enumerate(spheres):
			spheres[i] = scad.translate((-0.5, -0.5, 0))(sphere)

		self.spheres = spheres
		self.radii = radii
		self.x = _x
		self.y = _y

class DogaCircles(Phantom):
	def __init__(self, n_sizes=5, size_ratio=0.5, n_shuffles=5,res=20):
		radii, _x, _y = dogaPoints(n_sizes, size_ratio, n_shuffles)

		geo = None # ? Anyone know a way to create an empty scad object?
		for (k, x, y) in zip(radii.flatten(), _x.flatten(), _y.flatten()):
			if geo is None:
				geo = scad.translate((x, y, 0))(scad.linear_extrude(100)(scad.circle(k,segments=res)))
			else:
				geo += scad.translate((x, y, 0))(scad.linear_extrude(100)(scad.circle(k,segments=res)))

		assert geo

		self.radii = radii
		self.x = _x
		self.y = _y

		self.geometry = scad.translate((-0.5, -0.5, 0))(geo)

class SiemensStar(Phantom):
	def __init__(self, n_sectors=2, radius=0.5):
		# Number of total points
		n_points = 2 * n_sectors
		center = (0, 0)

		# Create even circular points
		points = []
		for t in np.linspace(0, 2 * np.pi, n_points, endpoint=False):
			x = radius * np.cos(t) + center[0]
			y = radius * np.sin(t) + center[1]
			points.append((x, y))


		# Extrude first polygon
		point = (points[2 * 0], points[2 * 0 + 1], center)
		geo = scad.linear_extrude(100)(scad.polygon(point))

		# Create n-1 sector extruded polygons
		for i in range(1, n_sectors):
			point = (points[2 * i], points[2 * i + 1], center)
			geo += scad.linear_extrude(100)(scad.polygon(point))

		# Translate model to ensure it cuts the Z axis
		geo = scad.translate((0,0,-50))(geo)
		self.geometry = geo

def plate(scale=1):
	return scad.cube([scale,scale,.1], center=True)

if __name__ == "__main__":

	outPath = Path("input_data/phantoms/")
	os.makedirs(outPath, exist_ok=True)
	os.makedirs(outPath / "spheres/", exist_ok=True)

	# Create a plate with doga holes cutout
	dogaPlate = plate() - DogaCircles().geometry
	dogaPlate = scad.scale((100,100,100))(dogaPlate)
	scad.scad_render_to_file(dogaPlate, outPath / "doga-plate.scad")

	# Create free-standing spheres in a doga formation
	dogaSpheres = DogaSpheres().geometry
	dogaSpheres = scad.scale((100,100,100))(dogaSpheres)
	scad.scad_render_to_file(dogaSpheres, outPath / "doga-spheres.scad")

	# Create free-standing spheres split by materials in a doga formation
	matSpheres = RandomMatSpheres()
	for i, spheres in enumerate(matSpheres.spheres):
		spheres = scad.scale((100,100,100))(spheres)
		scad.scad_render_to_file(spheres, outPath / f"spheres/spheres-{i}.scad")

	# Create a plate with a Siemens star cutout
	starPlate = plate() - SiemensStar(n_sectors=20,radius=0.4).geometry
	starPlate = scad.scale((100,100,100))(starPlate)
	scad.scad_render_to_file(starPlate, outPath / "star-plate.scad")

	# Create a free-standing siemens star
	star = plate() * SiemensStar(n_sectors=20,radius=0.4).geometry
	star = scad.scale((100,100,100))(star)
	scad.scad_render_to_file(star, outPath / "star.scad")

	# Create free-standing random spheres
	spheres = RandomSpheres().geometry
	spheres = scad.scale((100,100,100))(spheres)
	scad.scad_render_to_file(spheres, outPath / "spheres.scad")

	print("Scad files created!")

	# If openscad is installed, generate stl files
	files = [outPath / "doga-plate.scad", outPath / "doga-spheres.scad", outPath / "star-plate.scad", outPath / "star.scad", outPath / "spheres.scad"]
	files = [Path(x) for x in files]

	# try to call scad on first file
	try:
		for i in files:
			run(f"openscad -i {i} {i.with_suffix('.stl')}")
	except FileNotFoundError as e:
		print(f"! Failed to convert scad files to .stl: {e}")
		print("! You will need to use openscad to convert the files manually.")
