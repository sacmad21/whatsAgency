import unittest
from unittest.mock import patch
from feedback_management_utils import save_feedback_entry, fetch_feedback_by_user

class TestFeedbackManagementUtils(unittest.TestCase):

    @patch("feedback_management_utils.config.create_container")
    def test_save_feedback_entry(self, mock_container):
        mock_container.return_value.create_item.return_value = None
        result = save_feedback_entry(
            feedback_id="F123",
            business_id="B001",
            user_id="U001",
            content="Great service!",
            timestamp="2024-01-01T00:00:00Z"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Feedback entry saved successfully.")

    @patch("feedback_management_utils.config.create_container")
    def test_fetch_feedback_by_user(self, mock_container):
        mock_container.return_value.query_items.return_value = [
            {
                "feedbackId": "F123",
                "businessId": "B001",
                "userId": "U001",
                "content": "Great service!",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        ]
        result = fetch_feedback_by_user(user_id="U001", business_id="B001")
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)

if __name__ == "__main__":
    unittest.main()
