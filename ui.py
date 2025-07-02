import streamlit as st
import pandas as pd
import filePriceChecker as fp
import plotly.express as px

data = pd.read_csv('data/overall.csv')


# Set the page configuration for Streamlit
st.set_page_config(
    page_title="Fuel Price Checker NSW",
    page_icon=":fuelpump:",
    layout="wide",
    initial_sidebar_state="collapsed",

    
)





st.sidebar.title("Menu")

if 'selected_page' not in st.session_state:
    st.session_state['selected_page'] = 'Home'

# Go to Home
if st.sidebar.button('Home', use_container_width=True):
    st.session_state['selected_page'] = 'Home'

if st.sidebar.button('Realtime Price By Location', use_container_width=True):
    st.session_state['selected_page'] = 'Realtime'

if st.sidebar.button('Realtime Price By Brand', use_container_width=True):
    st.session_state['selected_page'] = 'Analysis'

if st.sidebar.button('Trends', use_container_width=True):
    st.session_state['selected_page'] = 'Trend'

# Main page content
if st.session_state['selected_page'] == 'Home':
    st.markdown("""
                # Welcome to the NSW Fuel Price Checker.

                This tool helps you quickly find and compare real-time fuel prices for different brands and fuel types across NSW.

                Whether you’re planning your next trip, keeping an eye on daily price trends, or just want to make sure you’re getting the best deal at the pump - you’re in the right place.

                **Key features:**
                - 🚗 **Live fuel prices** for multiple fuel types and brands.
                - 📍 **Map view** to easily locate fuel stations near you.
                - 📊 **Latest updates** to help you make informed choices.

                Use the sidebar menu to check current prices, view fuel stations on the map, or learn more about this project.""")
    st.map(data[['latitude','longitude']], zoom = 5)
    

elif st.session_state['selected_page'] == 'Realtime':
    st.markdown("Fuel Price Checker NSW")

    option = st.selectbox("Select a location", options=data['address'].unique() )
    col1, col2 = st.columns(2)
    with col1:
        brand_name = data[data['address'] == option][['brand']][0:1]
        brand = st.selectbox('', options=brand_name['brand'].unique(),)
    with col2:
        available_fuel = data[data['address'] == option][['fuel_type']]
        f_type = st.selectbox('Select Fuel Type', options=available_fuel['fuel_type'].unique())


    # Initialize flags
    if 'show_price' not in st.session_state:
        st.session_state['show_price'] = False

    # Toggle buttons
    if st.button('Show Latest Price'):
        st.session_state['show_price'] = not st.session_state['show_price']


    # Conditionally display
    if st.session_state['show_price']:
        fp.activate()
        ans = data[
            (data['address'] == option) & 
            (data['brand'] == brand) & 
            (data['fuel_type'] == f_type)
        ][['brand', 'fuel_type', 'price']]
        st.write("Latest Price Data for Selected Filters:", ans)
        

        update_time = data[data['address'] == option][['last_updated']].head(1)
        if not update_time.empty:
            st.write('Updated on:', update_time.iloc[0, 0])

    if 'show_map' not in st.session_state:
        st.session_state['show_map'] = False
        
    if st.button('Show on Map'):
        st.session_state['show_map'] = not st.session_state['show_map']

    if st.session_state['show_map']:
        st.map(data[
            (data['address'] == option) & 
            (data['brand'] == brand)
        ][['latitude', 'longitude']], zoom=15, size=15)

if st.session_state['selected_page'] == 'Analysis':
    fp.activate()
    data = pd.read_csv('data/overall.csv')
    
    brands = data['brand'].unique()
    selected_brand = st.selectbox("Select Brand:", brands)

    address_input = st.text_input('Seach on map:')
        

    df_brand = data[data['brand'] == selected_brand]

    dfs_by_address = {addr: group for addr, group in df_brand.groupby('address')}
    column1, column2 = st.columns(2)
    for addr, df in dfs_by_address.items():
        with column1:
            st.text(f"📍 {addr}")
            st.dataframe(df[['fuel_type','price','isAdBlueAvailable']])
        with column2:
            if address_input is not '':
                data = pd.read_csv('data/overall.csv')
                lat_long = data[data['address']== address_input][['latitude','longitude']][0:1]  # Example: get one row
                
                st.map(lat_long)
                break

                
if st.session_state['selected_page'] == 'Trend':
    st.header('Check trend')   
    data['last_updated'] = pd.to_datetime(data['last_updated'], errors='coerce')

    # ---- 2. Filter: You can add dropdowns to choose brand/fuel type ----
    st.title("⛽ Fuel Price Analysis")
    fp.activate()
    st.subheader("Select filters:")
    brands = data['brand'].unique().tolist()
    fuel_types = data['fuel_type'].unique().tolist()

    selected_brand = st.selectbox("Brand", brands)
    selected_fuel = st.selectbox("Fuel Type", fuel_types)

    data_filtered = data[
        (data['brand'] == selected_brand) &
        (data['fuel_type'] == selected_fuel)
    ]

    st.write(f"Showing price trend for **{selected_brand}** - **{selected_fuel}**")

    # ---- 3. Price trend line chart ----
    if not data_filtered.empty:
        fig = px.line(
            data_filtered.sort_values('last_updated'),
            x='last_updated',
            y='price',
            color='address',
            title=f'Price Trend for {selected_brand} - {selected_fuel}',
            markers=True
        )
        fig.update_layout(xaxis_title='Date', yaxis_title='Price (cents/Litre)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for this filter.")

    # ---- 4. Average price by brand bar chart ----
    st.subheader("Average Price by Brand")

    avg_price = data.groupby(['brand', 'fuel_type'])['price'].mean().reset_index()

    fig2 = px.bar(
        avg_price,
        x='brand',
        y='price',
        color='fuel_type',
        barmode='group',
        title='Average Fuel Price by Brand and Fuel Type'
    )

    st.plotly_chart(fig2, use_container_width=True)
        
