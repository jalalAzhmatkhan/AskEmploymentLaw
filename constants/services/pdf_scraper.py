HTTP_SCHEMA = "http://"
HTTPS_SCHEMA = "https://"

# Playwright Area
DICT_AREA_JAKARTA = {"latitude": -6.2088, "longitude": 106.8456}
HREF_ATTRIBUTE = "href"
LAW_SCRAPER_STARTING_PAGE = "https://peraturan.go.id/id/uu-no-13-tahun-2003"
LOCALE_ID = "id"
PAGE_LOADED_SELECTOR = "body"
TIMEZONE_JAKARTA = "Asia/Jakarta"

# Scraped Columns
JENIS_PERATURAN = "Jenis/Bentuk Peraturan"
NOMOR = "Nomor"
TAHUN = "Tahun"
TENTANG = "Tentang"
TEMPAT_PENETAPAN = "Tempat Penetapan"
DITETAPKAN_TANGGAL = "Ditetapkan Tanggal"
TANGGAL_PENGUNDANGAN = "Tanggal Pengundangan"
NONE_TYPE_TXT = "NoneType: None"

DOWNLOADED_LAW_MARKDOWN_EXAMPLE = """
# Undang-undang Nomor 13 Tahun 2003 Tentang Ketenagakerjaan\n
\n
Jenis/Bentuk Peraturan| UNDANG-UNDANG\n  
---|---  \n
Pemrakarsa| PEMERINTAH PUSAT\n  
Nomor| 13  \n
Tahun| 2003  \n
Tentang| KETENAGAKERJAAN\n  
Tempat Penetapan| Jakarta \n 
Ditetapkan Tanggal| 25 Maret 2003\n  
Pejabat yang Menetapkan|  \n
Status| Berlaku  \n
Dokumen Peraturan| [](/files/UU+13-2003.pdf) [](/files/UU+13-2003pjl.pdf)\n  
Jumlah dilihat| 34832  \n
Jumlah diDownload| 3914  \n
Tahun Pengundangan| 2003  \n
---|---  \n
Nomor Pengundangan| 39\n  
Nomor Tambahan| 4279  \n
Tanggal Pengundangan| 25 Februari 2003\n  
Pejabat Pengundangan|  \n
  \n
  *   *   *   *\n 
\n
\n
\n
###### **Hubungan Antar Peraturan**\n
\n
  \n
**Mencabut :**\n  
\n
  * [Undang-Undang Nomor 25 Tahun 1997](/id/uu-no-25-tahun-1997 "lihat detail") Tentang Ketenagakerjaan\n  
\n
  * [Undang-Undang Nomor 11 Tahun 1998](/id/uu-no-11-tahun-1998 "lihat detail") Tentang Perubahan Berlakunya Uu 25-1997 Tentang Ketenagakerjaan\n    
\n
**Dilaksanakan Oleh (Peraturan Pelaksana) :**\n  
\n
  * [Peraturan Menteri Ketenagakerjaan Nomor 34 Tahun 2016](/id/permenaker-no-34-tahun-2016 "lihat detail") Tentang Akreditasi Lembaga Pelatihan Kerja\n  
\n
  * [Peraturan Menteri Ketenagakerjaan Nomor 1 Tahun 2017](/id/permenaker-no-1-tahun-2017 "lihat detail") Tentang Struktur dan Skala Upah\n  
\n
###### **Dasar Hukum**\n
\n
  \n
\n
  * [Undang-Undang Nomor 25 Tahun 1997](/id/uu-no-25-tahun-1997 "lihat detail") Tentang Ketenagakerjaan\n  
\n
  * [Undang-Undang Nomor 11 Tahun 1998](/id/uu-no-11-tahun-1998 "lihat detail") Tentang Perubahan Berlakunya Uu 25-1997 Tentang Ketenagakerjaan\n  
\n
  * [Undang-Undang Nomor 28 Tahun 2000](/id/uu-no-28-tahun-2000 "lihat detail") Tentang Penetapan Perpu 3-2000 Tentang Perubahan Uu 11-1998 Tentang Perubahan Berlakunya Uu 25-1997 Tentang Ketenagakerjaan Menjadi Uu\n  
\n
  * [](/id/uud-1945 "lihat detail") Tentang Undang-undang Dasar Negara Republik Indonesia Tahun 1945\n  

"""
EXAMPLE_ANALYZED_RESPONSE = """
{
    \"status\": \"200\",
    \"response\": {
        \"type\": \"UNDANG-UNDANG\", 
        \"year\": 13, 
        \"number\": 2003,
        \"about\": \"KETENAGAKERJAAN\",
        \"title\": \"Undang-undang Nomor 13 Tahun 2003 Tentang Ketenagakerjaan\",
        \"place_of_confirmation\": \"Jakarta\",
        \"date_of_confirmation\": \"25 Maret 2003\",
        \"date_of_enactment\": "25 Februari 2003\",
        \"effective_date\": null,
        \"document_links\": [
            {
                \"url\": \"/files/UU+13-2003.pdf\"
            },
            {
                \"url\": \"/files/UU+13-2003pjl.pdf\"
            }
        ],
        \"removing_other_law\": true,
        \"removed_laws\": [
            {
                \"type\": \"UNDANG-UNDANG\",
                \"year\": 1997,
                \"number\": 25,
                \"url\": \"/id/uu-no-25-tahun-1997\",
                \"about\": \"Ketenagakerjaan\"
            },
            {
                \"type\": \"UNDANG-UNDANG\",
                \"year\": 1998,
                \"number\": 11,
                \"url\": \"/id/uu-no-11-tahun-1998\",
                \"about\": \"Perubahan Berlakunya Uu 25-1997 Tentang Ketenagakerjaan\"
            }
        ],
        \"executing_laws\": [
            {
                \"type\": \"Peraturan Menteri\",
                \"year\": 2016,
                \"number\": 34,
                \"url\": \"/id/permenaker-no-34-tahun-2016\",
                \"about\": \"Akreditasi Lembaga Pelatihan Kerja\"
            },
            {
                \"type\": \"Peraturan Menteri\",
                \"year\": 2017,
                \"number\": 1,
                \"url\": \"/id/permenaker-no-1-tahun-2017\",
                \"about\": \"Struktur dan Skala Upah\"
            }
        ]
    }
}
"""
