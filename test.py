import unittest
from unittest.mock import patch
from scrap import scrape_the_web

class TestScrapeTheWeb(unittest.TestCase):

    @patch('scrap.requests.get')
    def test_scrape_title_found(self, mock_get):
        mock_get.return_value.text = '<html><head><title>Test Title</title></head></html>'
        title = scrape_the_web('http://github.com', 'Title')
        self.assertEqual(title, 'Test Title')

    @patch('scrap.requests.get')
    def test_scrape_title_not_found(self, mock_get):
        mock_get.return_value.text = '<html><head></head></html>'
        title = scrape_the_web('http://github.com', 'Title')
        self.assertEqual(title, 'Title not found')

    @patch('scrap.requests.get')
    def test_scrape_headlines_found(self, mock_get):
        mock_get.return_value.text = '<html><body><h1>Test Headline</h1></body></html>'
        headlines = scrape_the_web('http://github.com', 'Headlines')
        self.assertEqual(headlines, 'Test Headline')

    # Similarly, write test cases for other scrape types

if __name__ == '__main__':
    unittest.main()
