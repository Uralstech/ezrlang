import ezr
from sys import argv
from requests import get, ConnectionError

def check_version():
	try:
		ov_text = get('https://pastebin.com/raw/SCjpDBpD').text
		ov, cv = ov_text.split('.'), ezr.VERSION.split('.')
		for i, v in enumerate(cv):
			if ov[i] > v:
				if i == 0: print(f'UPDATE AVAILABLE: v{ov_text} [MAJOR UPDATE]'); return
				if i == 1: print(f'UPDATE AVAILABLE: v{ov_text} [semi-major update]'); return
				if i == 2: print(f'UPDATE AVAILABLE: v{ov_text} [minor update]'); return
	except ConnectionError as e: print('Warning: Could not check for latest ezr version')

def main():
	print(f'ezrShell v{ezr.VERSION} ({ezr.VERSION_DATE}) - Ctrl+C to exit')
	check_version()

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

if __name__ == '__main__':
	main()