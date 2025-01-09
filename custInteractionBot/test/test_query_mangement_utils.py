import unittest
from unittest.mock import patch
from query_management_utils import save_customer_query, fetch_queries_by_user, save_chatbot_response, fetch_responses_by_query

class TestQueryManagementUtils(unittest.TestCase):

    @patch("query_management_utils.config.create_container")
    def test_save_customer_query(self, mock_container):
        mock_container.return_value.create_item.return_value = None
        result = save_customer_query(
            query_id="Q123",
            business_id="B001",
            user_id="U001",
            query_text="Is there a 2-bedroom apartment?",
            timestamp="2024-01-01T00:00:00Z"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Query saved successfully.")

    @patch("query_management_utils.config.create_container")
    def test_fetch_queries_by_user(self, mock_container):
        mock_container.return_value.query_items.return_value = [
            {
                "queryId": "Q123",
                "businessId": "B001",
                "userId": "U001",
                "queryText": "Is there a 2-bedroom apartment?",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        ]
        result = fetch_queries_by_user(user_id="U001", business_id="B001")
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)

    @patch("query_management_utils.config.create_container")
    def test_save_chatbot_response(self, mock_container):
        mock_container.return_value.create_item.return_value = None
        result = save_chatbot_response(
            response_id="R123",
            business_id="B001",
            query_id="Q123",
            response_text="Yes, a 2-bedroom apartment is available.",
            timestamp="2024-01-01T00:01:00Z"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Chatbot response saved successfully.")

    @patch("query_management_utils.config.create_container")
    def test_fetch_responses_by_query(self, mock_container):
        mock_container.return_value.query_items.return_value = [
            {
                "responseId": "R123",
                "businessId": "B001",
                "queryId": "Q123",
                "responseText": "Yes, a 2-bedroom apartment is available.",
                "timestamp": "2024-01-01T00:01:00Z"
            }
        ]
        result = fetch_responses_by_query(query_id="Q123", business_id="B001")
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)

if __name__ == "__main__":
    unittest.main()
