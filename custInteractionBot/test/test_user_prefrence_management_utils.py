import unittest
from unittest.mock import patch
from user_preferences_utils import save_user_preferences, fetch_user_preferences, fetch_property_info, search_properties

class TestUserPreferencesUtils(unittest.TestCase):

    @patch("user_preferences_utils.config.create_container")
    def test_save_user_preferences(self, mock_container):
        mock_container.return_value.create_item.return_value = None
        result = save_user_preferences(
            preference_id="P123",
            business_id="B001",
            user_id="U001",
            budget=50000,
            location="Downtown",
            property_type="Apartment"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "User preferences saved successfully.")

    @patch("user_preferences_utils.config.create_container")
    def test_fetch_user_preferences(self, mock_container):
        mock_container.return_value.query_items.return_value = [
            {
                "preferenceId": "P123",
                "businessId": "B001",
                "userId": "U001",
                "budget": 50000,
                "location": "Downtown",
                "propertyType": "Apartment"
            }
        ]
        result = fetch_user_preferences(user_id="U001", business_id="B001")
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)

    @patch("user_preferences_utils.config.create_container")
    def test_fetch_property_info(self, mock_container):
        mock_container.return_value.query_items.return_value = [
            {
                "propertyId": "PR123",
                "businessId": "B001",
                "address": "123 Main St",
                "price": 50000,
                "type": "Apartment"
            }
        ]
        result = fetch_property_info(property_id="PR123", business_id="B001")
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)

    @patch("user_preferences_utils.config.create_container")
    def test_search_properties(self, mock_container):
        mock_container.return_value.query_items.return_value = [
            {
                "propertyId": "PR123",
                "businessId": "B001",
                "address": "123 Main St",
                "price": 50000,
                "type": "Apartment"
            }
        ]
        filters = {"price": 50000, "type": "Apartment"}
        result = search_properties(business_id="B001", filters=filters)
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)

if __name__ == "__main__":
    unittest.main()
