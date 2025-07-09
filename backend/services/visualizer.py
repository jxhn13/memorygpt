import matplotlib.pyplot as plt
import io
import base64

# 🔹 Generates a base64 image from a chart
def plot_chart(data: dict) -> str:
    """
    Plot a simple chart from structured data.

    Expected format:
    {
        "x": ["Jan", "Feb", "Mar"],
        "y": [100, 150, 90],
        "title": "Monthly Sales",
        "xlabel": "Month",
        "ylabel": "Revenue"
    }
    """
    x = data.get("x", [])
    y = data.get("y", [])

    if not x or not y:
        return ""

    plt.figure(figsize=(8, 4))
    plt.plot(x, y, marker='o', linestyle='-', color='skyblue')
    plt.title(data.get("title", "Chart"))
    plt.xlabel(data.get("xlabel", "X-axis"))
    plt.ylabel(data.get("ylabel", "Y-axis"))
    plt.tight_layout()

    # Save chart to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode image as base64 string
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return image_base64
