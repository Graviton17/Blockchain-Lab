import hashlib

class MerkleTree:
	def __init__(self, data):
		self.data = data
		self.levels = []
		self.root = None
		self._build()

	def _hash_value(self, value):
		if isinstance(value, str):
			value = value.encode()
		elif not isinstance(value, bytes):
			value = str(value).encode()
		return hashlib.sha256(value).hexdigest()

	def _combine(self, left, right):
		return hashlib.sha256((left + right).encode()).hexdigest()

	def _build(self):
		if not self.data:
			self.root = None
			self.levels = []
			return

		level = [self._hash_value(item) for item in self.data]
		self.levels = [level]

		while len(level) > 1:
			if len(level) % 2 == 1:
				level = level + [level[-1]]
			parent = []
			for i in range(0, len(level), 2):
				parent.append(self._combine(level[i], level[i + 1]))
			level = parent
			self.levels.append(level)

		self.root = level[0]

	def get_root(self):
		return self.root

	def get_levels(self):
		return self.levels


def build_merkle_tree(data):
	return MerkleTree(data)


if __name__ == "__main__":
	count = int(input("Enter number of transactions: "))
	data = []
	for i in range(count):
		value = input(f"Enter transaction {i + 1}: ")
		data.append(value)
	tree = MerkleTree(data)
	print("Data:", data)
	print("Root:", tree.get_root())
	print("Levels:", tree.get_levels())
