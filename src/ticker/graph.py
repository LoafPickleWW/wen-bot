import matplotlib.pyplot as plt
import datetime
import io

def get_graph(candles):     
    sorted_candles = sorted(candles, key=lambda x: x["timestamp"])
    times = [datetime.datetime.fromtimestamp(candle["timestamp"]) for candle in sorted_candles]
    prices = [float(candle["close"]) for candle in sorted_candles]  # Ensure float conversion

    # Plot the data
    plt.figure(figsize=(10, 5), facecolor="none")
    plt.plot(times, prices, linestyle="-", color="green", linewidth=2.5)
    
    # Add fill below the line
    plt.fill_between(times, prices, min(prices), alpha=0.2, color="green")
    
    # Set the limits to zoom in on the data
    plt.xlim(times[0], times[-1])
    plt.ylim(min(prices), max(prices))
    plt.axis('off')
    
    img_io = io.BytesIO()
    plt.savefig(img_io, format="png", transparent=True)
    img_io.seek(0)
    plt.close()

    return img_io
