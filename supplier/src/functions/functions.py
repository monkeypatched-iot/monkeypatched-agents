import json
from src.tools.nats import publish_event
from src.dao.quality import SupplierQuality
from src.dao.locations import SupplierLocation
from src.dao.details import SupplierDetails
from src.dao.finances import SupplierFinancials
from src.dao.capablities import SupplierCapabilities
from src.dao.certifications import SupplierCertifications
from src.utils.logger import logging
from  src.tools.requests import get


from dotenv import load_dotenv
import os

from src.utils.graph import connection

load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")

supplier_aggregate = {}

def GetSupplierDetails(supplier_id):
    if supplier_id != "supplier_id":

        print("getting the supplier details")

        response = get(f"{BASE_URL}/v1/supplier/details/{supplier_id}")

         # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        supplier_dict = json.loads(json_string)

        print(supplier_dict)

        supplier_aggregate["details"] = supplier_dict

        connection.add(SupplierDetails(**supplier_dict))

def GetSupplierLocations(supplier_id):
    if supplier_id != "supplier_id":

        print("getting the supplier locatons")

        response = get(f"{BASE_URL}/v1/supplier/{supplier_id}/locations/")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        supplier_locations_dict = json.loads(json_string)

        print(supplier_locations_dict)

        supplier_aggregate["locations"] = supplier_locations_dict

        connection.add(SupplierLocation(**supplier_locations_dict[0]))

def GetSupplierFinance(supplier_id):
    if supplier_id != "supplier_id":

        print('getting the supplier finance')

        response = get(f"{BASE_URL}/v1/supplier/financials/{supplier_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        supplier_finance_dict = json.loads(json_string)

        print(supplier_finance_dict)

        connection.add(SupplierFinancials(**supplier_finance_dict))

def GetSupplierCapabilities(supplier_id):
    if supplier_id != "supplier_id":

        print("getting the supplier capablities")

        response = get(f"{BASE_URL}/v1/supplier/capabilities/{supplier_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        supplier_capabilities_dict = json.loads(json_string)

        print(supplier_capabilities_dict)

        connection.add(SupplierCapabilities(**supplier_capabilities_dict))

def GetSupplierCertifications(supplier_id):
    if supplier_id != "supplier_id":

        print("getting the supplier certifications")

        response = get(f"{BASE_URL}/v1/supplier/certifications/{supplier_id}")
        
        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        supplier_certifications_dict = json.loads(json_string)

        print(supplier_certifications_dict)

        connection.add(SupplierCertifications(**supplier_certifications_dict))
       

def GetSupplierQuality(supplier_id):
    if supplier_id != "supplier_id":

        print("getting the suppler quality metrics")

        response = get(f"{BASE_URL}/v1/supplier/quality/{supplier_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        supplier_quality_dict = json.loads(json_string)

        print(supplier_quality_dict)

        connection.add(SupplierQuality(**supplier_quality_dict))

def GetSupplierDetailsFromGraph(supplier_id):
    if not supplier_id:  # Handles None, empty strings
        logging.warning("Invalid supplier_id provided")
        return None
    
    logging.info(f"Fetching supplier details for ID: {supplier_id}")
    try:
        supplier_details = SupplierDetails.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_details:
            logging.info(f"Supplier details found: {supplier_details}")
            return supplier_details
        logging.info(f"No supplier details found for supplier_id: {supplier_id}")
    except Exception as e:
        logging.error(f"Error fetching supplier details: {e}", exc_info=True)

    return None

def GetSupplierLocationsFromGraph(supplier_id):
    if not supplier_id:  # Handles None, empty strings
        logging.warning("Invalid supplier_id provided")
        return None
    
    logging.info(f"Fetching supplier locations for ID: {supplier_id}")
    try:
        supplier_locations = SupplierLocation.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_locations:
            logging.info(f"Supplier locations found: {supplier_locations}")
            return supplier_locations
        logging.info(f"No supplier locations found for supplier_id: {supplier_id}")
    except Exception as e:
        logging.error(f"Error fetching supplier locations: {e}", exc_info=True)

    return None



def GetSupplierFinanceFromGraph(supplier_id):
    if not supplier_id:  # Handles None, empty strings
        logging.warning("Invalid supplier_id provided")
        return None
    
    logging.info(f"Fetching supplier finance details for ID: {supplier_id}")
    try:
        supplier_finance = SupplierFinancials.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_finance:
            logging.info(f"Supplier finance details found: {supplier_finance}")
            return supplier_finance
        logging.info(f"No supplier finance details found for supplier_id: {supplier_id}")
    except Exception as e:
        logging.error(f"Error fetching supplier finance details: {e}", exc_info=True)

    return None

def GetSupplierCapabilitiesFromGraph(supplier_id):
    if not supplier_id:  # Handles None, empty strings
        logging.warning("Invalid supplier_id provided")
        return None
    
    logging.info(f"Fetching supplier capabilities for ID: {supplier_id}")
    try:
        supplier_capabilities = SupplierCapabilities.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_capabilities:
            logging.info(f"Supplier capabilities found: {supplier_capabilities}")
            return supplier_capabilities
        logging.info(f"No supplier capabilities found for supplier_id: {supplier_id}")
    except Exception as e:
        logging.error(f"Error fetching supplier capabilities: {e}", exc_info=True)

    return None

def GetSupplierCertificationsFromGraph(supplier_id):
    if not supplier_id:  # Handles None, empty strings
        logging.warning("Invalid supplier_id provided")
        return None
    
    logging.info(f"Fetching supplier certifications for ID: {supplier_id}")
    try:
        supplier_certifications = SupplierCertifications.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_certifications:
            logging.info(f"Supplier certifications found: {supplier_certifications}")
            return supplier_certifications
        logging.info(f"No supplier certifications found for supplier_id: {supplier_id}")
    except Exception as e:
        logging.error(f"Error fetching supplier certifications: {e}", exc_info=True)

    return None

def GetSupplierQualityFromGraph(supplier_id):
    if not supplier_id:  # Handles None, empty strings
        logging.warning("Invalid supplier_id provided")
        return None
    
    logging.info(f"Fetching supplier quality details for ID: {supplier_id}")
    try:
        supplier_quality = SupplierQuality.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_quality:
            logging.info(f"Supplier quality details found: {supplier_quality}")
            return supplier_quality
        logging.info(f"No supplier quality details found for supplier_id: {supplier_id}")
    except Exception as e:
        logging.error(f"Error fetching supplier quality details: {e}", exc_info=True)

    return None

def publish_supplier(supplier_aggregate: dict) -> None:
    """Publishes supplier data to Kafka."""
    try:
        if not isinstance(supplier_aggregate, dict):
            raise ValueError("supplier_aggregate must be a dictionary")

        # Ensure the supplier data is serializable
        supplier_json = {"supplier": supplier_aggregate}
        json.dumps(supplier_json)  # Validate serialization

        # Publish event to Kafka
        publish_event("supplier", supplier_json)

        print("Supplier data published successfully.")

    except (ValueError, TypeError, json.JSONDecodeError) as e:
        logging.error(f"Error publishing supplier data: {e}")
        raise  # Re-raise the error for better debugging

def AddSupplier(supplier_id):
    if supplier_id != "supplier_id":
        print("adding the supplier id")
        print({"supplier":supplier_aggregate})
        publish_supplier(supplier_aggregate)

        try:
            # Retrieve supplier details
            supplier = GetSupplierDetailsFromGraph(supplier_id)
            certifications = GetSupplierCertificationsFromGraph(supplier_id)
            locations = GetSupplierLocationsFromGraph(supplier_id)
            finance = GetSupplierFinanceFromGraph(supplier_id)
            quality = GetSupplierQualityFromGraph(supplier_id)
            capabilities = GetSupplierCapabilitiesFromGraph(supplier_id)

            # Ensure the supplier exists before connecting various details
            if supplier:
                if certifications:
                    supplier.certifications.connect(certifications)
                if locations:
                    supplier.locations.connect(locations)
                if finance:
                    supplier.finance.connect(finance)
                if quality:
                    supplier.quality.connect(quality)
                if capabilities:
                    supplier.capabilities.connect(capabilities)

                logging.info(f"Supplier {supplier_id} added successfully.")
                return json.dumps({"message": "Supplier added successfully"})

            logging.error(f"Supplier {supplier_id} could not be added due to missing data.")
            return json.dumps({"error": "Supplier could not be added due to missing data"})
        
        except Exception as e:
            logging.error(f"Error adding supplier {supplier_id}: {e}", exc_info=True)
            return json.dumps({"error": f"Unexpected error: {str(e)}"})
