# ⛽ Fuel Price Checker NSW

**Fuel Price Checker NSW** is a simple and interactive Streamlit web app that helps drivers, commuters, and businesses easily **compare real-time and historical fuel prices** across New South Wales (NSW).  
With this tool, you can stay informed about fuel price trends, explore different brands and fuel types, and find the best prices near you — saving you money every time you fill up!

---

## 🚀 Live Demo

https://fuel-check-nsw.streamlit.app/

---

## 🔍 Features

**Live fuel prices:** View the latest prices for multiple brands and fuel types in NSW.  
**Historical trends:** Analyze price changes over time to pick the best days to refuel.  
**Interactive maps:** Visualize station locations and prices on a simple map.  
**Flexible filters:** Filter by brand, fuel type, and address to find exactly what you need.  
**Beautiful visualizations:** Interactive graphs powered by Plotly for clear insights.

---

## 🗃️ Tech Stack

- **Python 3**
- **Streamlit** — fast, easy web app framework
- **Pandas** — data manipulation and filtering
- **Plotly Express** — for interactive charts and trends
- **CSV dataset** — real-time & historical fuel price data

---

## 📂 Project Structure

This project mainly has two parts:
- **filePriceChecker.py**: Handles the core backend logic like fetching fuel price data (e.g., using APIs or CSVs), cleaning it, and preparing it for display.
- **ui.py**: The Streamlit app that defines the user interface. It calls functions from the backend, displays filters, tables, and the map. Everything updates instantly as the user changes options.

There’s also a `requirements.txt` that lists all Python packages needed to run the app. The major dependencies are Streamlit, pandas, requests, and possibly libraries for mapping (like pydeck or folium, depending on your code).

To run the app on your machine:
1. Clone this repository  
2. (Optional) Create a virtual environment and activate it  
3. Install dependencies with `pip install -r requirements.txt`  
4. Start the app using `streamlit run ui.py`

This app is currently live at [https://fuel-check-nsw.streamlit.app/](https://fuel-check-nsw.streamlit.app/) — it’s deployed using Streamlit Community Cloud. You can fork this repo and deploy your own version for free; just connect your GitHub repo on Streamlit Cloud and point it to `ui.py` as the entry point.

Feel free to contribute, suggest improvements, or adapt this project for other regions.  
Built with ❤️ using Python and Streamlit.
