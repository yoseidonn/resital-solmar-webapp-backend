# API Usage Examples

## File Upload with Base64 Content

The upload endpoints now accept file content as base64 encoded strings in JSON requests, automatically handling filename and upload date.

### Upload Resort Report File

```bash
POST /resort-report-files/
Content-Type: application/json

{
  "filename": "resort_report_2024.xlsx",
  "file_content": "UEsDBBQACgAIAA0A..."  // base64 encoded Excel file
}
```

**Response:**
```json
{
  "id": 123,
  "filename": "resort_report_2024.xlsx", 
  "file_path": "media/resort_report_files/resort_report_2024_20240602_b8f5e7c2-a123-4567-89ab-cdef01234567.xlsx",
  "records_created": 45,
  "upload_successful": true,
  "error": null,
  "uploaded_at": "2024-06-02T14:30:52.123456"
}
```

### Upload APIs Report File

```bash
POST /apis-report-files/
Content-Type: application/json

{
  "filename": "passenger_data_2024.xlsx",
  "file_content": "UEsDBBQACgAIAA0A..."  // base64 encoded Excel file  
}
```

**Response:**
```json
{
  "id": 124,
  "filename": "passenger_data_2024.xlsx",
  "file_path": "media/apis_report_files/passenger_data_2024_20240602_f7a9b3c1-d456-7890-abcd-ef0123456789.xlsx", 
  "records_created": 89,
  "upload_successful": true,
  "error": null,
  "uploaded_at": "2024-06-02T14:31:05.654321"
}
```

### Manual File Record Creation

If you need to create empty file records without uploading actual files:

```bash
POST /resort-report-files/manual?name=Manual Report&date=2024-06-02
```

```bash  
POST /apis-report-files/manual?name=Manual APIS&date=2024-06-02
```

## JavaScript Example

### Converting File to Base64

```javascript
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.split(',')[1]); // Remove data:type;base64, prefix
    reader.onerror = error => reject(error);
  });
}

// Usage
const fileInput = document.getElementById('file-input');
const file = fileInput.files[0];

fileToBase64(file).then(base64Content => {
  fetch('/resort-report-files/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      filename: file.name,
      file_content: base64Content
    })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Upload successful:', data);
    console.log(`Created ${data.records_created} database records`);
  });
});
```

### Python Example

```python
import base64
import requests
import uuid

# Read Excel file and encode to base64
with open('resort_report.xlsx', 'rb') as f:
    file_content = base64.b64encode(f.read()).decode('utf-8')

# Upload via API
response = requests.post('/resort-report-files/', json={
    'filename': 'resort_report.xlsx',
    'file_content': file_content
})

result = response.json()
print(f"Upload successful: {result['upload_successful']}")
print(f"Records created: {result['records_created']}")
```

## Key Benefits

1. **JSON-based**: Clean JSON API instead of multipart form data
2. **Automatic Naming**: Filename extracted from request, no manual input needed
3. **Automatic Dating**: Upload date set automatically to current timestamp  
4. **Guaranteed Uniqueness**: UUID + timestamp ensures no filename collisions
5. **Immediate Parsing**: Excel parsed and database records created in single request
6. **Rich Response**: Detailed response with upload status and record counts
7. **Validation**: Built-in validation for file types and base64 content

## Error Handling

### Invalid File Type
```json
{
  "detail": [
    {
      "loc": ["body", "filename"],
      "msg": "Only Excel files (.xlsx, .xls) are allowed",
      "type": "value_error"
    }
  ]
}
```

### Invalid Base64
```json
{
  "detail": [
    {
      "loc": ["body", "file_content"], 
      "msg": "file_content must be valid base64 encoded data",
      "type": "value_error"
    }
  ]
}
```

### Parsing Error (File uploads but Excel parsing fails)
```json
{
  "id": 125,
  "filename": "corrupted_file.xlsx",
  "file_path": "media/resort_report_files/corrupted_file_20240602_a1b2c3d4-e5f6-7890-abcd-ef0123456789.xlsx",
  "records_created": 0,
  "upload_successful": false, 
  "error": "Failed to parse Excel: Worksheet index out of range",
  "uploaded_at": "2024-06-02T14:32:00.789012"
}
``` 