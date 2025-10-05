import subprocess
import sys
import os

venv_python = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")

subprocess.run([venv_python, "fetch_multi_news_fixed.py"], check=True)
subprocess.run([venv_python, "generate_signals.py"], check=True)
