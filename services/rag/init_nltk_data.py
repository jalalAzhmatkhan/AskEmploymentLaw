import nltk

def init_nltk_data():
    """
    Function to initialize NLTK data.
    :return:
    """
    try:
        print("Checking NLTK data...")
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

if __name__ == "__main__":
    init_nltk_data()
