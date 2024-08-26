from d2rq_mapping.BaseMap import BaseMap

class PropertyBridge(BaseMap):
    def __init__(self, prefix, belongsToClassMap, property, mapping_name=None, refersToClassMap=None, joins=None, conditions=None, column=None, datatype=None, inverseOf=None):
        super().__init__(prefix=prefix)
        self.mapping_name = mapping_name
        self.belongsToClassMap = belongsToClassMap
        self.refersToClassMap = refersToClassMap
        self.joins = joins
        self.property = property
        self.conditions = conditions
        self.column = column
        self.datatype = datatype
        self.inverseOf = inverseOf

    def get_d2rq_mapping(self):
        return self._get_jinja_template().render(
                prefix = self.prefix,
                mapping_name = self.mapping_name,
                property=self.property,
                belongs_to_class_map=self.belongsToClassMap,
                refers_to_class_map=self.refersToClassMap,
                joins=self.joins,
                conditions=self.conditions,
                column=self.column,
                datatype=self.datatype,
                inverse_of=self.inverseOf
            )
    
    def _get_jinja_template(self):
        return self.get_jinja_env().get_template('propertybridge.j2')
    
print(PropertyBridge("cmt", "PropertyBridge", "ClassMap", mapping_name="djawlkdjaw", joins=["ClassMap", "adwaw"], refersToClassMap="Refer", conditions=["ClassMap"], column="ClassMap", datatype="ClassMap",inverseOf="ClassMap2").get_d2rq_mapping())