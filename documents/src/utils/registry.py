

from src.functions.functions import SendDocumentUploadNotification, IndexDocument


function_registry = {
   "IndexDocument":IndexDocument,
   "SendDocumentUploadNotification":SendDocumentUploadNotification
}