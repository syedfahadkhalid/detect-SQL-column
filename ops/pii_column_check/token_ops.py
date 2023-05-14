from config import Config
import logging

class TokenOps:

    def __init__(self):
        pass

    def get_tokens_from_create(self,tokens):
        config = Config()
        filtered_tokens = list(filter(lambda token: config.remove_newline_tab(token.ttype) == 'none' and config.has_parenthesis(config.remove_newline_tab(token)), tokens))
        mapped_tokens = list(map(lambda token: config.remove_newline_tab(config.get_text_between('(',')',token.value)), filtered_tokens))
        return self.get_cleaned_list(''.join(mapped_tokens).split(','))

    def get_cleaned_list(self,lst):
        cleaned_list = list(map(lambda token: token.strip(), lst))
        cleaned_list = list(filter(lambda token: token != '', cleaned_list))
        return cleaned_list

    def exclude_reserved_word_definition(self,lst):
        column_definition = list(filter(lambda token: token.split(' ')[0].upper() not in list(Config().MYSQL_RESERVED_WORDS),lst))
        return column_definition

    def get_tokens_from_alter(self,statement):
        config = Config()
        return [config.remove_newline_tab(config.get_text_between('add',';',statement.value))]

    def get_normalized_tokens(self,parsed_statements):
        tokens = []
        for statement in parsed_statements:
            cleaned_token = []
            if self.has_type_DDL_create(statement):
                cleaned_token = self.get_tokens_from_create(statement.tokens)
            elif self.has_type_DDL_alter(statement):
                cleaned_token = self.get_tokens_from_alter(statement)
            tokens.extend(cleaned_token) 
        return self.exclude_reserved_word_definition(tokens)

    def has_type_DDL_create(self,statement):
        return any(token.value == "create" for token in statement.tokens) and any(token.value == "table"  for token in statement.tokens)

    def has_type_DDL_alter(self,statement):
        return any(token.value == "alter" for token in statement.tokens) and any(token.value == "add" for token in statement.tokens)