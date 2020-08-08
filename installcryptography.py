import subprocess
import sys
import time
subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
time.wait(6000)
