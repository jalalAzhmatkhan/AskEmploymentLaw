from services import document_management_service

def test_extract_text_from_pdf():
    """Unit test to test PyTesseract OCR functionality"""
    with open('tests/services/rag/uu-no-1-tahun-2025.pdf', 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
        extracted_text = document_management_service.pdf_extractor(
            the_document=pdf_bytes
        )

        assert extracted_text is not None
        assert isinstance(extracted_text, str)
        assert len(extracted_text) > 0
        assert "UNDANG-UNDANG" in extracted_text
        assert "PRESIDEN REPUBLIK INDONESIA" in extracted_text
        assert "BADAN USAHA MILIK NEGARA" in extracted_text
