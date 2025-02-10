from neomodel import (StructuredNode, StringProperty)

class DocumentTag(StructuredNode):
    """Tag model"""
    name = StringProperty(unique_index=True)