import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import base64

def plot_chart(chart_data):
    chart_type = chart_data.get("type", "line")
    x = chart_data.get("x", [])
    y = chart_data.get("y", [])
    title = chart_data.get("title", "MemoryGPT Chart")
    xlabel = chart_data.get("xlabel", "")
    ylabel = chart_data.get("ylabel", "")

    fig, ax = plt.subplots()
    
    if chart_type == "line":
        ax.plot(x, y, marker='o')
    elif chart_type == "bar":
        ax.bar(x, y)
    elif chart_type == "scatter":
        ax.scatter(x, y)
    else:
        raise ValueError("Unsupported chart type")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    base64_img = base64.b64encode(img.read()).decode("utf-8")
    plt.close(fig)
    return base64_img
