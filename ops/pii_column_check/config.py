import re
import logging
import yaml
from environment_variables import pii_column_list,pii_datatype_list,mysql_reserved_word_list

class Config:

    COMMAND_TYPE = ['create']
    KEYWORD = ['table']

    PII_COLUMNS = yaml.load(open(pii_column_list), Loader=yaml.FullLoader).split(' ')
    PII_DATATYPE = yaml.load(open(pii_datatype_list), Loader=yaml.FullLoader).split(' ')
    MYSQL_RESERVED_WORDS = yaml.load(open(mysql_reserved_word_list), Loader=yaml.FullLoader).split(' ')

    def __init__(self):
        pass

    def remove_spaces_with_space(self,string):
        result =  ' '.join(string.split())
        return result
    
    def remove_newline_tab(self,string):
        result = re.sub(r"[\n\t]*", "", self.remove_spaces_with_space(str(string)))
        result = self.remove_backtick(result)
        result = ' '.join(result.split()).lower()
        return result.strip()

    def remove_backtick(self,string):
        return string.replace('`','')

    def remove_parenthesis(self,string):
        result = string.replace('(','').replace(')','')
        return result

    def has_parenthesis(self,string):
        return True if '(' in string and ')' in string else False

    def like_operation(self,sequence,word):
        filtered_list = list(filter(lambda item: item in word,sequence))
        if len(filtered_list)>0:
            return True
        return False

    def list_has_word(self,sequence,word):
        filtered_list = list(filter(lambda item: word in item,sequence))
        if len(filtered_list)>0:
            return True
        return False
    
    def set_logging_config(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    def get_text_between(self,start_char,end_char,text):
        return text[text.find(start_char)+len(start_char):text.rfind(end_char)]