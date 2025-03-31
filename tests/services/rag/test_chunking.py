from services.rag import Chunking

def test_chunking_fixed_length():
    """Test the fixed length chunking method."""
    full_text = "This is a test text. It is used to test the chunking functionality."
    chunk_length = 10
    chunking = Chunking(full_text)
    chunks = chunking.fixed_length(chunk_length)

    assert len(chunks) == 7  # 7 chunks of length 10
    assert all(len(chunk) <= chunk_length for chunk in chunks)  # All chunks should be of length <= chunk_length
    assert chunks[0] == "This is a "  # First chunk
    assert "nality." in chunks[-1]  # Last chunk

def test_chunking_sentence_based():
    """Test the sentence based chunking method."""
    full_text = "This is a test text. It is used to test the chunking functionality."
    chunking = Chunking(full_text)
    chunks = chunking.sentence_based()

    assert len(chunks) == 2  # 2 sentences in the text
    assert all(isinstance(chunk, str) for chunk in chunks)  # All chunks should be strings
    assert chunks[0] == "This is a test text."  # First sentence
    assert chunks[-1] == "It is used to test the chunking functionality."  # Last sentence

def test_chunking_paragraph_based():
    """Test the paragraph based chunking method."""
    full_text = "This is a test text. The test will be used to check chunking function.\n\nThere are 11 chunking methods, namely: fixed length, sentence based, paragraph based, etc. It is used in RAG system."
    chunking = Chunking(full_text)
    chunks = chunking.paragraph_based()

    assert len(chunks) == 2  # 2 paragraphs in the text
    assert all(isinstance(chunk, str) for chunk in chunks)  # All chunks should be strings
    assert chunks[0] == "This is a test text. The test will be used to check chunking function."  # First paragraph
    assert "It is used in RAG system." in chunks[-1]  # Last paragraph

def test_chunking_sliding_windows():
    """Test the sliding windows chunking method."""
    full_text = "This is a test text. It is used to test the chunking functionality. It is a just simple test."
    n_slide = 2
    chunking = Chunking(full_text)
    chunks = chunking.sliding_windows(n_slide)

    assert len(chunks) == 2  # 2 chunks with sliding window of size 2
    assert all(isinstance(chunk, str) for chunk in chunks)  # All chunks should be strings
    assert chunks[0] == "This is a test text. It is used to test the chunking functionality."  # First chunk
    assert chunks[-1] == "It is used to test the chunking functionality. It is a just simple test."  # Last chunk
