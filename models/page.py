from neomodel import StringProperty, StructuredNode


class Page(StructuredNode):
    url = StringProperty(required=True, unique_index=True)
    title = StringProperty()
    description = StringProperty()