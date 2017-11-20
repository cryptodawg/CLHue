from HueInteract import HueInteract
import cmd
from pprint import pprint

class clHue(cmd.Cmd):
	intro = 'Welcome to clHue!'
	prompt = 'hue> ' # TODO: Change this to the bridge name

	def __init__(self):
		super(clHue, self).__init__()
		self.api = HueInteract()

	# Exit the program
	# arg: None
	def do_exit(self, arg):
		print("Bye!")
		exit()

	def do_get(self, arg):
		pprint(self.api.get(arg))

	def do_toggle(self, arg):
		pprint(self.api.toggle(arg))

	def do_on(self, arg):
		pprint(self.api.power(arg, True))

	def do_off(self, arg):
		pprint(self.api.power(arg, False))

if __name__ == '__main__':
	clHue().cmdloop()
