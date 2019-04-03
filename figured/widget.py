

import plotly.graph_objs as go


class FigureWidget(go.FigureWidget):
	"""
	FigureWidget with optional metadata.
	"""

	def __init__(self, *args, metadata=None, **kwargs):
		super().__init__(*args, **kwargs)
		self._metadata = metadata if metadata is not None else {}

	@property
	def metadata(self):
		return self._metadata

	@metadata.setter
	def metadata(self, x):
		self._metadata = x

