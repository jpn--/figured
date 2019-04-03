
import pandas
from pandas.core.groupby.groupby import GroupBy
import numpy
from typing import Collection
import itertools

def get_name(i, from_first_item=False):
	"""
	Get a name from an object.

	Parameters
	----------
	i
		The object from which to get a name.
		If the object is a string, it is its own name.
		Otherwise, check if it has a name and use that.
	from_first_item : bool, default False
		If no name is available from the object and this
		is True, try to get a name from the first member
		of the object, assuming the object is a collection.
		If there is any problem (e.g., the object is not
		a collection, or the first item has no name)
		then silently ignore this.

	Returns
	-------
	str
		The name, or empty string if there is no name.
	"""
	if isinstance(i, str):
		return i
	if hasattr(i, 'name') and isinstance(i.name, str):
		return i.name
	if from_first_item:
		try:
			i0 = i[0]
		except:
			pass
		else:
			return get_name(i0)
	return ''

def any_names(I):
	"""
	Check if any member of a collection has a name.

	Parameters
	----------
	I : Iterable

	Returns
	-------
	bool
	"""
	for i in I:
		if get_name(i):
			return True
	return False

def same_names(I):
	"""
	Check if all members of a collection has the same name.

	Parameters
	----------
	I : Iterable

	Returns
	-------
	bool
	"""
	the_name = None
	for i in I:
		name = get_name(i)
		if the_name is None:
			the_name = name
		else:
			if the_name != name:
				return False
	return True


def preprocess_input(X, to_type=pandas.Series):
	"""
	Takes a general input X and returns turns it into a list of Series.

	Returns
	-------
	List[pandas.Series]
		The processed data
	List[str]
		Candidate labels
	"""
	if X is None:
		return [None, ]

	if isinstance(X, list) and all(isinstance(i, to_type) for i in X):
		return X

	if isinstance(X, to_type):
		return [X]

	if isinstance(X, numpy.ndarray):
		return [to_type(X)]

	if isinstance(X, Collection):
		if all(isinstance(i, Collection) for i in X):
			return [to_type(i) for i in X]

	if isinstance(X, GroupBy):
		return [to_type(i[1]) for i in X]

	raise NotImplementedError()


def zip_cycle(*args):
	maxlen = max(len(a) for a in args)
	return itertools.islice(zip(*(itertools.cycle(a) for a in args)), maxlen)

