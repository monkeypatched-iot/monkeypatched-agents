from neomodel import (StructuredNode, StringProperty)
from src.utils.graph import connection
from src.dao.document.tag import DocumentTag
from src.dao.product.details import ProductDetails

class DocumentMetadata(StructuredNode):
    document_id = StringProperty()
    title = StringProperty()
    author = StringProperty()
    created_at = StringProperty()
    modified_at = StringProperty()
    file_type = StringProperty()
    document_url = StringProperty()
    status = StringProperty()
    contract_id = StringProperty()
    component_id = StringProperty()
    product_id = StringProperty()
    supplier_id = StringProperty()
    order_id = StringProperty()
    customer_id = StringProperty()

    product =  connection.create_relationship_to('ProductDetails','BELONGS_TO')
    tags =  connection.create_relationship_to('DocumentTag','DESCRIBED BY')
