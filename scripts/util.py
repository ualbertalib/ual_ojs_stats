import re
import logging
import sys
import os

#
# correct the usage of the program
#
def usage(program):
    # Define the expected usage format of the script
    USAGE_FORMAT = f"python3 {program} <journal_file> <start_date> <end_date> <iStart> <iEnd>"
    EXPECTED_ARG_COUNT = 6 # Script name + 5 arguments = 6 total elements
    
    # Define the full, pre-formatted usage message
    USAGE_MESSAGE = f"""
    -------------------------------------------------------------------
    Error: the usage of the program is in a wrong format
    Expected format: {USAGE_FORMAT}
    
    Arguments:
      <journal_file>: Path to the journal CSV file (e.g., journal.csv)
      <start_date>:   Starting date for the range (YYYY-MM-DD)
      <end_date>:     Ending date for the range (YYYY-MM-DD)
      <iStart>:       Starting index for processing (integer)
      <iEnd>:         Ending index for processing (integer)
    
    Example:
      python3 {program} journals.csv 2024-01-01 2024-03-31 0 100
    -------------------------------------------------------------------"""

    logging.error(USAGE_MESSAGE)

def validate_args(args):

    program=args[0]

    if len(args) != 6:
        usage(program)
        sys.exit(1)

    if not os.path.exists(args[1]):
        logging.error("The input file doesn't exist")
        sys.exit(2)

    if not validate_date(args[2]):
        logging.error("The start date is in the wrong format")
        usage(program)
        sys.exit(3)

    if not validate_date(args[3]):
        logging.error("The end date is in the wrong format")
        usage(program)
        sys.exit(4)

    try:
        i_start = int(sys.argv[4])
        i_end = int(sys.argv[5])
    except ValueError:
        # This handles cases where arguments are not valid integers (e.g., "ten" or "1.5")
        logging.error("\nError: iStart and iEnd must be valid integers.")
        sys.exit(5)

    # Validation Check 1: Ensure iStart is not greater than iEnd (logical error)
    if i_start > i_end:
        logging.error(f"\nError: Starting index ({i_start}) cannot be greater than ending index ({i_end}).")
        sys.exit(5)

    # Validation Check 2: Ensure indices are not negative
    if i_start < 0 or i_end < 0:
        logging.error("\nError: Indices iStart and iEnd must be non-negative integers.")
        sys.exit(5)

    return True 
#
# the title can be in English, French, Italian or German etc.
#
def get_item_title(item):
    if item["publication"]["fullTitle"]["en_US"].strip() != "":
        title=item["publication"]["fullTitle"]["en_US"]
    elif item["publication"]["fullTitle"]["fr_CA"].strip() != "":
        title=item["publication"]["fullTitle"]["fr_CA"]
    elif item["publication"]["fullTitle"]["it_IT"].strip() != "":
         title=item["publication"]["fullTitle"]["it_IT"]
    elif item["publication"]["fullTitle"]["de_DE"].strip() != "":
         title=item["publication"]["fullTitle"]["de_DE"]
    else:
         title=""

    return title


#
# validate the date making sure it conforms to YYYY-MM-DD
#
def validate_date(date_str:str):
     
    pattern = r"\d{4}-\d{2}-\d{2}"
    if date_str is None or len(date_str) != 10:
        return False

    match = re.match(pattern, date_str)
    if match:
        return True
    
    return False 

