import sqlparse as sa
from config import Config
import logging
from token_ops import TokenOps
import re

class ParseSql:

    def __init__(self):
        pass

    def parse_sql_statement(self,statement):
        statement = sa.format(self.strip_comments(statement), strip_comments=True, reindent=True, keyword_case='lower').strip()
        return sa.parse(statement)

    def strip_comments(self,text):
        comment_start = re.escape("#")
        comment_end = re.escape("\n")
        matches = re.search('%s(.*)%s' % (comment_start, comment_end), text)
        while matches is not None:
            start = matches.start()
            end = matches.end()
            text = text[:start]+text[end:]
            matches = re.search('%s(.*)%s' % (comment_start, comment_end), text)
        return text

    def has_create_statement(self,parsed_statement):
        if TokenOps().has_type_DDL_create(parsed_statement) or TokenOps().has_type_DDL_alter(parsed_statement):
            logging.info('Statment has create DDL')
            return True
        return False

    def pii_column_validate(self,tokens,comment_queries):
        try:
            for column_definition in tokens:
                column_name = column_definition.strip().split(' ')[0] 
                hasPiiColumn = Config().like_operation(Config().PII_COLUMNS,column_name)
                if hasPiiColumn:
                    logging.info(f'PII Column detected {str(column_name)}')
                    return self.pii_column_has_pii_comment(hasPiiColumn,column_definition,comment_queries) 
            return True
        except NameError:
            logging.info(f'Script Failed, Error: {str(NameError)}')
            return False
    
    def pii_datatype_validate(self,tokens,comment_queries):
        try:
            for column_definition in tokens:
                column_type = column_definition.strip().split(' ')[1] 
                hasPiiDatatype = Config().like_operation(Config().PII_DATATYPE,column_type)
                if hasPiiDatatype:
                    logging.info(f'PII Datatype detected {str(column_type)}')
                    return self.pii_column_has_pii_comment(hasPiiDatatype,column_definition,comment_queries)
            return True
        except NameError:
            logging.info(f'Script Failed, Error: {str(NameError)}')
            return False
    
    def validate_comment_attribute(self,tokens,comment_queries):
        try:
            if(len(comment_queries)>0):
                for column_definition in tokens:
                    col_name = '.'+column_definition.split(' ')[0]
                    return Config().list_has_word(comment_queries,col_name)
            else:
                for column_definition in tokens:
                    if " comment " not in column_definition:
                        logging.info(f'Comment attribute missing at {str(column_definition)}')
                        return False
            return True
        except NameError:
            logging.info(f'Script Failed, Error: {str(NameError)}')
            return False

    def pii_column_has_pii_comment(self,isPII,column_definition,comment_queries):
        col_name = '.'+column_definition.split(' ')[0]

        if(len(comment_queries)>0 and isPII):
            column_definition = list(filter(lambda query: col_name in query,comment_queries))[0]
        
        return isPII and "[pii]" in column_definition