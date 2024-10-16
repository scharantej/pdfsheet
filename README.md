## Flask Application Design for PDF to Google Sheets Data Transformation

### HTML Files

**index.html:**

This is the main page of the application. It contains a form for uploading multiple PDF files:

```html
<form action="{{ url_for('upload') }}" method="POST" enctype="multipart/form-data">
    <input type="file" name="files[]" multiple>
    <input type="submit" value="Upload">
</form>
```

### Routes

**upload()** route:

Handles the upload of multiple PDF files. It extracts the data from the uploaded files and transforms it into a Google Sheets format.

```python
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        data = extract_data(files)
        upload_to_google_sheets(data)
        return redirect(url_for('success'))
```

**success()** route:

Displays a success message after the data transformation is complete:

```python
@app.route('/success')
def success():
    return "Data transformation completed successfully!"
```

**extract_data()** function:

Extracts the data from the uploaded PDF files. This can be implemented using a third-party library like PyPDF2:

```python
import PyPDF2

def extract_data(files):
    data = []
    for file in files:
        pdf = PyPDF2.PdfFileReader(file)
        for page in range(pdf.getNumPages()):
            text = pdf.getPage(page).extractText()
            data.append(text)
    return data
```

**upload_to_google_sheets()** function:

Uploads the transformed data to a Google Sheet. This can be implemented using the gspread library:

```python
import gspread

def upload_to_google_sheets(data):
    gc = gspread.service_account()
    sheet = gc.open('Insurance Data').sheet1
    sheet.update('A1', data)
```