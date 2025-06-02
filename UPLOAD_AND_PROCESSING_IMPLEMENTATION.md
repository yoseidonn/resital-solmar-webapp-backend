# File Upload and Database Record Creation Implementation

## Overview
This document outlines the implementation that ensures Excel file uploads create individual database records instead of working directly with Excel files. The upload and database record creation processes have been merged into unified endpoints.

## Changes Made

### 1. Unified File Upload Routes

#### Resort Report File Route (`routes/resort_report_file.py`)
- **Primary Endpoint**: `POST /` - Unified endpoint supporting both file upload and manual creation
- **File Upload Mode**: When `file` parameter is provided
  - Accepts Excel files (.xlsx, .xls)
  - Saves uploaded Excel file to `media/resort_report_files/`
  - Creates `ResortReportFile` record
  - Parses Excel and creates individual `ResortReport` records
  - Links each `ResortReport` to the `ResortReportFile` via `resort_report_file_id`
- **Manual Creation Mode**: When `name` and `date` parameters are provided
  - Creates empty `ResortReportFile` record without physical file
  - Useful for manual data entry scenarios
- **Legacy Support**: `POST /upload` endpoint maintained for backward compatibility

#### APIs Report File Route (`routes/apis_report_file.py`)
- **Primary Endpoint**: `POST /` - Unified endpoint supporting both file upload and manual creation
- **File Upload Mode**: When `file` parameter is provided
  - Accepts Excel files (.xlsx, .xls) 
  - Saves uploaded Excel file to `media/apis_report_files/`
  - Creates `APISReportFile` record
  - Parses Excel and creates individual `AdvancedPassengerInformation` records
  - Links each record to the `APISReportFile` via `apis_report_file_id`
- **Manual Creation Mode**: When `name` and `date` parameters are provided
  - Creates empty `APISReportFile` record without physical file
- **Legacy Support**: `POST /upload` endpoint maintained for backward compatibility

### 2. Schema Updates

#### Resort Report Schema (`schemas/resort_report.py`)
- Fixed field name: `resort_report_file` → `resort_report_file_id`

#### Advanced Passenger Information Schema (`schemas/advanced_passenger_information.py`)
- Fixed field name: `apis_report_file` → `apis_report_file_id`

### 3. Model Updates

#### APIs Report Output Model (`models/apis_report_output.py`)
- Added `user_name` field
- Added `individual_reservations` field for consistency

#### Caretaker Extras View Output Model (`models/caretaker_extras_view_output.py`)
- Added `user_name` field
- Added `file_path` field for consistency

### 4. Service Updates - All Use Database Records

#### APIs Report Output Service (`services/apis_report_output_service.py`)
- **✅ Database-First Approach**: `generate_apis_report_output()` queries `AdvancedPassengerInformation` records instead of parsing Excel
- **Proper Field Mapping**: Uses `_to_snake_case()` to map Excel headers to model attributes
- **Date Formatting**: Properly formats datetime and date fields for Excel output

#### Extras Filtered Reservation Output Service (`services/extras_filtered_reservation_output_service.py`)
- **✅ Database-First Approach**: `generate_extras_filtered_reservation_summary()` uses `get_reports_by_file()` to fetch `ResortReport` records from database
- **No Excel Parsing**: Works entirely with database models

#### Caretaker Extras View Output Service (`services/caretaker_extras_view_output_service.py`)
- **✅ Database-First Approach**: `generate_caretaker_extras_view_output()` uses `get_reports_by_file()` to fetch `ResortReport` records from database
- **No Excel Parsing**: Works entirely with database models

#### Services Import (`services/__init__.py`)
- Added `advanced_passenger_service` import

### 5. Database Migration
- Generated migration: `4_20250602115436_add_missing_fields_to_output_models.py`
- Applied migration successfully
- Added missing fields to output models

## Data Flow

### Unified File Upload Process
1. **Upload**: User uploads Excel file via `POST /` endpoint with `file` parameter
2. **File Storage**: File saved to appropriate media directory
3. **File Record**: Create file record in database
4. **Parse Excel**: Parse Excel row by row
5. **Create Records**: Create individual records (ResortReport or AdvancedPassengerInformation)
6. **Link Records**: Each record linked to file via foreign key
7. **Response**: Return file record with database ID

### Manual Creation Process (Alternative)
1. **Request**: User provides `name` and `date` parameters via `POST /`
2. **File Record**: Create empty file record in database
3. **Response**: Return file record for manual data entry

### Report Generation Process
1. **✅ Query Database**: All services query individual records (not Excel files)
2. **Filter Data**: Apply filters to database records
3. **Generate Output**: Create Excel/reports from filtered database records
4. **Save Output**: Store output metadata in database

## Key Benefits

1. **Performance**: Database queries are faster than Excel parsing
2. **Scalability**: Individual records can be indexed and queried efficiently
3. **Data Integrity**: Structured data with proper validation
4. **Flexibility**: Can easily add new filtering/searching capabilities
5. **Consistency**: All services work with same data structure
6. **Unified API**: Single endpoint handles both upload and manual creation
7. **No Redundancy**: Eliminated duplicate endpoints and functionality

## API Endpoints

### Upload Resort Report File
```bash
# File Upload Mode
POST /resort-report-files/
Content-Type: multipart/form-data

file: resort_data.xlsx

# Manual Creation Mode  
POST /resort-report-files/
Content-Type: application/x-www-form-urlencoded

name=Resort Report 2024&date=2024-06-02
```

### Upload APIs Report File  
```bash
# File Upload Mode
POST /apis-report-files/
Content-Type: multipart/form-data

file: passenger_data.xlsx

# Manual Creation Mode
POST /apis-report-files/
Content-Type: application/x-www-form-urlencoded

name=APIS Report 2024&date=2024-06-02
```

### Legacy Endpoints (Backward Compatibility)
```bash
POST /resort-report-files/upload
POST /apis-report-files/upload
```

## All Output Services Verified ✅

1. **✅ APIs Report Output**: Uses database `AdvancedPassengerInformation` records
2. **✅ Extras Filtered Reservation Output**: Uses database `ResortReport` records via `get_reports_by_file()`
3. **✅ Caretaker Extras View Output**: Uses database `ResortReport` records via `get_reports_by_file()`

**No services parse Excel files directly for report generation - all work with database models.**

## Testing

- File upload routes import successfully
- Migration applied successfully  
- Database schema updated
- All services use database-first approach
- Unified endpoints handle both upload and manual creation

## Future Enhancements

1. **Batch Processing**: For very large Excel files
2. **Validation**: Enhanced data validation during parsing
3. **Duplicate Detection**: Prevent duplicate records
4. **Progress Tracking**: Show upload progress for large files
5. **File Versioning**: Handle multiple versions of the same file
6. **Async Processing**: Handle large file uploads asynchronously 