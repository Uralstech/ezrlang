import ezr
from sys import argv

print(f'ezrShell v{ezr.VERSION} (09-09-2022) - Ctrl+C to exit')

first_command = None
if len(argv) > 1:
	path = argv[1].replace('\\', '//')
	first_command = f'RUN(\'{path}\')'

while True:
	try:
		if first_command == None:
			input_ = input('>>>')
			if input_.strip() == '': continue
		else:
			print(f'>>>{first_command}')
			input_ = first_command
			first_command = None

		result, error = ezr.run('__main__', input_)

		if error: print(error.as_string())
		elif result:
			if len(result.elements) == 1: print(repr(result.elements[0]))
			else: print(repr(result))
	except KeyboardInterrupt: break
	except EOFError: break