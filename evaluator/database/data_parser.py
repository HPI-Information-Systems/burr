#das ding muss vom datacrawler erben. Damit ich dann mit verschiedenen dateiformaen arbeiten kann. Z.B. Exceldateien
class DataParser():
    def __init__(self) -> None:
        self.data = None
        pass

    def get_context(self, table_name):
        raise NotImplementedError

    def get_schema_element_type(self, el):
        raise NotImplementedError

    def load_data(self, credentials):
        #connect to db or load excel file
        raise NotImplementedError