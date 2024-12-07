import os
import subprocess

log_filename = 'log.txt'

def log_append(data):
    #test_string = "\ntest"
    next_line_data = "\n" + data
    log_filename = 'log.txt'
    try:
        with open(log_filename, 'a') as log_file:
            log_file.write(next_line_data)
            print("Activity logged to", os.path.abspath(log_filename))
    except:
        print("Something went wrong with logging")

log_append("Test")
cmd = "bat " + log_filename
output = subprocess.run(["bat", log_filename], capture_output=True)
#print(output)
