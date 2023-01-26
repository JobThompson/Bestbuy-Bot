from pprint import pprint
import logging
import datetime
from Classes.Config import instanceConfig
from ProgramState import programState

# TODO: Re-Write to allow for multiple log types to be written to the same file and rewrite the log file creation.

def write_to_log(level, info):
    """Outputs info string to the log file that is set upon initial script execution."""
    logging.info(f'{str(datetime.datetime.now())} : {level} : {info}')  # Writes time and date as well as the info string to log file.
    return

def create_logfile():
    """Creates a new Log file with a date Identifier. If there is an existing log file with that identifier,
    the function adds an iterative number to the end of the file name until it gets to a file name that doesn't' exist."""
    date = str(datetime.datetime.now().strftime("%m_%d_%Y")) # sets date to a variable
    logfile = (f'Log_{date}.log') # creates a new file name using date variable set above as the identifier
    multiple = 1
    while True:  # compares the last log file to the created file name
        try:
            open(f'{instanceConfig.log_directory}/{logfile}', "x") # creates a new file using the new log file name
            break
        except Exception as e:  # if the file name is the same, it adds an iterating number to the end
            pprint(e)
            logfile = (f'Log_{date}_{str(multiple)}.log')
            multiple += 1  # iterates the number at the end of the file
    logfile = (f'{instanceConfig.log_directory}/{logfile}') # sets logfile to the full filepath.
    logging.basicConfig(filename=logfile, level=logging.INFO) # sets the logging file as the newly created file.
    return logfile

def handle_exit():
    """This function handles the exit of the program. It writes a final log entry and closes the log file."""
    write_to_log('INFO', f'Total Number of Attempts: {str(programState.RefreshAttempts)}')
    write_to_log('INFO', 'Program Exited. Closing Log File.')
    logging.shutdown()
    exit(0)