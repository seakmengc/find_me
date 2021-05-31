from neomodel import StringProperty, StructuredNode, BooleanProperty


class Doc(StructuredNode):
    url = StringProperty(required=True, unique_index=True)
    title = StringProperty()
    description = StringProperty()
    stemmed = BooleanProperty(default=False)

    @staticmethod
    def get_havent_stemmed():
        return Doc.nodes.first_or_none(stemmed__exact=False, title__isnull=False, description__isnull=False)