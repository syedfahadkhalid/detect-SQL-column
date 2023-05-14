from pydriller import Repository
import logging
from parse_sql import ParseSql as ps
from token_ops import TokenOps
from config import Config

class PiiValidation:

    def __init__(self):
        pass

    def execute_pii_test(self,commit_hash):
        logging.info(f'Executing PII column detection process, commit ID: {str(commit_hash)}')
        for commit in Repository(path_to_repo=".", single=commit_hash).traverse_commits():
            for modified_file in commit.modified_files:
                return self.perform_pii_test(modified_file)
    
    def perform_pii_test(self,modification):
        logging.info(f'Executing PII test on Modification: {str(modification.filename)}')
        parsed_queries, tokens, comment_queries = self.get_modification_content(modification)
        
        if parsed_queries is not None and tokens is not None:
            for query in parsed_queries:
                if ps().has_create_statement(query):
                    rules = [
                        ps().validate_comment_attribute(tokens,comment_queries),
                        ps().pii_column_validate(tokens,comment_queries),
                        ps().pii_datatype_validate(tokens,comment_queries)
                        ]
                    if not all(rules):
                        logging.info(f'Build failed the PII test, file name: {str(modification.filename)}')
                        return False
        logging.info('Build passed the PII test')            
        return True

    def get_modification_content(self,modification):
        if modification.filename.endswith(".sql") and modification.change_type.name in ["ADD", "MODIFY"]:
            expansion_file_content = str(modification.source_code)
            parsed_queries = ps().parse_sql_statement(expansion_file_content)
            tokens = TokenOps().get_normalized_tokens(parsed_queries)

            #for postgres
            parsed_queries_cleaned = list(map(lambda query: Config().remove_spaces_with_space(Config().remove_newline_tab(query.value.lower())),parsed_queries ))
            comment_queries = list(filter(lambda query: query.split(' ')[0] == 'comment' ,parsed_queries_cleaned ))
            return parsed_queries,tokens,comment_queries

        return None,None,None