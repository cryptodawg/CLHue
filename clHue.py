from HueInteract import HueInteract
from LightGroup import LightGroup
import cmd
from pprint import pprint

class clHue(cmd.Cmd):
	""" A command-line interface for interacting with a Philips Hue bridge. """

	intro = 'Welcome to clHue!'

	def __init__(self):
		super(clHue, self).__init__()
		self.api = HueInteract()
		self.prompt = self.api.bridgeName() + '> '

	def do_exit(self, arg):
		""" Exit the program. """
		print("Bye!")
		exit()

	def do_get(self, arg):
		"""	Get an object from the bridge.  Doesn't return anything.

		Parameters:
			arg -- a string in the form of <lights/groups> <id>
		"""
		pprint(self.api.get(arg))

	def do_toggle(self, arg):
		"""	Toggle the power of an object. Doesn't return anything.

		Parameters:
			arg -- a string in the form of <lights/groups> <id>
		"""
		pprint(self.api.toggle(arg))

	def do_on(self, arg):
		"""	Power an object on. Doesn't return anything.

		Parameters:
			arg -- a string in the form of <lights/groups> <id>
		"""
		pprint(self.api.power(arg, True))

	def do_off(self, arg):
		"""	Power an object off. Doesn't return anything.

		Parameters:
			arg -- a string in the form of <lights/groups> <id>
		"""
		pprint(self.api.power(arg, False))

	def do_changestate(self, arg):
		"""	Change the state information of an object. Doesn't return anything.

		Parameters:
			arg -- a string in the form of <lights/groups> <id>
		"""
		newStateStr = input("Enter the new state: ")
		newState = dict() # Is there a way to just throw newStateStr into a dict without converting types?
		for i in newStateStr.split(','):
			state = i.split('=')
			stateParam = state[0].strip()
			stateValue = state[1].strip()
			if stateValue.isnumeric():
				stateValue = int(stateValue)
			elif stateValue == 'True':
				stateValue = True # bool(state[1]) always returns True, so we need to do this instead
			elif stateValue == 'False':
				stateValue = False # bool(state[1]) always returns True
			newState[stateParam] = stateValue
		pprint(self.api.putState(arg, newState))

	# TODO: Add arguments for brightness and saturation to this
	def do_rainbow(self, arg):
		"""	Cycles the object (arg) through all hues. Doesn't return anything.

		Parameters:
			arg -- a string in the form of <lights/groups> <id>
		"""
		pprint(self.api.rainbow(arg))

	def do_test(self, arg):
		""" Lets us test commands in HueInteract """
		group = LightGroup(self.api, 'all', 'Test1')
		group.remove(2)
		print(group)
		group.add(2)
		print(group)
		group.remove('blah')
		group.add('blah')

if __name__ == '__main__':
	clHue().cmdloop()
