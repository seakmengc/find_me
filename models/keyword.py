from neomodel import StructuredNode, StringProperty, RelationshipTo


class Keyword(StructuredNode):
    keyword = StringProperty(unique_index=True)

    docs = RelationshipTo('CrawledUrl', 'IN')