import argparse
import logging
from pii_validation import PiiValidation
from config import Config
from sys import exit

    
def main(commit_id):
    commit_hash = commit_id
    if_build_pass = PiiValidation().execute_pii_test(commit_hash)
    if not if_build_pass: 
        raise Exception('Build Failed, PII columns detected!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit_id", help="Identifier is the instance name of the database.", required=True)
    args = parser.parse_args()
    Config().set_logging_config()
    main(args.commit_id)    