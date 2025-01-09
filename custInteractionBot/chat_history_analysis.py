from query_management_utils import fetch_queries_by_user
from feedback_management_utils import fetch_feedback_by_user

def analyze_chat_history(business_id, user_id):
    """
    Analyze chat history to identify patterns and generate insights.
    """
    # Fetch user queries
    query_result = fetch_queries_by_user(user_id=user_id, business_id=business_id)
    if query_result["status"] != "success":
        return {"status": "error", "message": "Failed to fetch user queries."}

    user_queries = query_result["data"]

    # Fetch user feedback
    feedback_result = fetch_feedback_by_user(user_id=user_id, business_id=business_id)
    if feedback_result["status"] != "success":
        return {"status": "error", "message": "Failed to fetch user feedback."}

    user_feedback = feedback_result["data"]

    # Analyze chat patterns (Placeholder: implement advanced analysis later)
    most_common_queries = [query["queryText"] for query in user_queries[:3]]  # Example logic
    feedback_summary = [feedback["content"] for feedback in user_feedback[:3]]  # Example logic

    # Generate insights
    insights = {
        "most_common_queries": most_common_queries,
        "recent_feedback": feedback_summary
    }

    return {"status": "success", "insights": insights}

# Example usage
if __name__ == "__main__":
    result = analyze_chat_history(
        business_id="B001",
        user_id="U005"
    )
    print(result)
