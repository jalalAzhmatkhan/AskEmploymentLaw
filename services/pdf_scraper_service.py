# pylint: skip-file
from typing import Dict, List, Literal, Optional, Union
from uuid import uuid4

from html2text import HTML2Text
from playwright.async_api import async_playwright

from constants.core import llm_adapters as llm_adapters_constants
from constants.services import pdf_scraper as pdf_scraper_constants
from constants.services.pdf_scraper import NONE_TYPE_TXT
from core.llm_adapters import LLMAdapters
from core.logger import logger
from schemas import LLMAdapterMessageRequest, LLMAdapterUserMessageRequest

class Scraper:
    """
    Scraper class to get Law PDF files
    """
    def __init__(
        self,
        llm_model: str,
        llm_service: Literal[
            "groq",
            "huggingface",
            "ollama",
            "openai"
        ] = llm_adapters_constants.LLM_SERVICE_OPENAI,
        llm_service_api_key: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs
    ):
        """
        Init function
        :param url: (str)
        """
        self.target_url: str = url
        self.markdown_converter = HTML2Text()
        self.markdown_converter.ignore_links = False
        self.markdown_converter.ignore_images = True
        self.llm_model = llm_model
        self.llm_service = llm_service
        self.llm_host = None
        self.llm_port = None
        self.llm_model_tag = None
        self.llm_service_api_key = None

        if "host" in kwargs:
            self.llm_host = kwargs["host"]
        elif "ip_address" in kwargs:
            self.llm_host = kwargs["ip_address"]
        elif "llm_host" in kwargs:
            self.llm_host = kwargs["llm_host"]

        if "port" in kwargs:
            self.llm_port = kwargs["port"]
        elif "llm_port" in kwargs:
            self.llm_port = kwargs["llm_port"]

        if "tag" in kwargs:
            self.llm_model_tag = kwargs["tag"]
        elif "llm_tag" in kwargs:
            self.llm_model_tag = kwargs["llm_tag"]
        elif "llm_model_tag" in kwargs:
            self.llm_model_tag = kwargs["llm_model_tag"]

        if llm_service_api_key:
            self.llm_service_api_key = llm_service_api_key

    async def analyze_extracted_text(
        self,
        extracted_text: str,
        user_prompt: LLMAdapterUserMessageRequest
    )->Optional[Dict[str, str]]:
        """
        Function to analyze the extracted text
        :param extracted_text:
        :param user_prompt:
        :return:
        """
        llm_adapter = LLMAdapters(
            model=self.llm_model,
            api_key=self.llm_service_api_key,
            llm_service=self.llm_service,
            host=self.llm_host,
            port=self.llm_port,
            tag=self.llm_model_tag,
        )

        # create a system message prompt
        message_to_llm = []
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
            {\"error\": 501, \"error_message\": \"No knowledge available.\"} \n
            Please STRICTLY follow the response format as stated above!\n
            Example questions and its answers: 
            **Question:** Tolong ekstrak judul peraturan dari markdown berikut.
            Jawaban anda harus berupa Python dictionary seperti:\n
            {\"title\": \"string_judul\"}
            Tempatkan jawaban anda pada nilai key \"title\".\n\n
            Markdown:\n
            # Undang-undang Nomor 28 Tahun 2013 Tentang ABC\n
Jenis/Bentuk Peraturan| UNDANG-UNDANG  \n
---|---  \n
Pemrakarsa| PEMERINTAH PUSAT\n  
Nomor| 13  \n
Tahun| 2003  \n
Tentang| KETENAGAKERJAAN  \n
            **Answer:** {
                \"status\": \"200\", 
                \"response\": {\"title\": \"Undang-undang Nomor 28 Tahun 2013 Tentang ABC\"}
            }
            **Question:** Tolong ekstrak jenis/bentuk peraturan, nomor peraturan, tahun
            peraturan, dan tentang dari markdown berikut!
            Jawaban anda harus berupa Python dictionary seperti:\n
            {
                \"type\": \"string_jenis/bentuk_peraturan\", 
                \"year\": integer_tahun_peraturan, 
                \"number\": integer_nomor_peraturan,
                \"about\": \"string_tentang\"
            }
            Tempatkan jawaban anda pada nilai key dari dictionary di atas. \n\n
            Markdown:\n
            # Undang-undang Nomor 28 Tahun 2013 Tentang ABC\n
\n
Jenis/Bentuk Peraturan| UNDANG-UNDANG\n  
---|---  \n
Pemrakarsa| PEMERINTAH PUSAT\n  
Nomor| 28  \n
Tahun| 2013  \n
Tentang| ABCDEFabc  \n
            **Answer:** {
                \"status\": \"200\", 
                \"response\": {
                    \"type\": \"UNDANG-UNDANG\", 
                    \"year\": 2013, 
                    \"number\": 28,
                    \"about\": \"ABCDEFabc\"
                }
            }
            **Question:** Tolong ekstrak jenis/bentuk peraturan, nomor peraturan, tahun
            peraturan, dan tentang dari markdown berikut!
            Jawaban anda harus berupa Python dictionary seperti:
            {
                \"type\": \"the_extracted_type_in_string\", 
                \"year\": integer_of_the_extracted_year, 
                \"number\": integer_of_the_extracted_law_number,
                \"about\": \"the_law_about_in_string\"
            }
            Tempatkan jawaban anda pada nilai dari key-key dari dictionary di atas. \n\n
            Markdown:\n
            # Undang-undang Nomor 19 Tahun 2003\n
\n
Jenis/Bentuk Peraturan| UNDANG-UNDANG\n  
---|---  \n 
Nomor| 19  \n
Tahun| 2003  \n
Tentang| Pengelolaan Minyak dan Gas    \n
            **Answer:** {
                \"status\": \"200\", 
                \"response\": {
                    \"type\": \"UNDANG-UNDANG\", 
                    \"year\": 2003, 
                    \"number\": 19,
                    \"about\": \"Pengelolaan Minyak dan Gas\",
                }
            }\n\n
            """
        )
        message_to_llm.append(system_message)
        if user_prompt.role == "user" and len(user_prompt.content) > 0:
            user_prompt.content += "\n" + extracted_text
        message_to_llm.append(user_prompt)

        llm_inference = await llm_adapter.inference(messages=message_to_llm)
        logger.info(f"Scraper: analyze_extracted_text: LLM inference response: {llm_inference}", exc_info=True)
        return llm_inference

    def extract_text_from_markdown(self, markdown: str)->Optional[str]:
        """
        Function to extract text from a given HTML markdown
        :param markdown:
        :return:
        """
        try:
            return self.markdown_converter.handle(markdown)
        except Exception as e:
            req_id = str(uuid4()).replace("-", "")
            logger.error(f"Scraper: extract_text_from_markdown: {req_id} {e}", exc_info=True)
            raise RuntimeError("An error occured while processing the scrapped URL.")

    async def scrape(self, url: Optional[str] = None)->list:
        """
        Function to scrape the PDF and its metadata
        :return:
        """
        if not url:
            url = self.target_url
        scrape_results = []
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context(
                geolocation=pdf_scraper_constants.DICT_AREA_JAKARTA,
                locale=pdf_scraper_constants.LOCALE_ID,
                timezone_id=pdf_scraper_constants.TIMEZONE_JAKARTA,
            )
            page = await context.new_page()

            await page.goto(url, timeout=60000)

            # Wait for the necessary elements to load
            await page.wait_for_selector("body")

            title_container = await page.query_selector('section#description > div.detail_title_1 > h1')
            title = ""
            if title_container:
                title = await title_container.inner_text()
                title = title.strip()

            description_section = await page.query_selector("section#description")
            description_section_html = ""
            if description_section:
                description_section_html = await description_section.inner_html()

            reviews_section = await page.query_selector("section#reviews")
            reviews_section_html = ""
            if reviews_section:
                reviews_section_html = await reviews_section.inner_html()

            text_description = self.extract_text_from_markdown(
                description_section_html
            )
            text_description = text_description.replace(NONE_TYPE_TXT, "")
            text_reviews = self.extract_text_from_markdown(
                reviews_section_html
            )
            text_reviews = text_reviews.replace(NONE_TYPE_TXT, "")
            all_text_markdown = text_description + "\n\n" + text_reviews

            text_desc_prompt = LLMAdapterUserMessageRequest(
                role="user",
                content="""
                    **Question:**\n
            Tolong ekstrak judul peraturan, jenis/bentuk peraturan, nomor peraturan, tahun peraturan,
            tentang, tempat penetapan, tanggal penetapan, tanggal pengundangan, tanggal berlaku, link-link
            dokumen peraturan, apakah peraturan ini mencabut peraturan lain (boolean), detail URL dan tentang
            dari peraturan yang dicabut, dan detail URL dan tentang dari peraturan pelaksana.
            Jawaban anda harus berupa Python dictionary seperti:
            {
                \"type\": \"string_jenis/bentuk_peraturan\", 
                \"year\": integer_nomor_peraturan, 
                \"number\": integer_nomor_peraturan,
                \"about\": \"string_tentang\",
                \"title\": \"string_judul_peraturan\",
                \"place_of_confirmation\": \"string_tempat_penetapan\",
                \"date_of_confirmation\": \"string_tanggal_penetapan\",
                \"date_of_enactment\": "string_tanggal_pengundangan\",
                \"effective_date\": \"string_tanggal_berlaku\",
                \"document_links\": [
                    {
                        \"url\": \"string_url_dokumen_peraturan\"
                    }
                ],
                \"removing_other_law\": boolean,
                \"removed_laws\": [
                    {
                        \"type\": \"string_jenis/bentuk_peraturan_yang_dicabut\",
                        \"year\": integer_nomor_peraturan_yang_dicabut,
                        \"number\": integer_nomor_peraturan_yang_dicabut,
                        \"url\": \"string_url_ke_peraturan_yang_dicabut\",
                        \"about\": \"string_tentang_peraturan_yang_dicabut\"
                    }
                ],
                \"executing_laws\": [
                    {
                        \"type\": \"string_jenis/bentuk_peraturan_pelaksana\",
                        \"year\": integer_nomor_peraturan_pelaksana,
                        \"number\": integer_nomor_peraturan_pelaksana,
                        \"url\": \"string_url_ke_peraturan_pelaksana\",
                        \"about\": \"string_tentang_peraturan_pelaksana\"
                    }
                ]
            }
            Tempatkan jawaban anda pada nilai key-key dari dictionary di atas. \n\n
            **Contoh Markdown:**\n
                """
            )
            text_desc_prompt.content += text_desc_prompt.content + pdf_scraper_constants.DOWNLOADED_LAW_MARKDOWN_EXAMPLE
            text_desc_prompt.content += text_desc_prompt.content + """
                \n**Example response:**\n
                <example_response>
                \n\n
                Berikut markdown yang akan anda ekstrak.
                **Markdown:**
            """
            text_desc_prompt.content = text_desc_prompt.content.replace(
                "<example_response>",
                pdf_scraper_constants.EXAMPLE_ANALYZED_RESPONSE
            )

            analyzed_text = await self.analyze_extracted_text(
                all_text_markdown,
                text_desc_prompt
            )

            logger.info(f"Scraper: scrape: the resulting information from {url} is: "
                        f"{analyzed_text}", exc_info=True)

            await page.close()
            await context.close()

        return scrape_results
