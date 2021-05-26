from neomodel import StructuredNode, StringProperty, RelationshipTo, StructuredRel, IntegerProperty
from models.doc import Doc



class KeywordRelationship(StructuredRel):
    freq = IntegerProperty(required=True)


class Keyword(StructuredNode):
    keyword = StringProperty(unique_index=True)

    docs = RelationshipTo('Doc', 'IN', model=KeywordRelationship)

