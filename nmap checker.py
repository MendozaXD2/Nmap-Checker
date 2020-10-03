import colorama, socket, struct, sys, re

from colorama import Fore, Style

colorama.init()

banner = f'''{Style.BRIGHT}
{Fore.WHITE}                          _           _           
{Fore.WHITE} ___ _____ ___ ___    ___{Fore.BLACK}| |{Fore.WHITE}_ ___ ___{Fore.BLACK}| |{Fore.WHITE}_ ___ ___ 
{Fore.BLACK}|   |     | .'| . |  |  _|   | -_|  _| '_| -_|  _|
{Fore.BLACK}|_|_|_|_|_|__,|  _|  |___|_|_|___|___|_,_|___|_|  
{Fore.BLACK}              |_|                                 
{Fore.WHITE}just a simple py program that check your nmap
{Fore.WHITE}scans output (for minecraft griefers)
{Fore.RED}by {Fore.YELLOW}@wejdene{Fore.RED} on telegram btw
'''

def check(ip, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		s.settimeout(1);
		s.connect((ip, int(port)));
		s.send(b'\xfe\x01');
		data = s.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
		s.close()
		motd = re.sub(r'§[a-zA-Z0-9]', '', data[2].strip().replace('  ', '').replace('  ', ''))
		version = re.sub(r'§[a-zA-Z0-9]', '', data[1].strip().replace('  ', '').replace('  ', ''))
		players = re.sub(r'§[a-zA-Z0-9]', '', f'{data[3]}/{data[4]}'.strip().replace('  ', '').replace('  ', ''))
		print(f'{Fore.BLACK}({Fore.WHITE}{ip}:{port}{Fore.BLACK})({Fore.WHITE}{players}{Fore.BLACK})({Fore.WHITE}{version}{Fore.BLACK})({Fore.WHITE}{motd}{Fore.BLACK})')
	except socket.timeout:
		print(f'{Fore.BLACK}({Fore.WHITE}{ip}:{port}{Fore.BLACK})({Fore.RED}timed out{Fore.BLACK})')
	except IndexError:
		print(f'{Fore.BLACK}({Fore.WHITE}{ip}:{port}{Fore.BLACK})({Fore.RED}can\'t parse json data{Fore.BLACK})')

print(banner)

try:
	with open(sys.argv[1]) as f:
		content = f.read()
		reports = content.split('Nmap scan report for ')
		for report in reports:
			ip = re.findall(r'\(([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\)', report)
			if ip != []:
				ip = ip[0]
				ports = re.findall(r'([0-9]+)/tcp', report)
				for port in ports:
					check(ip, port)
except IndexError:
	print(f'python {sys.argv[0]} <nmap file file>')
	sys.exit(0)
