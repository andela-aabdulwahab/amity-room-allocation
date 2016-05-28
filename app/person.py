import uuid

class Person():

	''' Acts as object for person
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

	methods:
		is_allocated - check if person is allocated or not
		get_id - create Id for person with name
	'''

	def __init__(self, name, gender):
		"""
		Initialize the object, setting the name and gender
		defualt gender is none if not provided

		"""
		self.name = name
		self.gender = gender
		self.room_name = {}
		self.identifier = self.generate_id()

	def is_allocated(self, room_type):
		""" checks if person is allocated
		Arguments:
		    room_type - the room type to check for
		returns:
		    True if the room type is specify in room_name

		"""
		return room_type in self.room_name

	def generate_id(self):
		''' Generate a unique Id for person using UUID4

		return
		   the first part of uuid4 generated

		'''
		#str(uuid.uuid4()).split('-')[0]
		uuid_generated = uuid.uuid4()
		uuid_to_string = str(uuid_generated)
		uuid_first_part = uuid_to_string.split('-')[0]
		return uuid_first_part