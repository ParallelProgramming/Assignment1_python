class gap_struct:

	def __init__(self,p1,p2):
		self._p1 = p1
		self._p2 = p2
		self._gap = p2-p1

	def getP1(self):
		return self._p1

	def getP2(self):
		return self._p2

	def getGap(self):
		return self._gap

	def __eq__(self,gap_b):
		return self._gap == gap_b.getGap()

	def __lt__(self,gap_b):
		return self._gap < gap_b.getGap()

	def __le__(self,gap_b):
		return self._gap <= gap_b.getGap()

	def __str__(self):
		return "Gap {} for numbers {} and {}".format(self._gap,self._p1,self._p2)
