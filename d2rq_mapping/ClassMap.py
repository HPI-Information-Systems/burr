from d2rq_mapping import BaseMap

class ClassMap(BaseMap):
    def __init__(self, prefix, class_name, mapping_name=None, uri_pattern=None, uri_column=None, translate_with=None, additional_property=None, condition=None, datastorage="database"):
        assert (uri_pattern is not None or uri_column is not None) and (uri_pattern is None and uri_column is not None or uri_pattern is not None and uri_column is None), "Either uriPattern or uriColumn must be provided"
        super().__init__(prefix, datastorage)
        self.class_name = class_name
        self.mapping_name = mapping_name
        self.uri_pattern = uri_pattern
        self.uri_column = uri_column
        self.translate_with = translate_with
        self.additional_property = additional_property
        self.condition = condition

    def get_d2rq_mapping(self):
        return self._get_jinja_template.render(
                class_name=self.class_name,
                mapping_name = self.mapping_name,
                uri_pattern=self.uri_pattern,
                uri_column=self.uri_column,
                translate_with=self.translate_with,
                additional_property=self.additional_property,
                condition=self.condition,
                datastorage=self.datastorage,
            )
    
    def _get_jinja_template(self):
        env = self.get_jinja_env()
        return env.get_template('classmap.j2')


ClassMap("http://example.org/", "http://example.org/Class", "Class", "ClassMap", uri_pattern="DWKDW").get_d2rq_mapping()