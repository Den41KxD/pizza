import random
import string
from pathlib import Path


def generate_random_string(length: int = 4):
	letters = string.ascii_letters
	random_string = ''.join(random.choice(letters) for _ in range(length))
	return random_string


def convert_to_webp(source: Path, size: tuple = None):
	from PIL import Image
	"""Convert image to WebP.

	Args:
		source (pathlib.Path): Path to source image

	Returns:
		pathlib.Path: path to new image
	"""
	destination = source.with_suffix(".webp")
	new_file_path = destination.with_stem(destination.stem[0:70]+generate_random_string())
	image = Image.open(source)
	if size:
		image = image.resize(size=size)
	image.save(new_file_path, format="webp", quality=90)  # Convert image to webp

	return str(new_file_path).split('media')[-1]
