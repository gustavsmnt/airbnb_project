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
df_listing = pd.read_csv("C:\\Users\\Gustav\\Desktop\\Final Project\\listing_byCountry.csv")
df_region = pd.read_csv("C:\\Users\\Gustav\\Desktop\\Final Project\\DQLab_nieghbourhood(22Sep2022).csv")
df_review = pd.read_csv("C:\\Users\\Gustav\\Desktop\\Final Project\\DQLab_reviews(22Sep2022).csv")

#SETTING WEB PAGE
st.set_page_config(
    page_title="project airbnb",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""
            <h2 style='text-align: center; color: #18978F;'>AIRBNB SINGAPORE LISTINGS DATA ANALYSIS</h2>
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
sidebar.image(
    "https://skillacademy-prod-image.skillacademy.com/offline-marketplace/DQLab_Icon.png")
sidebar.markdown('---')
sidebar.caption("Click This Button To Show Listing Data Table")
showdata_BNT = sidebar.button(label="Show Data Table")
sidebar.caption("Click This Button To Hide Listing Data Table")
hidedata_BTN = sidebar.button(label="Hide Data Table")
sidebar.markdown("---")


if showdata_BNT:
    st.markdown("""
        <h2 style='text-align: center; color: orange ;'>Listing Data Table</h2>
    """, unsafe_allow_html=True)
    st.dataframe(df_listing.sample(5))
    st.markdown("---")

if hidedata_BTN:

    showdata_BNT = False
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

    with st.expander(label="Show Visualization"):            
        col1, col2, col3 = st.columns(3)
        with col1:
            x = df_listing['price']
            hist_data = [x]
            group_labels = ['Singapore'] # name of the dataset

            fig = ff.create_distplot(hist_data, group_labels, curve_type='normal'
                    , show_hist=False)
            fig.update_layout(
            title="Plot Title",
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
        
        text_a = st.text_area(label="", value="""From the visualization above the most price 
        density are between range SGD100 - SGD360 per-night.""")
    st.markdown('---')

#PRICE TRENDS PER NEIGHBOURHOOD
b = st.container()
with b:
    st.markdown(
        """
        ##### Airbnb Singapore price trend in the Neighborhood
        """)
    with st.expander(label="Show Visualization"):
        col1, col2, col3 = st.columns(3)

        order = df_listing.merge(
            df_review, left_on="id", right_on="listing_id")
        order = order.groupby(['neighbourhood','room_type'])['price'].mean().to_frame('avg_price').reset_index()
        order = order.sort_values('avg_price', ascending = False)      
        with col1:
            agree = st.checkbox('Tips ')
            if agree:
                st.info('please select room type', icon="ℹ️")                  
        with col2:
            room_type = st.selectbox(
            "Select the Room Type:",
            options=order["room_type"].unique())
            
        df_selection = order.query(
            """room_type == @room_type""")
        fig = px.line(df_selection, y="avg_price", x="neighbourhood"
        , title='Price trend per neighbourhood', color='room_type')
        st.plotly_chart(fig)
        text_b = st.text_area(label=" ", value="""The chart above shows price trends from each neighborhood 
        grouped by room type. As a note,  not all neighborhoods have all room types (based on the data).""") 
st.markdown('---')


#id dan name listing apa yang mempunyai number of reviews paling banyak?Mengapa bisa terjadi demikian?(semi-adv)
c = st.container()
with c:
    st.markdown(
        """
        ##### Most review listing of Airbnb Singapore
        """)
    with st.expander(label="Show Visualization"):
        col1, col2, col3 = st.columns(3)

        ordermap = df_listing.merge(
                    df_review, left_on="id", right_on="listing_id")
        ordermap = ordermap.groupby(['id','name','room_type','neighbourhood','latitude','longitude','price'])['date'].size().to_frame('review').reset_index()
        ordermap = ordermap.sort_values('review',ascending = False)
        max_rev = ordermap[['id','name','room_type','neighbourhood','price','review']].head(10).reset_index()
        
        fig = px.bar(max_rev, y="name", x="review"
        , title='Most Review Airbnb Singapore Listings', barmode='group'
        ,hover_name='name',hover_data=['id','room_type','neighbourhood','price','review'])
        st.plotly_chart(fig)
        text_c = st.text_area(label="  ", value="The chart above shows the 10 most reviewed Airbnb Singapore listings.")
    with st.expander(label="Show Table"):
            st.dataframe(max_rev)



# Bagaimana rata-rata harga listings per neigbourhood_group?(semi-adv)
d = st.container()
with d:
    st.markdown(
        """
        ##### Airbnb Singapore average price by region
        """)
    with st.expander(label="Show Visualization"):
        col1, col2, col3 = st.columns(3)
        ordermap_region = ordermap.merge(df_region, on='neighbourhood')
        ordermap_region_avg = ordermap_region.groupby(['room_type','neighbourhood_group'])['price'].mean().to_frame('avg_price').reset_index()

        fig1 = px.bar(ordermap_region_avg, y="avg_price", x="neighbourhood_group"
            , title='Average price by room type per region', color='room_type', barmode='group')
        st.plotly_chart(fig1) 
        text_d = st.text_area(label="   ", value="""The chart above shows average price trends from each 
        region grouped by room type. As a note,  not all region have all room types (based on the data).""")
    with st.expander(label="Show Table"):
            st.dataframe(ordermap_region_avg)


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
            , title='Most Rental Activity Airbnb Singapore', barmode='group'
            ,hover_name='month_year',hover_data=['review','month_year'])
    fig.update_xaxes(tickangle=90)
    with st.expander(label="Show Visualization"):
        st.plotly_chart(fig)
        text_e = st.text_area(label="    ", value="The chart above shows month and year with the most rental activity ")
    with st.expander(label="Show Table"):
        st.dataframe(ordermap_region_sort_desc)
    
f = st.container()
with f:
    st.markdown(
        """
        ##### Least Rental Activity Airbnb Singapore
        """)
    ordermap_region_sort_asc = ordermap_region_sort.groupby(['month_year'])['date'].size().to_frame('review').reset_index()
    ordermap_region_sort_asc = ordermap_region_sort_asc.sort_values('review')
    ordermap_region_sort_asc = ordermap_region_sort_asc.head(20)
    fig = px.bar(ordermap_region_sort_desc, y="review", x="month_year"
            , title='Least Rental Activity Airbnb Singapore', barmode='group'
            ,hover_name='month_year',hover_data=['review','month_year'])
    fig.update_xaxes(tickangle=90)
    with st.expander(label="Show Visualization"):
        st.plotly_chart(fig)
        text_f = st.text_area(label="     ", value="The chart above shows month and year with the least rental activity ")
    with st.expander(label="Show Table"):
        st.dataframe(ordermap_region_sort_asc)
    




#nyoba map
map = st.container()
        
with map:
    
    st.markdown(
        """
        ##### LISTING MAP SPREAD ORDER COUNT IN THE LAST 4 YEARS
        """)



    agree = st.checkbox('Tips')
    if agree:
        st.info("""scroll mouse inside map area to zoom in or zoom out,
         hover mouse to the dot inside map area to view listing details, hold right-click mouse inside map area to pan""", icon="ℹ️")
    
    ordermap = df_listing.merge(
            df_review, left_on="id", right_on="listing_id")
    ordermap = ordermap.groupby(['neighbourhood','room_type','latitude','longitude','name','price'])['date'].size().to_frame('order').reset_index()
    rented_365_map = px.scatter_mapbox(ordermap, lat="latitude", lon="longitude", color="room_type"
    , hover_name='name',hover_data=['neighbourhood', 'order'],zoom=9, width=750)
    rented_365_map.update_layout(mapbox_style="open-street-map")
    rented_365_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(rented_365_map)


for i in range(4):
    st.write("")

st.markdown("""
    <h5 style='text-align: center; color: #1746A2;'>For more airbnb singapore listing analysis and data visualization, please visit my Friend streamlit webapp</h5>
""", unsafe_allow_html=True)

st.markdown("""
    
    [<h5 style='text-align: center; color: #5F9DF7 ;'>Adifta Airbnb Project</h5>](https://nununu-py-dqlab-final-project-main-g26t83.streamlit.app/)

""", unsafe_allow_html=True)