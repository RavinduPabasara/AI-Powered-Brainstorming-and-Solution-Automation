#nlp_processor.py
import nltk

class NLPProcessor:
    def download_nltk_data(self):
        try:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
        except Exception as e:
            print(f"Error downloading NLTK data: {e}")
            print("Please manually download the required NLTK data using the following commands:")
            print(">>> import nltk")
            print(">>> nltk.download('punkt')")
            print(">>> nltk.download('stopwords')")
            print(">>> nltk.download('wordnet')")
            exit(1)



