import random
import string
import unittest
from typing import Optional

class URLShortener:
    """
    A simple in-memory URL Shortener service for MVP development.
    Stores mappings of short codes to long URLs.
    """
    def __init__(self):
        # Mapping: short_code -> long_url
        self.storage = {}
        # Character set for Base62 encoding (A-Z, a-z, 0-9)
        self.characters = string.ascii_letters + string.digits

    def _generate_unique_code(self, length=7):
        """Generates a random, unique base62 code of specified length."""
        while True:
            code = ''.join(random.choices(self.characters, k=length))
            # Check for collision
            if code not in self.storage:
                return code

    def get_short_url(self, long_url: str) -> str:
        """
        Generates a short code for a given long URL if one does not exist.
        Returns the formatted short URL string.
        """
        # Check if the URL already exists
        for short_code, url in self.storage.items():
            if url == long_url:
                return f"http://short.ly/{short_code}"
        
        # Generate and save the new mapping
        short_code = self._generate_unique_code()
        self.storage[short_code] = long_url
        return f"http://short.ly/{short_code}"

    def get_long_url(self, short_code: str) -> Optional[str]:
        """
        Retrieves the original long URL associated with a short code.
        Returns None if the code is not found.
        """
        return self.storage.get(short_code)

    def __len__(self):
        return len(self.storage)

# --- Unit Tests ---

class TestURLShortener(unittest.TestCase):
    
    def setUp(self):
        """Setup a fresh instance before each test."""
        self.shortener = URLShortener()

    def test_initialization(self):
        """Test if the shortener initializes correctly."""
        self.assertEqual(len(self.shortener), 0)
        self.assertIsInstance(self.shortener.storage, dict)

    def test_generate_and_store_new_url(self):
        """Test generating a new code and storing the mapping."""
        long_url = "https://www.example.com/new-page"
        short_url = self.shortener.get_short_url(long_url)
        
        # Check if the storage was updated
        self.assertEqual(len(self.shortener), 1)
        
        # Extract the code from the formatted URL for testing the storage dict
        short_code = short_url.split('/')[-1]
        self.assertIn(short_code, self.shortener.storage)
        self.assertEqual(self.shortener.storage[short_code], long_url)

    def test_retrieval_existing_url(self):
        """Test retrieving the long URL when the short code is known."""
        long_url = "https://www.test.com"
        self.shortener.get_short_url(long_url) # Pre-populate storage
        
        # Get the stored code (assuming only one entry was created)
        short_code = list(self.shortener.storage.keys())[0]

        retrieved_url = self.shortener.get_long_url(short_code)
        self.assertEqual(retrieved_url, long_url)

    def test_retrieval_non_existent_url(self):
        """Test retrieving the long URL when the code does not exist."""
        non_existent_code = "zzzzzzzzz" 
        retrieved_url = self.shortener.get_long_url(non_existent_code)
        self.assertIsNone(retrieved_url)

    def test_idempotency(self):
        """Test that calling get_short_url multiple times for the same URL returns the same short code."""
        url = "http://same.com"
        # First call generates the code
        short_url1 = self.shortener.get_short_url(url)
        code1 = short_url1.split('/')[-1]
        
        # Second call should reuse the code
        short_url2 = self.shortener.get_short_url(url)
        code2 = short_url2.split('/')[-1]
        
        self.assertEqual(code1, code2)
        self.assertEqual(short_url1, short_url2)

if __name__ == '__main__':
    unittest.main()
