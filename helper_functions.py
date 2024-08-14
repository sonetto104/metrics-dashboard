import PyPDF2

def extract_date_from_pdf(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    metadata = pdf_reader.metadata
    creation_date = metadata.get('/CreationDate')
    if creation_date:
        creation_date = creation_date[2:].replace("'", '')
        creation_date = creation_date[:8]
        return creation_date[:4] + '-' + creation_date[4:6] + '-' + creation_date[6:]
    else:
        return None

def anonymize_apprentice_names(df):
    df['Apprentice'] = df.index.to_series().apply(lambda i: f'Apprentice {i}')
    return df