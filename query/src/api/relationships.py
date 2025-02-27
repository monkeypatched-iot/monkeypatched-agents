
relationships = """ 

     CustomerDetails
        HAS_A → CustomerMetadata
        HAS_A → CustomerOrderMetrics
        HAS_A → CustomerPaymentData
        HAS_MANY → OrderDetails

     OrderDetails
        HAS_A → OrderMetrics
        HAS_A → OrderPayment
        HAS_A → OrderShipping

   
"""
