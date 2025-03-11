import pytest

from core.llm_adapters import LLMAdapters
from schemas.core.llm_adapters import LLMAdapterMessageRequest
from services.text_classifier_service import TextClassifierService

@pytest.mark.asyncio
async def test_llm_adapters():
    """ Unit test to check LLM Adapter """
    # Test Ollama Service
    llm_host = "http://localhost"
    llm_port = "11434"
    llm_service = "ollama"
    llm_name = "mistral"
    llm_tag = "latest"

    llm_adapter = LLMAdapters(
        host=llm_host,
        port=llm_port,
        model=llm_name,
        llm_service=llm_service,  # type: ignore
        tag=llm_tag,
    )
    text_classifier = TextClassifierService(
        llm_host=llm_host,
        llm_port=llm_port,
        llm_model=llm_name,
        llm_service=llm_service,  # type: ignore
        llm_tag=llm_tag,
    )

    ## Test Case 1
    request_messages = []
    system_message = LLMAdapterMessageRequest(
        role="system",
        content="""
            You are an intelligent system that answer the question about the Indonesian Law. 
            DO NOT answer any inquiries other than about the Indonesian Law. If you encounter
            questions about anything other than the Indonesian Law, marked by the \"is_law_question\" flag
            value being \"false\", please strictly response with this Python dictionary: 
            {\"error\": 502, \"error_message\": \"Question is out-of-topics.\"} \n 
            The valid answer should be a clean Python dictionary like: 
            {\"status\": \"200\", \"response\": \"the_answer\"} \n
            the answer should be placed as the \"response\" key's value and in Indonesian language. 
            The nature of the questions is about the Indonesian Law. Please answer 
            accordingly. Do NOT add any information other than the specified Python dictionary.
            If you happened to have no knowledge to answer it, please response it 
            with a clean Python dictionary: 
            {\"error\": 501, \"error_message\": \"No knowledge available.\"} \n
            Please STRICTLY follow the response format as stated above!
            Example questions and its answers: \n
            **Pertanyaan:** Apa hukuman untuk pencurian di Indonesia? 
            **is_law_question:** true
            **Jawaban:** Dalam KUHP Pasal 362, pencurian diancam dengan pidana penjara paling lama lima tahun 
            atau pidana denda paling banyak enam puluh juta rupiah. 
            **Pertanyaan:** Siapa presiden pertama Indonesia? 
            **is_law_question:** false
            **Jawaban:** {\"error\": 502, \"error_message\": \"Question is out-of-topics.\"} 
            **Pertanyaan:** Apa perbedaan antara PHK dan pengunduran diri dalam hukum Indonesia? 
            **is_law_question:** true
            **Jawaban:** Dalam UU Ketenagakerjaan No. 13 Tahun 2003, PHK adalah pemutusan hubungan kerja oleh 
            perusahaan, sedangkan pengunduran diri adalah keputusan karyawan untuk berhenti atas kehendak sendiri.
            **Pertanyaan:** Sebutkan nutrisi yang terkandung dalam makanan sehat! 
            **is_law_question:** false
            **Jawaban:** {\"error\": 502, \"error_message\": \"Question is out-of-topics.\"}\n\n
        """
    )
    request_messages += [system_message]
    mocked_user_question_1 = LLMAdapterMessageRequest(
        role="user",
        content="""
        Apakah anda bisa menjelaskan Undang-Undang No 13 Tahun 2003 di Republik Indonesia?\n
        """
    )
    request_messages += [mocked_user_question_1]
    is_law_question_1 = await text_classifier.classify("law,not law",mocked_user_question_1.content)
    is_law_question_content = f"""
    is_law_question: {is_law_question_1}\n
    """
    is_law_question_msg = LLMAdapterMessageRequest(
        role="user",
        content=is_law_question_content,
    )
    request_messages += [is_law_question_msg]


    response_from_llm_1 = await llm_adapter.inference(request_messages)
    assert isinstance(response_from_llm_1, dict), "Response from the LLM should be a dictionary."
    assert "status" in response_from_llm_1, "No status for the answer of a valid question."
    assert str(response_from_llm_1["status"]) == "200", "LLM response failed."
    assert "response" in response_from_llm_1, "No response from the LLM."

    ## Test Case 2
    request_messages = []
    mocked_user_question_2 = LLMAdapterMessageRequest(
        role="user",
        content="""
        Apakah anda bisa menjelaskan bagaimana cara sebuah makanan dicerna sehingga menghasilkan nutrisi?\n
        """
    )
    request_messages += [system_message]
    request_messages += [mocked_user_question_2]
    is_law_question_2 = await text_classifier.classify("law,not law", mocked_user_question_2.content)
    is_law_question_content = f"""
        is_law_question: {is_law_question_2}\n
        """
    is_law_question_msg_2 = LLMAdapterMessageRequest(
        role="user",
        content=is_law_question_content,
    )
    request_messages += [is_law_question_msg_2]

    response_from_llm_2 = await llm_adapter.inference(request_messages)
    assert isinstance(response_from_llm_2, dict), "Response from the LLM should be a dictionary."
    assert "error" in response_from_llm_2
    assert str(response_from_llm_2["error"]) == "502"

    # Test Ollama Service via Langchain
    llm_host = "http://localhost"
    llm_port = "11434"
    llm_service = "ollama-langchain"
    llm_name = "mistral"
    llm_tag = "latest"

    llm_adapter_langchain = LLMAdapters(
        host=llm_host,
        port=llm_port,
        model=llm_name,
        llm_service=llm_service,  # type: ignore
        tag=llm_tag,
    )

    ## Test Case 3
    request_messages = []
    system_message = LLMAdapterMessageRequest(
        role="system",
        content="""
            You are an intelligent system that answer the question about the Indonesian Law. 
            DO NOT answer any inquiries other than about the Indonesian Law. If you encounter
            questions about anything other than the Indonesian Law, please strictly response with 
            this Python dictionary: 
            {\"error\": 502, \"error_message\": \"Question is out-of-topics.\"} \n
            The valid answer should be a clean Python dictionary like: 
            {\"status\": \"200\", \"response\": \"the_answer\"} \n
            the answer should be placed as the \"response\" key's value and in Indonesian language. 
            The nature of the questions is about the Indonesian Law. Please answer 
            accordingly. Do NOT add any information other than the specified Python dictionary.
            If you happened to have no knowledge to answer it, please response it 
            with a clean Python dictionary: 
            {\"error\": 501, \"error_message\": \"No knowledge available.\"} \n
            Please STRICTLY follow the response format as stated above!
            Example questions and its answers: 
            **Pertanyaan:** Apa hukuman untuk pencurian di Indonesia? 
            **Jawaban:** Dalam KUHP Pasal 362, pencurian diancam dengan pidana penjara paling lama lima tahun 
            atau pidana denda paling banyak enam puluh juta rupiah. \n
            **Pertanyaan:** Siapa kanselir Jerman saat Perang Dunia II? 
            **Jawaban:** {\"error\": 502, \"error_message\": \"Question is out-of-topics.\"} \n
            **Pertanyaan:** Apa perbedaan antara PHK dan pengunduran diri dalam hukum Indonesia? 
            **Jawaban:** Dalam UU Ketenagakerjaan No. 13 Tahun 2003, PHK adalah pemutusan hubungan kerja oleh 
            perusahaan, sedangkan pengunduran diri adalah keputusan karyawan untuk berhenti atas kehendak sendiri. \n
            **Pertanyaan:** Sebutkan nutrisi yang terkandung dalam makanan sehat! 
            **Jawaban:** {\"error\": 502, \"error_message\": \"Question is out-of-topics.\"} \n
        """
    )
    request_messages += [system_message]
    mocked_user_question_3 = LLMAdapterMessageRequest(
        role="user",
        content="""
        Apakah anda bisa menjelaskan Undang-Undang No 13 Tahun 2003 di Republik Indonesia?
        """
    )
    request_messages += [mocked_user_question_3]

    response_from_llm_3 = await llm_adapter_langchain.inference(request_messages)
    assert isinstance(response_from_llm_3, dict), "Response from the LLM should be a dictionary."
    assert "status" in response_from_llm_3, "No status for the answer of a valid question."
    assert str(response_from_llm_3["status"]) == "200", "LLM response failed."
    assert "response" in response_from_llm_3, "No response from the LLM."

@pytest.mark.asyncio
async def test_process_scrape_document_with_llm():
    """Unit test for Process scrapped website with LLM"""
    # Test Ollama Service
    llm_host = "http://localhost"
    llm_port = "11434"
    llm_service = "ollama"
    llm_name = "mistral"
    llm_tag = "latest"

    llm_adapter = LLMAdapters(
        host=llm_host,
        port=llm_port,
        model=llm_name,
        llm_service=llm_service,  # type: ignore
        tag=llm_tag,
    )

    # Test Case 1
    request_messages = []
    system_message = LLMAdapterMessageRequest(
        role="system",
        content="""
            You are an intelligent scraper system that extract important information from the provided 
            extracted text of a Governmental website.
            The valid answer should be a clean Python dictionary like: 
            {
                \"status\": \"200\", 
                \"response\": \"the_answer\"
            } 
            the answer should be placed as the \"response\" key's value. 
            The nature of the questions is about scraping/extracting information about the Indonesian Law
            document from an unstructured text set. Please answer accordingly. Do NOT add any information other 
            than the specified Python dictionary.
            If you happened to have no knowledge to answer it, please response it 
            with a clean Python dictionary: 
            {\"error\": 501, \"error_message\": \"No knowledge available.\"} 
            Example questions and its answers: 
            **Question:** Please extract the title of the law from this downloaded markdown!
            Your answer should be a clean Python dictionary like:
            {\"title\": \"the_extracted_title\"}
            Place your answer on the \"title\" key's value.\n
            # Undang-undang Nomor 28 Tahun 2013 Tentang ABC

Jenis/Bentuk Peraturan| UNDANG-UNDANG  
---|---  
Pemrakarsa| PEMERINTAH PUSAT  
Nomor| 13  
Tahun| 2003  
Tentang| KETENAGAKERJAAN  
Tempat Penetapan| Jakarta  
            **Answer:** {
                \"status\": \"200\", 
                \"response\": {\"title\": \"Undang-undang Nomor 28 Tahun 2013 Tentang ABC\"}
            }
            **Question:** Please extract the type of the law, the law number, the law
            year, and what is the law's talking about from this downloaded markdown!
            Your answer should be a clean Python dictionary like:
            {
                \"type\": \"the_extracted_type_in_string\", 
                \"year\": integer_of_the_extracted_year, 
                \"number\": integer_of_the_extracted_law_number,
                \"about\": \"the_law_about_in_string\"
            }
            Place your answer on the key's value. The type of the law usually taken from 
            the \"Jenis/Bentuk Peraturan\" field. The law number usually taken from the 
            \"Nomor\" field. The law year usually taken from the \"Tahun\" field. The 
            law's about usually taken from the \"Tentang\" field. \n
            # Undang-undang Nomor 28 Tahun 2013 Tentang ABC\n
\n
Jenis/Bentuk Peraturan| UNDANG-UNDANG\n  
---|---  \n
Pemrakarsa| PEMERINTAH PUSAT\n  
Nomor| 28  \n
Tahun| 2013  \n
Tentang| ABC  \n
Tempat Penetapan| Jakarta  \n
            **Answer:** {
                \"status\": \"200\", 
                \"response\": {
                    \"type\": \"UNDANG-UNDANG\", 
                    \"year\": 2013, 
                    \"number\": 28,
                    \"about\": \"ABC\"
                }
            }
        """
    )
    mocked_user_question_1 = LLMAdapterMessageRequest(
        role="user",
        content="""
            Please extract the type of the law, the law number, the law
            year, what is the law's talking about, and the law's place of confirmation 
            from this downloaded markdown!
            Your answer should be a clean Python dictionary like:
            {
                \"type\": \"the_extracted_type_in_string\", 
                \"year\": integer_of_the_extracted_year, 
                \"number\": integer_of_the_extracted_law_number,
                \"about\": \"the_law_about_in_string\",
                \"place_of_confirmation\": \"the_extracted_place_of_confirmation_in_string\"
            }
            Place your answer on the key's value. The type of the law usually taken from 
            the \"Jenis/Bentuk Peraturan\" field. The law number usually taken from the 
            \"Nomor\" field. The law year usually taken from the \"Tahun\" field. The 
            law's about usually taken from the \"Tentang\" field. The law's place of 
            confimation usually taken from \"Tempat Penetapan\" field. \n
            # Undang-undang Nomor 12 Tahun 2002 Tentang EFG\n
\n
Jenis/Bentuk Peraturan| UNDANG-UNDANG\n  
---|---  \n
Pemrakarsa| PEMERINTAH PUSAT\n  
Nomor| 12  \n
Tahun| 2002  \n
Tentang| EFG  \n
Tempat Penetapan| Jakarta\n  
        """
    )
    request_messages += [system_message]
    request_messages += [mocked_user_question_1]

    response_from_llm_1 = await llm_adapter.inference(request_messages)
    assert "status" in response_from_llm_1, "No status from the LLM."
    assert "response" in response_from_llm_1, "No response from the LLM."
    assert isinstance(response_from_llm_1, dict), "Wrong data type."
    assert response_from_llm_1["status"] == "200", "Wrong response status."
    assert "year" in response_from_llm_1["response"], "No \"year\" field on the response."
    assert "type" in response_from_llm_1["response"], "No \"type\" field on the response."
    assert "number" in response_from_llm_1["response"], "No \"number\" field on the response."
    assert "about" in response_from_llm_1["response"], "No \"about\" field on the response."
    assert "place_of_confirmation" in response_from_llm_1["response"], ("No \"place_of_confirmation\" "
                                                                        "field on the response.")
    assert isinstance(response_from_llm_1["response"]["year"], int), "Wrong response data type."  # type: ignore
    assert isinstance(response_from_llm_1["response"]["number"], int), "Wrong response data type."  # type: ignore
    assert isinstance(response_from_llm_1["response"]["about"], str), "Wrong response data type."  # type: ignore
