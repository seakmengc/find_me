from neomodel import StringProperty, StructuredNode, BooleanProperty


class Doc(StructuredNode):
    url = StringProperty(required=True, unique_index=True)
    title = StringProperty()
    description = StringProperty()
    stemmed = BooleanProperty(default=False)