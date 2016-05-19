class Person():

	""" Acts as object for person
	Holds the name and gender for a person
	Initialize with the name of the person and gender which is optional
	implements the methods for set the value of gender

	subclasses:
	Staff
	Fellow

	instance Variables:
	name - name of the person
	gender - the sex of the person
	room_name - name of the room allocated to person
	allocation - Status of allocation

	methods:
	get_name - return the name of person
	get_gender - return the sex of person
	set_gender - use to set the value of gender variable
	is_allocated - check if person is allocated or not
	set_allocation - use to set the person allocated room
	get_allocation - returns the name of the room allocated to person
	get_id - create Id for person with name
	"""

	def __init__(self, name, gender=None):
		"""
		Initialize the object, setting the name and gender
		defualt gender is none if not provided

		"""
		self.name = name
		self.gender = gender
		self.room_name = {}

	def get_name(self):
		""" return the name of person """
		return self.name
	def get_gender(self):
		""" returns the sex of person """
		return self.gender
	def set_gender(self, gender):
		""" set person gender
		arguments:
		gender - the sex of person, M or F
		"""
		self.gender = gender
	def is_allocated(self, room_type):
		""" checks if person is allocated
		returns true if so and False otherwise
		"""
		return room_type in self.room_name

	def set_allocation(self, room_type, room_name):
		""" set the name of room allocated to person
		and set the allocation status to false
		arguments:
		room_name - name of room in strings
		"""
		self.room_name[room_type] = room_name
		return 1

	def get_allocation(self, room_type):
		""" returns the name of room allocated to person """
		if self.is_allocated(room_type):
			return self.room_name[room_type]
		else:
			return 9

	def get_id(self):
		""" Create id for each person
		by striping all the whitespace and change to lowercase
		return id
		"""
		name_strip = self.name.replace(" ", "")
		return name_strip.lower()
