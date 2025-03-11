import pytest

from services.text_classifier_service import TextClassifierService

@pytest.mark.asyncio
async def test_text_classifier_service():
    """Unit test for Text Classifier Service"""
    # Test Ollama Service
    llm_host = "http://localhost"
    llm_port = "11434"
    llm_service = "ollama"
    llm_name = "mistral"
    llm_tag = "latest"

    # Test Case 1
    str_classes_test_case_1="positive, negative"
    text_test_case_1 = """
    CCTV Dirusak Saat Aksi Indonesia Gelap di Patung Kuda.
    """

    text_classifier_service = TextClassifierService(
        llm_host=llm_host,
        llm_port=llm_port,
        llm_service=llm_service,  # type: ignore
        llm_model=llm_name,
        llm_tag=llm_tag,
    )
    ai_response_test_case_1 = await text_classifier_service.classify(
        classes=str_classes_test_case_1,
        text=text_test_case_1
    )

    assert isinstance(ai_response_test_case_1, dict)
    assert "status" in ai_response_test_case_1
    assert ai_response_test_case_1["status"] == "200"
    assert "response" in ai_response_test_case_1
    assert ai_response_test_case_1["response"] == "false"

    # Test Case 2
    str_classes_test_case_2 = "positive, neutral, negative"
    text_test_case_2 = """
        Pak Koki memasak makanan di tepi pantai sambil ditemani oleh anjing kesayangannya, Mako.
        """

    ai_response_test_case_2 = await text_classifier_service.classify(
        classes=str_classes_test_case_2,
        text=text_test_case_2
    )

    assert isinstance(ai_response_test_case_2, dict)
    assert "status" in ai_response_test_case_2
    assert ai_response_test_case_2["status"] == "200"
    assert "response" in ai_response_test_case_2
    assert ai_response_test_case_2["response"] == "neutral"
