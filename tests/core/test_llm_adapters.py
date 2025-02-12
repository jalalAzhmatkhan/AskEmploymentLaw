import random

from core.configs import settings
from core.llm_adapters import LLMAdapters
from schemas.core.llm_adapters import LLMAdapterMessageRequest

def test_llm_adapters():
    """ Unit test to check LLM Adapter """
    if settings.TEST_LLM_SERVICE:
        # Test Ollama Service
        llm_host = "http://localhost"
        llm_port = "11434"
        llm_service = "ollama"
        llm_name="mistral"
        llm_tag="latest"

        llm_adapter = LLMAdapters(
            host=llm_host,
            port=llm_port,
            model=llm_name,
            llm_service=llm_service, # type: ignore
            tag=llm_tag,
        )

        ## Test Case 1
        request_messages = []
        system_message = LLMAdapterMessageRequest(
            role="system",
            content="""
                You are an intelligent system that answer the question about the Indonesian Law. 
                Do NOT answer any inquiries other than about the Indonesian Law. If you are 
                asked about anything besides the Indonesian Law, please response with 
                this Python dictionary: 
                {\"error\": 502, \"error_message\": \"Question is out-of-topics.\"} 
                The valid answer should be a clean Python dictionary like: 
                {\"status\": \"200\", \"response\": \"the_answer\"} 
                the answer should be placed as the \"response\" key's value and in Indonesian language. 
                The nature of the questions is about the Indonesian Law. Please answer 
                accordingly. Do NOT add any information other than the specified Python dictionary.
                If you happened to have no knowledge to answer it, please response it 
                with a clean Python dictionary: 
                {\"error\": 501, \"error_message\": \"No knowledge available.\"} 
                Example questions and its answers: 
                **Pertanyaan:** Apa hukuman untuk pencurian di Indonesia? 
                **Jawaban:** Dalam KUHP Pasal 362, pencurian diancam dengan pidana penjara paling lama lima tahun 
                atau pidana denda paling banyak enam puluh juta rupiah. 
                **Pertanyaan:** Siapa presiden pertama Indonesia? 
                **Jawaban:** {\"error\": 502, \"error_message\": \"Question is out-of-topics.\"} 
                **Pertanyaan:** Apa perbedaan antara PHK dan pengunduran diri dalam hukum Indonesia? 
                **Jawaban:** Dalam UU Ketenagakerjaan No. 13 Tahun 2003, PHK adalah pemutusan hubungan kerja oleh 
                perusahaan, sedangkan pengunduran diri adalah keputusan karyawan untuk berhenti atas kehendak sendiri.
            """
        )
        request_messages += [system_message]
        mocked_user_question_1 = LLMAdapterMessageRequest(
            role="user",
            content="""
            Apakah anda bisa menjelaskan Undang-Undang No 13 Tahun 2003 di Republik Indonesia?
            """
        )
        request_messages += [mocked_user_question_1]

        response_from_llm_1 = llm_adapter.inference(request_messages)
        assert isinstance(response_from_llm_1, dict), "Response from the LLM should be a dictionary."
        assert "status" in response_from_llm_1, "No status for the answer of a valid question."
        assert str(response_from_llm_1["status"]) == "200", "LLM response failed."
        assert "response" in response_from_llm_1, "No response from the LLM."

        ## Test Case 2
        request_messages = []
        mocked_user_question_2 = LLMAdapterMessageRequest(
            role="user",
            content="""
            Apakah anda bisa menjelaskan bagaimana cara sebuah makanan dicerna sehingga menghasilkan nutrisi?
            """
        )
        request_messages += [system_message]
        request_messages += [mocked_user_question_2]

        response_from_llm_2 = llm_adapter.inference(request_messages)
        assert isinstance(response_from_llm_2, dict), "Response from the LLM should be a dictionary."
        assert "error" in response_from_llm_2
        assert str(response_from_llm_2["error"]) == "502"
