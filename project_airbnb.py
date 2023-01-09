#PACKAGE
import random
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.figure_factory as ff

#FONT FOR WEBSITES
FONT = {'family': 'serif',
        'color':  '#2C3639',
        'weight': 'bold',
        'size': 13,
        }

#DATASET
df_listing = pd.read_csv("listing_byCountry.csv")
df_region = pd.read_csv("DQLab_nieghbourhood(22Sep2022).csv")
df_review = pd.read_csv("DQLab_reviews(22Sep2022).csv")

#SETTING WEB PAGE
st.set_page_config(
    page_title="project airbnb",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""
            <h2 style='text-align: center; color: #FFFFFF;'>AIRBNB SINGAPORE LISTING DATA ANALYSIS</h2>
        """, unsafe_allow_html=True)

# DROP UNNECESSARY COLUMN FROM DATA LISTING
df_listing.drop(labels=["Unnamed: 0", "lat-long"], axis=1, inplace=True)
df_listing['id'] = df_listing.id.astype(np.int64)

# FILTER DATA LISTING COUNTRY ONLY SINGAPORE
df_listing = df_listing[df_listing['country name'] == "Singapore"]

# FILTER DATA PRICE = 0
price = df_listing.price != 0
avail = df_listing.availability_365 != 0
df_listing = df_listing[(price) & (avail)]

# CLEAN DATA LISTING WHICH IS "HAVING PRICE PERNIGHT > 2000"
df_listing = df_listing.sort_values("price", ascending=False)
df_listing = df_listing[15:][:]


# st.dataframe(df_listing['neighbourhood'].unique())
# SIDE BAR
sidebar = st.sidebar

agree = sidebar.checkbox('Show Data Table')
if agree:
    st.markdown("""
    <h2 style='text-align: center; color: #FFFFFF ;'>Listing Data Table</h2>
    """, unsafe_allow_html=True)
    sidebar.info('The data table will show on top of the page', icon="ℹ️")
    
    st.info('The table only shows 5 rows, if data is empty please choose another neighborhood', icon="ℹ️")
    agree = st.checkbox('Tips     ')
    if agree:
        st.info('Click on column name to sort value ascending or descending', icon="ℹ️")
    neighbourhood = sidebar.multiselect(
        "Select Neighborhood:",
        options=df_listing["neighbourhood"].unique(), max_selections=3,
        default=df_listing["neighbourhood"].iloc[2]
    )
    room_type = sidebar.multiselect(
        "Select Room Type:",
        options=df_listing["room_type"].unique(),
        default=df_listing["room_type"].unique(),
    )
    price_filter = sidebar.slider(
        'Select range of price (SGD):',
        0, 3500, (100, 200))
    max_range_p = price_filter[1]
    min_range_p = price_filter[0]
    sidebar.write('Price Range:', min_range_p,'-',max_range_p)

    df_selection = df_listing.query(
        "neighbourhood ==@neighbourhood & room_type ==@room_type & price >=@min_range_p & price <=@max_range_p")
    st.dataframe(df_selection[['id','name','host_name','neighbourhood','price','room_type']].head(5))
    st.markdown("---")
else:
    sidebar.info("Check the checkbox above for data sampling!",icon="ℹ️")
    sidebar.markdown("---")
    sidebar.write("Kindly check my Linkedin profile by clicking link below")
    sidebar.markdown("""
    [<h4 style='text-align: left; color: #FFFFFF ;'>My Linkedin Profile</h4>](https://www.linkedin.com/in/gustavsmnt/)
""", unsafe_allow_html=True)
    sidebar.image(
    "https://skillacademy-prod-image.skillacademy.com/offline-marketplace/DQLab_Icon.png",width = 100)
    sidebar.write("DQLab Bootcamp Final Projects")
    sidebar.write("0136 - Gustav Bagus Samanta")
st.write('')
st.write('')
st.write('')
st.write('')
#PRICE DISTRIBUTION OF SINGAPORE LISTING
a = st.container()
with a:
    st.markdown(
        """
        ##### Airbnb Singapore price distribution
        """)

    with st.expander(label="Show Visualization Airbnb Singapore price distribution"):            
        col1, col2, col3 = st.columns(3)
        with col1:
            x = df_listing['price']
            hist_data = [x]
            group_labels = ['Singapore'] # name of the dataset

            fig = ff.create_distplot(hist_data, group_labels, curve_type='normal'
                    , show_hist=False)
            fig.update_layout(
            yaxis_title="Density",
            xaxis_title="Price",
            legend_title="Country Name",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
            )
            st.plotly_chart(fig)
        
        text_a = st.text_area(label="", value="""From the visualization above the most price density are between range SGD 100 to SGD 360 per-night.""")
    st.markdown('---')

#PRICE TRENDS PER NEIGHBOURHOOD
b = st.container()
with b:
    st.markdown(
        """
        ##### Airbnb Singapore price trend in the Neighborhood
        """)
    
    col1, col2, col3 = st.columns(3)

    order = df_listing.merge(
        df_review, left_on="id", right_on="listing_id")
    order = order.groupby(['neighbourhood','room_type'])['price'].mean().to_frame('avg_price').reset_index()
    order = order.sort_values('avg_price', ascending = False)      
    with col1:
        agree = st.checkbox('Tips ')
        if agree:
            st.info('Please select room type, hover mouse to line inside chart area for details', icon="ℹ️")                  
    with col2:
        room_type = st.selectbox(
        "Select the Room Type:",
        options=order["room_type"].unique())
        
    df_selection = order.query(
        """room_type == @room_type""")
    fig = px.line(df_selection, y="avg_price", x="neighbourhood"
    , color='room_type')
    fig.update_layout(
        yaxis_title="Average Price",
        xaxis_title="Neighborhoods",
        legend_title="Room Type",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
        )
    st.plotly_chart(fig)
    text_b = st.text_area(label=" ", value="""The chart above shows price trends from each neighborhood grouped by room type. As a note,  not all neighborhoods have all room types (based on the data).""") 
st.markdown('---')


#id dan name listing apa yang mempunyai number of reviews paling banyak?Mengapa bisa terjadi demikian?(semi-adv)
c = st.container()
with c:
    st.markdown(
        """
        ##### Most review listing of Airbnb Singapore
        """)
    
    col1, col2, col3 = st.columns(3)

    ordermap = df_listing.merge(
                df_review, left_on="id", right_on="listing_id")
    ordermap = ordermap.groupby(['id','name','room_type','neighbourhood','latitude','longitude','price'])['date'].size().to_frame('review').reset_index()
    ordermap = ordermap.sort_values('review',ascending = False)
    max_rev = ordermap[['id','name','room_type','neighbourhood','price','review']].head(10).reset_index()
    
    fig = px.bar(max_rev, y="name", x="review"
    , barmode='group'
    ,hover_name='name',hover_data=['id','room_type','neighbourhood','price','review'])
    fig.update_layout(
    yaxis_title="Listing Name",
    xaxis_title="Reviews",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
    )
        
    st.plotly_chart(fig)
    text_c = st.text_area(label="  ", value="The chart above shows the 10 most reviewed Airbnb Singapore listings.")
    
    with st.expander(label="Show Table Most review listing of Airbnb Singapore"):
            agree = st.checkbox('Tips  ')
            if agree:
                st.info('Click on column name to sort value ascending or descending', icon="ℹ️")
            st.dataframe(max_rev)

st.markdown('---')

# Bagaimana rata-rata harga listings per neigbourhood_group?(semi-adv)
d = st.container()
with d:
    st.markdown(
        """
        ##### Airbnb Singapore average price by region
        """)

    col1, col2, col3 = st.columns(3)
    ordermap_region = ordermap.merge(df_region, on='neighbourhood')
    ordermap_region_avg = ordermap_region.groupby(['room_type','neighbourhood_group'])['price'].mean().to_frame('avg_price').reset_index()

    fig = px.bar(ordermap_region_avg, y="avg_price", x="neighbourhood_group"
        , color='room_type', barmode='group')
    fig.update_layout(
    yaxis_title="Average Price",
    xaxis_title="Region",
    legend_title="Room Type" ,
    font=dict(
    family="Courier New, monospace",
    size=18,
    color="RebeccaPurple"
    )
    )
    st.plotly_chart(fig) 
    text_d = st.text_area(label="   ", value="""The chart above shows average price trends from each region grouped by room type. As a note,  not all region have all room types (based on the data).""")
    
    with st.expander(label="Show Table Airbnb Singapore average price by region"):
            agree = st.checkbox('Tips   ')
            if agree:
                st.info('Click on column name to sort value ascending or descending', icon="ℹ️")
            st.dataframe(ordermap_region_avg)

st.markdown('---')
#Pada bulan dan tahun berapa aktivitas penyewaan listing paling sedikit dan paling banyak ?(advance)
ordermap_region_sort = df_listing.merge(
            df_review, left_on="id", right_on="listing_id")
ordermap_region_sort['date'] = pd.to_datetime(ordermap_region_sort['date'])
ordermap_region_sort['month_year'] = ordermap_region_sort['date'].apply(lambda x: x.strftime('%B-%Y'))

e = st.container()
with e:
    st.markdown(
        """
        ##### Most Rental Activity Airbnb Singapore 
        """)
    ordermap_region_sort_desc = ordermap_region_sort.groupby(['month_year'])['date'].size().to_frame('review').reset_index()
    ordermap_region_sort_desc = ordermap_region_sort_desc.sort_values('review',ascending=False)
    ordermap_region_sort_desc = ordermap_region_sort_desc.head(20)
    fig = px.bar(ordermap_region_sort_desc, y="review", x="month_year"
            , barmode='group'
            ,hover_name='month_year',hover_data=['review','month_year'])
    fig.update_layout(
    yaxis_title="Rental",
    xaxis_title="Date",
    font=dict(
    family="Courier New, monospace",
    size=18,
    color="RebeccaPurple"
    )
    )
    st.plotly_chart(fig)
    text_e = st.text_area(label="    ", value="The chart above shows month and year with the most rental activity ")

    with st.expander(label="Show Table Most Rental Activity Airbnb Singapore "):
        agree = st.checkbox('Tips    ')
        if agree:
            st.info('Click on column name to sort value ascending or descending', icon="ℹ️")
        st.dataframe(ordermap_region_sort_desc)
st.markdown('---')
f = st.container()
with f:
    st.markdown(
        """
        ##### Least Rental Activity Airbnb Singapore
        """)
    ordermap_region_sort_asc = ordermap_region_sort.groupby(['month_year'])['date'].size().to_frame('review').reset_index()
    ordermap_region_sort_asc = ordermap_region_sort_asc.sort_values('review')
    ordermap_region_sort_asc = ordermap_region_sort_asc.head(20)
    fig = px.bar(ordermap_region_sort_asc, y="review", x="month_year"
            , barmode='group'
            ,hover_name='month_year',hover_data=['review','month_year'])
    fig.update_layout(
    yaxis_title="Rental",
    xaxis_title="Date",
    font=dict(
    family="Courier New, monospace",
    size=18,
    color="RebeccaPurple"
    )
    )
    st.plotly_chart(fig)
    text_f = st.text_area(label="     ", value="The chart above shows month and year with the least rental activity ")
    with st.expander(label="Show Table Least Rental Activity Airbnb Singapore"):
        agree = st.checkbox('Tips               ')
        if agree:
            st.info('Click on column name to sort value ascending or descending', icon="ℹ️")
        st.dataframe(ordermap_region_sort_asc)
st.markdown('---')   




#MAP
map = st.container()
        
with map:
    
    st.markdown(
        """
        ##### LISTING MAP SPREAD ORDER COUNT IN THE LAST 4 YEARS
        """)



    agree = st.checkbox('Tips')
    if agree:
        st.info("""Scroll mouse inside map area to zoom in or zoom out, hover mouse to the dot inside map area to view listing details, hold right-click mouse inside map area to pan""", icon="ℹ️")
    
    ordermap = df_listing.merge(
            df_review, left_on="id", right_on="listing_id")
    ordermap = ordermap.groupby(['neighbourhood','room_type','latitude','longitude','name','price'])['date'].size().to_frame('order').reset_index()
    rented_365_map = px.scatter_mapbox(ordermap, lat="latitude", lon="longitude", color="room_type"
    , hover_name='name',hover_data=['neighbourhood', 'order'],zoom=10.5, width=900)
    rented_365_map.update_layout(mapbox_style="open-street-map")
    rented_365_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    rented_365_map.update_layout(
    legend_title="Room Type",
    font=dict(
    family="Courier New, monospace",
    size=18,
    color="RebeccaPurple"
    )
    )
    st.plotly_chart(rented_365_map)


for i in range(4):
    st.write("")

st.markdown("""
    <h5 style='text-align: center; color: #1746A2;'>For more airbnb singapore listing analysis and data visualization, please visit my Friend streamlit webapp</h5>
""", unsafe_allow_html=True)

st.markdown("""
    
    [<h5 style='text-align: center; color: #5F9DF7 ;'>Adifta Airbnb Project</h5>](https://nununu-py-dqlab-final-project-main-g26t83.streamlit.app/)

""", unsafe_allow_html=True)
