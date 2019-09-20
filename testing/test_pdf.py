import os

os.system('enscript -p output.ps log.log')
os.system('ps2pdf output.ps asrs_log.pdf')

