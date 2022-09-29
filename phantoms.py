from pathlib import Path
from typing import Tuple
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

		colors = [2.0**j for j in range(0, spheres)]
		np.random.shuffle(colors)

		# generate grid
		_x = np.arange(0, 1, spacing) + spacing / 2
		px, py, = np.meshgrid(_x, _x)
		px = np.ravel(px)
		py = np.ravel(py)

		# calculate jitters
		jitters = 2 * radius * (np.random.rand(2, spheres) - 0.5)

		# place the circles
		geo = scad.translate((px[0] + jitters[0, 0], py[0] + jitters[1, 0], 0))(scad.sphere(radius))
		for i in range(1, spheres):
			center = (px[i] + jitters[0, i], py[i] + jitters[1, i], 0)
			geo += scad.translate(center)(scad.sphere(radius))
		self.geometry = geo

def dogaPoints(n_sizes=5, size_ratio=0.5, n_shuffles=5) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
		n_sizes = int(n_sizes)
		if n_sizes <= 0:
			raise ValueError('There must be at least one size.')
		if size_ratio > 1 or size_ratio <= 0:
			raise ValueError('size_ratio should be <= 1 and > 0.')
		n_shuffles = int(n_shuffles)
		if n_shuffles < 0:
			raise ValueError('Cant shuffle a negative number of times')

		# Seed a latin square, use integers to prevent rounding errors
		top_row = np.array(range(0, n_sizes), dtype=int)
		rowsum = np.sum(top_row)
		lsquare = np.empty([n_sizes, n_sizes], dtype=int)
		for i in range(0, n_sizes):
			lsquare[:, i] = np.roll(top_row, i)

		# Choose a row or column shuffle sequence
		sequence = np.random.randint(0, 2, n_shuffles)

		# Shuffle the square
		for dim in sequence:
			lsquare = np.rollaxis(lsquare, dim, 0)
			np.random.shuffle(lsquare)

		# Assert that it is still a latin square.
		for i in range(0, n_sizes):
			assert np.sum(lsquare[:, i]) == rowsum, \
				"Column {0} is {1} and should be {2}".format(i, np.sum(
														lsquare[:, i]), rowsum)
			assert np.sum(lsquare[i, :]) == rowsum, \
				"Column {0} is {1} and should be {2}".format(i, np.sum(
														lsquare[i, :]), rowsum)

		# Draw it
		period = (np.arange(0, n_sizes) / n_sizes + 1 / (2 * n_sizes)) * 0.7
		_x, _y = np.meshgrid(period, period)
		radii = (1 - 1e-10) / (2 * n_sizes) * size_ratio**lsquare * 0.7
		_x += (1 - 0.7) / 2
		_y += (1 - 0.7) / 2

		return (radii, _x, _y)

class DogaSpheres(Phantom):
	def __init__(self, n_sizes=5, size_ratio=0.5, n_shuffles=5, res=20):
		radii, _x, _y = dogaPoints(n_sizes, size_ratio, n_shuffles)

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

class DogaCircles(Phantom):
	def __init__(self, n_sizes=5, size_ratio=0.5, n_shuffles=5,res=20):
		radii, _x, _y = dogaPoints(n_sizes, size_ratio, n_shuffles)

		geo = None
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
		super(SiemensStar, self).__init__()
		if n_sectors < 2:
			raise ValueError("A Siemens star must have > 1 sector.")
		if radius <= 0:
			raise ValueError("radius must be greater than zero.")

		n_points = 2 * n_sectors
		self.ratio = n_sectors / (2 * np.pi * radius)
		self.n_sectors = n_sectors

		center = (0, 0)
		# generate an even number of points around the unit circle
		points = []
		for t in np.linspace(0, 2 * np.pi, n_points, endpoint=False):
			x = radius * np.cos(t) + center[0]
			y = radius * np.sin(t) + center[1]
			points.append((x, y))


		point = (points[2 * 0], points[2 * 0 + 1], center)
		geo = scad.linear_extrude(100)(scad.polygon(point))
		# connect pairs of points to the center to make triangles
		for i in range(1, n_sectors):
			point = (points[2 * i], points[2 * i + 1], center)
			geo += scad.linear_extrude(100)(scad.polygon(point))

		geo = scad.translate((0,0,-50))(geo)
		self.geometry = geo

	def get_frequency(self, radius):
		"""Return the spatial frequency at the given radius.

		.. versionadded:: 0.6
		"""
		return self.n_sectors / (2 * np.pi * radius)

	def get_radius(self, frequency):
		"""Return the radius which provides the given frequency.

		.. versionadded:: 0.6
		"""
		return self.n_sectors / (2 * np.pi * frequency)

def plate(scale=1):
	return scad.cube([scale,scale,.1], center=True)

if __name__ == "__main__":

	outPath = Path("input_data/phantoms/")
	os.makedirs(outPath, exist_ok=True)

	# Create a plate with doga holes cutout
	dogaPlate = plate() - DogaCircles().geometry
	dogaPlate = scad.scale((100,100,100))(dogaPlate)
	scad.scad_render_to_file(dogaPlate, outPath / "doga-plate.scad")

	# Create free-standing spheres in a doga formation
	dogaSpheres = DogaSpheres().geometry
	dogaSpheres = scad.scale((100,100,100))(dogaSpheres)
	scad.scad_render_to_file(dogaSpheres, outPath / "doga-spheres.scad")

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
		print(f"Failed to convert scad files to .stl: {e}")
		print("You will need to use openscad to convert the files manually.")
