from neomodel import StructuredNode, StringProperty, RelationshipTo, StructuredRel, IntegerProperty
from models.doc import Doc


class KeywordRelationship(StructuredRel):
    freq = IntegerProperty(required=True)


# INDEX
# CREATE CONSTRAINT ON (k:Keyword) ASSERT k.keyword IS UNIQUE
#
class Keyword(StructuredNode):
    keyword = StringProperty(unique_index=True)

    docs = RelationshipTo('Doc', 'IN', model=KeywordRelationship)
