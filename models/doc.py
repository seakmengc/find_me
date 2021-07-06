from neomodel import StringProperty, StructuredNode, BooleanProperty,RelationshipTo, StructuredRel
from neomodel.properties import IntegerProperty


class RefRelationship(StructuredRel):
    pass

class Doc(StructuredNode):
    url = StringProperty(required=True, unique_index=True)
    title = StringProperty()
    description = StringProperty()
    # ref = IntegerProperty(default=0)
    stemmed = BooleanProperty(default=False)

    ref_docs = RelationshipTo('Doc', 'REF', model=RefRelationship)

    @staticmethod
    def get_havent_stemmed():
        return Doc.nodes.first_or_none(stemmed__exact=False, title__isnull=False, description__isnull=False)
