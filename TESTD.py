import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl as ox
from PIL import Image
import altair as alt
import requests
import json
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
import plotly.graph_objs as go
import datetime
import os
import matplotlib.pyplot as plt
import base64

#Mendefinisikan fungsi untuk menampilkan animasi Lottie
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Mendefinisikan URL animasi Lottie yang akan ditampilkan
url = "https://assets5.lottiefiles.com/packages/lf20_m2aybuxx.json"

# Menampilkan animasi Lottie di tampilan utama Streamlit
st_lottie(load_lottie_url(url))

col1, col2= st.columns([2,1])
with col1:
            st.title(" Dashboard Performa Kerja Staff" )
            st.subheader("Ormawa Eksekutif PKU IPB Kabinet Gantari Arti")   
with col2:
        # Tampilkan informasi nilai mutu
             st.image('RISBANG X INTERNAL.png', width=340)



st.markdown('------')
st.write('Dengan mengetahui performa tiap staf secara statistik, akan membantu Ormawa Eksekutif PKU IPB, khususnya Biro Internal dalam memonitoring kinerja tiap staf. Pembaharuan dashboard ini dilakukan setiap 2 bulan sekali.')
st.markdown('------')
st.subheader("Demografi Staff")




#-----------DATABASE KABINET------------
print("-----------DATABASE KABINET------------")
#https://docs.google.com/spreadsheets/d/1zD_tz_u73IzIj3HbMJxkDg5Ea7qDc99Is9mgY3aKlXU/edit#gid=0
# Path file excel
excel_path1 = "DATA/Model Database Kabinet.xlsx"
#sheet_id1 = '1zD_tz_u73IzIj3HbMJxkDg5Ea7qDc99Is9mgY3aKlXU'
dfA = pd.read_excel(excel_path1)
print(dfA)



#-----------DATABASE ANTAR BIRDEPT------------
print("-----------DATABASE ANTAR BIRDEPT------------")
#https://docs.google.com/spreadsheets/d/1EVYwc62ZlxDwPL1zNOgXu47sKlJtI1-UbhnbN2p-l9A/edit#gid=0
excel_path2 = "DATA/Database Antar BirDept.xlsx"
#sheet_id2 = '1EVYwc62ZlxDwPL1zNOgXu47sKlJtI1-UbhnbN2p-l9A'
dfB = pd.read_excel(excel_path2, parse_dates=['DATE_1'])

# Baca data dari file CSV
#data = pd.read_csv('data.csv', parse_dates=['Bulan'])

# Buat fungsi untuk membuat grafik
def create_chart(df, divisi):
    fig = px.line(df, x='DATE_1', y=divisi)
    fig.update_layout(title=f'Performa {divisi}', xaxis_title='Bulan', yaxis_title='Performa')
    return fig

# Buat aplikasi Streamlit



#-----------DATABASE BEST Performance------------

print("-----------DATABASE BEST Performance------------")
#https://docs.google.com/spreadsheets/d/1-Q6YNsNFB3JOEwQlUmfHqYKGoNplS2LJN8MO7_QcaCg/edit#gid=0
sheet_id3 = '1-Q6YNsNFB3JOEwQlUmfHqYKGoNplS2LJN8MO7_QcaCg'
dfC = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id3}/export?format=csv')
print(dfC)


#-----------DATABASE DEMOGRAFI STAFF------------
print("-----------DATABASE DEMOGRAFI STAFF------------")

print("-----------Fakultas------------")
dfD= pd.read_excel(
    io='Model Database Demografi.xlsx',
    engine='openpyxl',
    sheet_name='Fakultas',
    usecols='A:B',)
names = dfD['Fakultas'].apply(str)
values = dfD['Frekuensi_Fa'].apply(int)

fig1= px.pie(dfD, values= values, 
names= names, 
title= 'Based on Faculty')
print(dfD)

print("-----------Gender------------")
dfE= pd.read_excel(
    io='Model Database Demografi.xlsx',
    engine='openpyxl',
    sheet_name='Gender',
    usecols='A:B',)

names = dfE['Gender'].apply(str)
values = dfE['Frekuensi_Ge'].apply(int)

fig3= px.pie(dfE, values= values, 
names= names, 
title= 'Based on Gender')
print(dfE)

print("-----------Birdept------------")
dfF= pd.read_excel(
    io='Model Database Demografi.xlsx',
    engine='openpyxl',
    sheet_name='BIRDEPT',
    usecols='A:B',)
names = dfF['Divisi'].apply(str)
values = dfF['Frekuensi_Di'].apply(int)

fig2= px.pie(dfF, values= values, 
names= names, 
title= 'Based on Birdept')

print(dfF)


left_column, middle_column, Right_Column = st.columns([4,4,4])
left_column.plotly_chart(fig3, use_container_width=True)
middle_column.plotly_chart(fig2,use_container_width=True)
Right_Column.plotly_chart(fig1,use_container_width=True)

st.markdown('------')
st.subheader("Hasil Analisis")

#=============================== HASIL ANALISIS ===========================================
dfA['DATE_2'] = pd.to_datetime(dfA['DATE_2'], format='%Y-%m-%d')
# Compute percentage increase in performance
current_month = dfA['DATE_2'].max()
current_performance = dfA[dfA['DATE_2'] == current_month]['GANTARI ARTI'].values[0]
previous_month = dfA[dfA['DATE_2'] < current_month]['DATE_2'].max()
previous_performance = dfA[dfA['DATE_2'] == previous_month]['GANTARI ARTI'].values[0]
percentage_increase = round((current_performance - previous_performance) / previous_performance * 100, 2)

# Determine icon based on percentage increase
icon_file = ''
if percentage_increase > 0:
    icon_file = 'naik.png'
elif percentage_increase < 0:
    icon_file = 'turun.png'
else:
    icon_file = 'tetap.png'

# Define function to create chart
def create_chart(df):
    fig = px.line(df, x='DATE_2', y='GANTARI ARTI')
    fig.update_layout(title='Performa Kabinet Gantari Arti', xaxis_title='Bulan', yaxis_title='Performa')

    # Add icon and percentage increase to the right of the chart
    icon_path = os.path.join(os.path.dirname(__file__), icon_file)
    icon_html = f'<img src="data:image/png;base64,{base64.b64encode(open(icon_path, "rb").read()).decode()}" height="25"/>'
    st.markdown(f'<div style="text-align:right">{icon_html} {percentage_increase}%</div>', unsafe_allow_html=True)

    return fig

# Create Streamlit app
st.title('Grafik Time Series Performa Kabinet Gantari Arti')
st.markdown('''
            Grafik time series interaktif untuk menampilkan nilai performa Kabinet Gantari Arti.
            ''')

# Show chart
st.plotly_chart(create_chart(dfA), use_container_width=True)


#=============================== PERBANDINGAN KINERJA ANTAR BIRDEPT ===========================================
data = {
    'Nama Staff': ['John', 'Sarah', 'Mike', 'Lisa', 'David', 'Mia', 'Oliver', 'Emily', 'Ryan', 'Sophie'],
    'Divisi': ['Sales', 'Marketing', 'IT', 'Finance', 'Sales', 'Marketing', 'IT', 'Finance', 'Sales', 'Marketing'],
    'Bulan': ['Januari', 'Januari', 'Februari', 'Februari', 'Maret', 'Maret', 'April', 'April', 'Mei', 'Mei'],
    'Nilai Performa': [70, 80, 75, 85, 65, 90, 80, 75, 70, 85]
}

df = pd.DataFrame(data)
def boxplot_divisi(df):
    # Buat selectbox untuk memilih divisi
    divisi = st.selectbox('Pilih Divisi', df['Divisi'].unique())

    # Buat selectbox untuk memilih bulan
    bulan = st.selectbox('Pilih Bulan', df['Bulan'].unique())

    # Filter data berdasarkan divisi dan bulan yang dipilih
    df_filter = df[(df['Divisi'] == divisi) & (df['Bulan'] == bulan)]

    # Buat grafik box plot
    fig, ax = plt.subplots()
    ax.boxplot(df_filter['Nilai Performa'])
    ax.set_title('Performa Kerja Divisi {} di Bulan {}'.format(divisi, bulan))
    ax.set_ylabel('Nilai Performa')
    st.pyplot(fig)
boxplot_divisi(df)





# Buat fungsi untuk membuat grafik
def create_chart(dfB):
    fig = go.Figure()
    
    for col in dfB.columns[1:]:
        fig.add_trace(go.Scatter(x=dfB['DATE_1'], y=dfB[col], mode='lines', name=col))
        
    fig.update_layout(title='Perbandingan Performa Kerja Antar Birdept', xaxis_title='Bulan', yaxis_title='Performa')
    return fig

# Buat aplikasi Streamlit
st.title('Grafik Perbandingan Performa Kerja Antar Birdept')
st.markdown('''
            Grafik interaktif yang membandingkan performa kerja antar Birdept.
            ''')

# Tampilkan grafik
st.plotly_chart(create_chart(dfB), use_container_width=True)

 #=============================== KINERJA Tiap BIRDEPT ===========================================

# Convert DATE_1 column to datetime
dfB['DATE_1'] = pd.to_datetime(dfB['DATE_1'], format='%Y-%m-%d')

# Remove commas from numeric columns
numeric_cols = dfB.columns[1:-1]
dfB[numeric_cols] = dfB[numeric_cols].replace(',', '', regex=True).astype(float)

# Compute trend
dfB['Trend'] = dfB[numeric_cols].mean(axis=1).diff().apply(lambda x: 'naik' if x > 0 else ('turun' if x < 0 else 'tetap'))

# Define function to create chart
def create_chart(df, divisi):
    fig = px.line(df, x='DATE_1', y=divisi)
    fig.update_layout(title=f'Performa {divisi}', xaxis_title='Bulan', yaxis_title='Performa')

    # Compute percentage increase in performance
    current_month = df['DATE_1'].max()
    current_performance = df[df['DATE_1'] == current_month][divisi].values[0]
    previous_month = df[df['DATE_1'] < current_month]['DATE_1'].max()
    previous_performance = df[df['DATE_1'] == previous_month][divisi].values[0]
    percentage_increase = round((current_performance - previous_performance) / previous_performance * 100, 2)

    # Determine icon based on percentage increase
    icon_file = ''
    if percentage_increase > 0:
        icon_file = 'naik.png'
    elif percentage_increase < 0:
        icon_file = 'turun.png'
    else:
        icon_file = 'tetap.png'

    # Add icon and percentage increase to the right of the chart
    icon_path = os.path.join(os.path.dirname(__file__), icon_file)
    icon_html = f'<img src="data:image/png;base64,{base64.b64encode(open(icon_path, "rb").read()).decode()}" height="25"/>'
    st.markdown(f'<div style="text-align:right">{icon_html} {percentage_increase}%</div>', unsafe_allow_html=True)

    return fig

# Create Streamlit app
st.title('Grafik Time Series Performa Kabinet Gantari Arti')
st.markdown('''
            Grafik time series interaktif untuk menampilkan nilai performa Kabinet Gantari Arti.
            ''')

# Show dropdown to select division
divisi = st.selectbox('Pilih Divisi', numeric_cols, key='option1')

# Filter data by selected division
filtered_data = dfB[['DATE_1', divisi, 'Trend']].copy()

# Show chart
st.plotly_chart(create_chart(filtered_data, divisi), use_container_width=True)


#=============================== BEST PERFORMANCE WORKERS ===========================================


def display_staff_info( performance, attitude, contribution, attendance, activity, nilai_mutu, photo_path):
    
      # Tampilkan deskripsi staff
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
     st.image(foto_staff, width=280)

    with col2:
       # Tampilkan informasi nilai mutu
       st.image(foto_nilai_mutu, width=280)

    with col3:
        st.write("Performa: ", performance)

         # Tampilkan nilai sikap
        st.image("attitude_logo.png", width=50)
        st.write("Sikap: ", attitude)

        # Tampilkan nilai kontribusi
        st.image("contribution_logo.png", width=50)
        st.write("Kontribusi: ", contribution)

        # Tampilkan nilai kehadiran
        st.image("attendance_logo.png", width=50)
        st.write("Kehadiran: ", attendance)

        # Tampilkan nilai keaktifan
        st.image("activity_logo.png", width=50)
        st.write("Keaktifan: ", activity)

       
       


# Set judul halaman
st.title(" TOP 11 Staffs with Best Work Performance of The Month")

# Path file excel
excel_path = "DATA/TESTC.xlsx"
# Path folder foto
foto_folder = ""
# Path folder foto kelompok staff
poto_folder = {
    'Risbang': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/Risbang/",
    'Medbrand': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/Medbrand/",
    'SLH': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/SLH/",
    'Adkesmah': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/Adkesmah/",
    'PSDM': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/PSDM/",
    'Bismit': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/Bismit",
    'Internal': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/Internal/",
    'BPH': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/BPH/",
    'Peraga': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/Peraga/",
    'Senbud': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/Senbud/",
    'Kastrat': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/Kastrat",
    'Akpres': "C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto/Akpres/",

}
# Path folder nilai mutu
nilai_mutu_folder = ""

# Baca file excel
df = pd.read_excel(excel_path)
df['Foto'] = 'Foto/' + df['Foto']
df['Nilai Mutu'] = nilai_mutu_folder + df['Nilai Mutu'] + '.png'
df = df.reset_index(drop=True)


# Buat list bulan
months = df['Bulan'].unique()

# Tampilkan dropdown untuk memilih bulan
selected_month = st.selectbox("Pilih Bulan", months)

# Filter data berdasarkan bulan yang dipilih
filtered_df = df[df['Bulan'] == selected_month]

# Urutkan data berdasarkan nilai performa
sorted_df = filtered_df.sort_values(by=['Performa'], ascending=False)

print(sorted_df)

# Tampilkan informasi staff
for i, row in sorted_df.iterrows():
    name = row['Nama']
    division = row['Divisi']
    performance = row['Performa']
    photo_path = foto_folder + row['Foto']
    attitude = row['Sikap']
    contribution = row['Kontribusi']
    attendance = row['Kehadiran']
    activity = row['Keaktifan']
    nilai_mutu = row['Nilai Mutu']
    foto_nilai_mutu = Image.open(nilai_mutu)
    foto_staff = Image.open(photo_path)
    
    st.subheader(name)
    display_staff_info( performance, attitude, contribution, attendance, activity, nilai_mutu, photo_path)

  
