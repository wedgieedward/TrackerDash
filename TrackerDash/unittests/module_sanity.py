"""
Sanity Test for trackerdash module
"""
import unittest


class TrackerSanity(unittest.TestCase):
	"""
	Sanity Test to ensure package can run after fresh install
	"""
	def test_imports(self):
		"""
		tests that we can import all the neccisary libraries
		this should never fail because setuptools is awesome
		"""
		try:
			import klein
			import twisted
			self.assertTrue(True)
		except ImportError as err:
			self.assertTrue(False,
				"Could not import dependency: %r" % err)


if __name__ == '__main__':
	unittest.main()