import re

# 🔹 Define simple rules to detect visual intent in the query
def is_visual_query(query: str) -> bool:
    visual_keywords = [
        "chart", "plot", "graph", "trend", "visualize",
        "show distribution", "bar chart", "pie chart", "line graph",
        "statistics over time", "time series", "data chart"
    ]

    query = query.lower()
    return any(keyword in query for keyword in visual_keywords)

# Optional utility — clean text or file names (extend as needed)
def sanitize_filename(name: str) -> str:
    return re.sub(r'[^\w\-_\. ]', '_', name)
