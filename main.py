import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import io
import fitz  # PyMuPDF

# Title of the Streamlit app
st.title("Multiple PDF Upload, Merge, and Display")

# File uploader for multiple PDFs
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

# Define a flag to control the visibility of previews
merge_clicked = False

# Function to read PDF using PyPDF2
def read_pdf(file):
    pdf_reader = PdfReader(file)
    all_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        all_text += page.extract_text()
    return all_text

# If PDFs are uploaded and the merge button hasn't been pressed yet
if uploaded_files and not merge_clicked:
    for uploaded_file in uploaded_files:
        
        # Displaying PDF content using PyPDF2 for now
        text = read_pdf(uploaded_file)
        
        if text:
            st.write(f"**File Name:** {uploaded_file.name}")
        else:
            st.write(f"No display content from {uploaded_file.name}.")

    # Button to merge PDFs
    if st.button("Merge PDFs"):
        # Set the flag to true, which will hide the previews
        merge_clicked = True

        # Initialize a PDF writer
        pdf_writer = PdfWriter()

        # Iterate over the uploaded files and append their pages
        for uploaded_file in uploaded_files:
            pdf_reader = PdfReader(uploaded_file)
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

        # Output the merged PDF to a BytesIO buffer
        merged_pdf = io.BytesIO()
        pdf_writer.write(merged_pdf)
        merged_pdf.seek(0)

        # Provide a download link for the merged PDF
        st.success("PDFs have been successfully merged!")
        st.download_button(
            label="Download Merged PDF",
            data=merged_pdf,
            file_name="merged_output.pdf",
            mime="application/pdf"
        )

        # Render and display the merged PDF on the screen
        with fitz.open(stream=merged_pdf, filetype="pdf") as merged_document:
            st.write("### Merged PDF Preview:")
            for page_num in range(len(merged_document)):
                # Extract the page as an image
                page = merged_document.load_page(page_num)
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")  # Convert to PNG
                st.image(img_data, caption=f"Page {page_num + 1}", use_column_width=True)

        # Reset the buffer for download, so the user can still download the merged PDF
        merged_pdf.seek(0)