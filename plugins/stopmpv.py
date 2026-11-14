import sonutils
import subprocess

def run(*args):
	try:
		p = subprocess.run(["pgrep", "-x", "mpv"], capture_output=True, text=True).stdout.replace("\n","")
		if p!="":subprocess.run(["kill", p])
	except: print("err")