
# Import the necessary libraries
import PyPDF2
import gspread
from flask import Flask, request, redirect, url_for, render_template

# Create a Flask app
app = Flask(__name__)

# Define the upload route
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the uploaded files
        files = request.files.getlist('files')

        # Extract data from the uploaded files
        data = []
        for file in files:
            pdf = PyPDF2.PdfFileReader(file)
            for page in range(pdf.getNumPages()):
                text = pdf.getPage(page).extractText()
                data.append(text)

        # Upload the data to a Google Sheet
        gc = gspread.service_account()
        sheet = gc.open('Insurance Data').sheet1
        sheet.update('A1', data)

        # Redirect to the success page
        return redirect(url_for('success'))

# Define the success route
@app.route('/success')
def success():
    # Render the success page
    return render_template('success.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
