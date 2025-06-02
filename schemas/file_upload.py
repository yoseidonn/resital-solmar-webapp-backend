from pydantic import BaseModel, validator
from typing import Optional
import base64

class FileUploadRequest(BaseModel):
    filename: str
    file_content: str  # base64 encoded file content
    
    @validator('filename')
    def validate_filename(cls, v):
        if not v.endswith(('.xlsx', '.xls')):
            raise ValueError('Only Excel files (.xlsx, .xls) are allowed')
        return v
    
    @validator('file_content')
    def validate_file_content(cls, v):
        try:
            # Try to decode base64 to validate it's valid base64
            base64.b64decode(v, validate=True)
        except Exception:
            raise ValueError('file_content must be valid base64 encoded data')
        return v

class FileUploadResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    records_created: int
    upload_successful: bool
    error: Optional[str] = None
    uploaded_at: str 