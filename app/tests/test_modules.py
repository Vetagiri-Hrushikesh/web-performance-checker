import unittest
from app import create_app

class TestOverviewAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_circular_progress(self):
        response = self.client.get('/api/lighthouse/overview/circular-progress/premium')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Performance', response.get_json())
        self.assertIn('Accessibility', response.get_json())
        self.assertIn('Best Practices', response.get_json())
        self.assertIn('SEO', response.get_json())

if __name__ == '__main__':
    unittest.main()
