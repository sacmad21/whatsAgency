import unittest
from unittest.mock import patch
from session_management_utils import create_chat_session, fetch_chat_session

class TestSessionManagementUtils(unittest.TestCase):

    @patch("session_management_utils.config.create_container")
    def test_create_chat_session(self, mock_container):
        mock_container.return_value.create_item.return_value = None
        result = create_chat_session(
            session_id="S123",
            business_id="B001",
            user_id="U001",
            messages=[
                {"messageId": "M001", "content": "Hello!", "timestamp": "2024-01-01T00:00:00Z"}
            ]
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Chat session created successfully.")

    @patch("session_management_utils.config.create_container")
    def test_fetch_chat_session(self, mock_container):
        mock_container.return_value.query_items.return_value = [
            {
                "sessionId": "S123",
                "businessId": "B001",
                "userId": "U001",
                "messages": [
                    {"messageId": "M001", "content": "Hello!", "timestamp": "2024-01-01T00:00:00Z"}
                ]
            }
        ]
        result = fetch_chat_session(session_id="S123", business_id="B001")
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)

if __name__ == "__main__":
    unittest.main()
