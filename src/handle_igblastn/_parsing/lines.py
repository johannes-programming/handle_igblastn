import simple_tsv as _tsv

class BaseLine:
	def __init__(self, string):
		string = str(string)
		self._string = self.format(string)
	def __str__(self):
		return self._string
	def __eq__(self, other):
		return str(self) == str(other)
	def __ne__(self, other):
		return not (self == other)
	def __hash__(self):
		return str(self).__hash__()
	@classmethod
	def format(cls, string):
		raise NotImplementedError
	
class EmptyLine(BaseLine):
	@classmethod
	def format(cls, string):
		if '\t' in string:
			raise ValueError
		if string.strip() == "":
			return ""
		else:
			raise ValueError
	def __len__(self):
		return 0

class CommentLine(BaseLine):
	@classmethod
	def format(cls, string):
		for x in string:
			if x == ' ':
				continue
			if x == '#':
				return string.rstrip()
			raise ValueError

class TabLine(BaseLine):
	@classmethod
	def format(cls, string):
		if '\t' not in string:
			raise ValueError
        items, = (x for x in _tsv.reader([line.strip()]))
        return '\t'.join(items)
    def __getitem__(self, key):
    	return self._string.split('\t')[key]
    def __len__(self):
    	return len(self._string.count('\t')) + 1

class TotalLine(BaseLine):
	@classmethod
	def _format(cls, string):
		k, v = string.split('=')
		k = k.strip()
		v = int(v.strip())
		return k, v
	@classmethod
	def format(cls, string):
		if not string.startswith("Total "):
			raise ValueError
		k, v = cls._format(string)
		return f"{k} = {v}"
	def __getitem__(self, key):
		return self._format(self._string)[key]
	def __len__(self):
		return 2

def line(string):
	lineclasses = [EmptyLine, CommentLine, TabLine, TotalLine]
	lineobjects = list()
	for lineclass in lineclasses:
		try:
			lineobject = lineclass(string)
		except:
			continue
		else:
			lineobjects.append(lineobject)
	ans, = lineobjects
	return ans
