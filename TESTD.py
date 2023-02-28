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
import seaborn as sns

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
            st.title(" Dashboard Kinerja Pengurus" )
            st.subheader("Ormawa Eksekutif PKU IPB Kabinet Gantari Arti")   
with col2:
        # Tampilkan informasi nilai mutu
             st.image('RISBANG X INTERNAL.png', width=300)



st.markdown('------')
st.write('Dengan mengetahui performa tiap pengurus secara statistik, akan membantu Ormawa Eksekutif PKU IPB, khususnya Biro Internal dalam memonitoring kinerja tiap pengurus. Pembaharuan dashboard ini dilakukan setiap 2 bulan sekali.')
st.markdown('------')
st.subheader("Demografi Pengurus Kabinet Gantari Arti")




#-----------DATABASE KABINET------------
print("-----------DATABASE KABINET------------")
# LINK CSV
#https://docs.google.com/spreadsheets/d/19k-_Giv40KxhtykzPNLd3A86xnAa7gIEuQRjPHFrWAw/edit#gid=0
sheet_id1 = '19k-_Giv40KxhtykzPNLd3A86xnAa7gIEuQRjPHFrWAw'
dfA = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id1}/export?format=csv')



#-----------DATABASE ANTAR BIRDEPT------------
print("-----------DATABASE ANTAR BIRDEPT------------")

# LINK CSV
#https://docs.google.com/spreadsheets/d/1h7wK5Zy331sLvhN0EHwEsnZPgtcgPTQOe6GLTBxQ0JE/edit
sheet_id12 = '1h7wK5Zy331sLvhN0EHwEsnZPgtcgPTQOe6GLTBxQ0JE'
dfB = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id12}/export?format=csv',parse_dates=['DATE_1'])


# Buat fungsi untuk membuat grafik
def create_chart(df, divisi):
    fig = px.line(df, x='DATE_1', y=divisi)
    fig.update_layout(title=f'Performa {divisi}', xaxis_title='Bulan', yaxis_title='Performa')
    return fig

# Buat aplikasi Streamlit



#-----------DATABASE BEST Performance------------

print("-----------DATABASE BEST Performance------------")
#https://docs.google.com/spreadsheets/d/1UWMla9vOWPNH0cehuhmvYbmWzBWVzaAPgHr9gS4GZJg/edit#gid=0
sheet_id3 = '1UWMla9vOWPNH0cehuhmvYbmWzBWVzaAPgHr9gS4GZJg'
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
dfA['DATE_2'] = pd.to_datetime(dfA['DATE_2'].apply(lambda x: x+'/1'), format='%m/%Y/%d')
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
# Buat fungsi untuk membuat grafik

#https://docs.google.com/spreadsheets/d/1SH7ctXNUN8TIs1_1rf_dhQnj9kx-iYltR43rbS09nIw/edit?usp=sharing
sheet_id10 = '1SH7ctXNUN8TIs1_1rf_dhQnj9kx-iYltR43rbS09nIw'
dfZ = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id10}/export?format=csv')

print(dfZ)

# Sort data by month column
dfZ = dfZ.sort_values('DATE_1')

# # Sidebar for filters
# st.sidebar.header('Filter')
# selected_month = st.sidebar.selectbox('Select Month', dfZ['DATE_1'].unique())

# Tampilkan dropdown untuk memilih bulan
selected_month = st.selectbox("Pilih Bulan",dfZ['DATE_1'].unique())

# Main content
st.title('Perbandingan Kinerja BPH dan Antar Biro/Departemen')
st.write(f'Month: {selected_month}')

# Create boxplot for all divisions
df_filtered = dfZ[dfZ['DATE_1'] == selected_month]
if len(df_filtered) > 0:
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 10))
    sns.boxplot(x='BPH dan Biro/Departemen', y='Performa', data=df_filtered, ax=ax1)
    ax1.set_title(f'Boxplot Performa Kerja BPH dan Seluruh Biro/Departemen ({selected_month})')
    
  
    # Rotate x-labels for better visibility
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    
     # Distribution plot
    sns.kdeplot(data=df_filtered, x='Performa', hue='BPH dan Biro/Departemen', multiple='stack', ax=ax2)
    ax2.set_title(f'Sebaran Performa Kerja BPH dan Seluruh Biro/Departemen ({selected_month})')
    ax2.legend(loc='upper right',title='Divisi')
    
    fig.tight_layout()
    st.pyplot(fig)
   


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
st.title('Grafik Time Series Performa Biro dan Departemen')
st.markdown('''
            Grafik time series interaktif untuk menampilkan nilai Biro dan Departemen.
            ''')

# Show dropdown to select division
divisi = st.selectbox('Pilih Divisi', numeric_cols, key='option1')

# Filter data by selected division
filtered_data = dfB[['DATE_1', divisi, 'Trend']].copy()

# Show chart
st.plotly_chart(create_chart(filtered_data, divisi), use_container_width=True)

#=============================== BEST PERFORMANCE BPH SEBAGAI SC ===========================================
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

#https://docs.google.com/spreadsheets/d/1g2KHjjvTDUC4qkTwBImNWmPdUuZ0ejNIeNnvLxIFyxo/edit#gid=0
sheet_id4 = '1g2KHjjvTDUC4qkTwBImNWmPdUuZ0ejNIeNnvLxIFyxo'
df = CSV_Link_1 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id4}/export?format=csv')
print(dfC)

# Tambahkan sidebar


# Membuat sidebar
with st.sidebar:
    st.subheader("Menu Navigasi")
    menu = ["BPH sebagai SC", "Biro dan Departemen","Pimpinan","TOP 11 Staff"]
    selected_menu = st.sidebar.selectbox("Best Performance", menu) 
    # Jika menu "BPH dengan Performa Kerja Terbaik" dipilih

if selected_menu == "BPH sebagai SC":

    # Set judul halaman
    st.title("BPH dengan Performa Kerja Terbaik")



    # Path folder foto
    foto_folder = "FOTO STAFF DAN IKON/"

    # Path folder nilai mutu
    nilai_mutu_folder = "FOTO STAFF DAN IKON/"

    # Baca file CSV

    #df['C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto'] = 'Foto/' + df['Foto']
    df = df.rename(columns={'FOTO STAFF DAN IKON/': 'Path Foto'})
    # Tambahkan prefix 'Foto/' pada nilai kolom 'Foto' dan simpan hasilnya pada kolom baru 'Path Foto'
    df['Path Foto'] = 'FOTO STAFF DAN IKON/' + df['Foto']
    # Hapus kolom 'Foto' karena sudah tidak diperlukan lagi
    df = df.drop(columns=['Foto'])

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
        photo_path = row['Path Foto']
        attitude = row['Sikap']
        contribution = row['Kontribusi']
        attendance = row['Kehadiran']
        activity = row['Keaktifan']
        nilai_mutu = row['Nilai Mutu']
        foto_nilai_mutu = Image.open(nilai_mutu)
        foto_staff = Image.open(photo_path)
        
        st.subheader(name)
        display_staff_info( performance, attitude, contribution, attendance, activity, nilai_mutu, photo_path)




#=============================== BEST PERFORMANCE BIRDEPT ===========================================
def display_staff_info( performance,nilai_mutu, photo_path):
    
      # Tampilkan deskripsi staff
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
     st.image(foto_staff, width=280)

    with col2:
       # Tampilkan informasi nilai mutu
       st.image(foto_nilai_mutu, width=280)

    with col3:
        st.write("Performa: ", performance)


#https://docs.google.com/spreadsheets/d/1eNp46rCBAWo0axXG_FG6ZZorqrxDRa3PwqgmSUAhBR4/edit#gid=0
sheet_id5 = '1eNp46rCBAWo0axXG_FG6ZZorqrxDRa3PwqgmSUAhBR4'
df = CSV_Link_2 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id5}/export?format=csv')
print(dfC)



# Jika menu "BPH dengan Performa Kerja Terbaik" dipilih
if selected_menu == "Biro dan Departemen":
# Set judul halaman
    st.title("Biro dan Departemen")


    # Path folder foto
    foto_folder = "FOTO STAFF DAN IKON/"

    # Path folder nilai mutu
    nilai_mutu_folder = "FOTO STAFF DAN IKON/"

    #df['C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto'] = 'Foto/' + df['Foto']
    df = df.rename(columns={'FOTO STAFF DAN IKON/': 'Path Foto'})
    # Tambahkan prefix 'Foto/' pada nilai kolom 'Foto' dan simpan hasilnya pada kolom baru 'Path Foto'
    df['Path Foto'] = 'FOTO STAFF DAN IKON/' + df['Foto']
    # Hapus kolom 'Foto' karena sudah tidak diperlukan lagi
    df = df.drop(columns=['Foto'])

    df['Nilai Mutu'] = nilai_mutu_folder + df['Nilai Mutu'] + '.png'
    df = df.reset_index(drop=True)



    # Buat list bulan
    months = df['Bulan'].unique()

    # Tampilkan dropdown untuk memilih bulan
    selected_month = st.selectbox("Pilih Bulan", months,key="select_month_1")

    # Filter data berdasarkan bulan yang dipilih
    filtered_df = df[df['Bulan'] == selected_month]

    # Urutkan data berdasarkan nilai performa
    sorted_df = filtered_df.sort_values(by=['Performa'], ascending=False)

    print(sorted_df)

    # Tampilkan informasi staff
    for i, row in sorted_df.iterrows():
        name = row['Nama']
        performance = row['Performa']
        photo_path = row['Path Foto']
        nilai_mutu = row['Nilai Mutu']
        foto_nilai_mutu = Image.open(nilai_mutu)
        foto_staff = Image.open(photo_path)
        
        st.subheader(name)
        display_staff_info( performance, nilai_mutu, photo_path)





#=============================== BEST PERFORMANCE Pimpinan ===========================================
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

#https://docs.google.com/spreadsheets/d/18_GUDHDtBNhBddHL-2m0AYNtdepN_BFOHJULOCOv31Q/edit
sheet_id6 = '18_GUDHDtBNhBddHL-2m0AYNtdepN_BFOHJULOCOv31Q'
df = CSV_Link_3 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id6}/export?format=csv')
print(dfC)

# Jika menu "BPH dengan Performa Kerja Terbaik" dipilih
if selected_menu == "Pimpinan":

# Set judul halaman
    st.title("Pimpinan")




    # Path folder foto
    foto_folder = "FOTO STAFF DAN IKON/"

    # Path folder nilai mutu
    nilai_mutu_folder = "FOTO STAFF DAN IKON/"


    #df['C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto'] = 'Foto/' + df['Foto']
    df = df.rename(columns={'FOTO STAFF DAN IKON/': 'Path Foto'})

    # Tambahkan prefix 'Foto/' pada nilai kolom 'Foto' dan simpan hasilnya pada kolom baru 'Path Foto'
    df['Path Foto'] = 'FOTO STAFF DAN IKON/' + df['Foto']
    # Hapus kolom 'Foto' karena sudah tidak diperlukan lagi
    df = df.drop(columns=['Foto'])

    df['Nilai Mutu'] = nilai_mutu_folder + df['Nilai Mutu'] + '.png'
    df = df.reset_index(drop=True)


    # Buat list bulan
    months = df['Bulan'].unique()

    # Tampilkan dropdown untuk memilih bulan
    selected_month = st.selectbox("Pilih Bulan", months, key="select_month_2")

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
        photo_path = row['Path Foto']
        attitude = row['Sikap']
        contribution = row['Kontribusi']
        attendance = row['Kehadiran']
        activity = row['Keaktifan']
        nilai_mutu = row['Nilai Mutu']
        foto_nilai_mutu = Image.open(nilai_mutu)
        foto_staff = Image.open(photo_path)
        
        st.subheader(name)
        display_staff_info( performance, attitude, contribution, attendance, activity, nilai_mutu, photo_path)

  

#=============================== BEST PERFORMANCE STAFF ===========================================


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

       
 #https://docs.google.com/spreadsheets/d/1UWMla9vOWPNH0cehuhmvYbmWzBWVzaAPgHr9gS4GZJg/edit#gid=0
sheet_id7 = '1UWMla9vOWPNH0cehuhmvYbmWzBWVzaAPgHr9gS4GZJg'
df = CSV_Link_4 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id7}/export?format=csv')      

# Jika menu "BPH dengan Performa Kerja Terbaik" dipilih
if selected_menu == "TOP 11 Staff":
# Set judul halaman
    st.title("TOP 11 Staff")




    # Path folder foto
    foto_folder = "FOTO STAFF DAN IKON/"

    # Path folder nilai mutu
    nilai_mutu_folder = "FOTO STAFF DAN IKON/"

    #df['C:/Users/user/Documents/ST03/Project/Dashboard_Project/Eksekutif Ormawa PKU 2023-2024/Work Performances Dashboard/Foto'] = 'Foto/' + df['Foto']
    df = df.rename(columns={'FOTO STAFF DAN IKON/': 'Path Foto'})
    # st.write(df.head())
    # Tambahkan prefix 'Foto/' pada nilai kolom 'Foto' dan simpan hasilnya pada kolom baru 'Path Foto'
    df['Path Foto'] = 'FOTO STAFF DAN IKON/' + df['Foto']
    # Hapus kolom 'Foto' karena sudah tidak diperlukan lagi
    df = df.drop(columns=['Foto'])

    df['Nilai Mutu'] = nilai_mutu_folder + df['Nilai Mutu'] + '.png'
    df = df.reset_index(drop=True)



    # Buat list bulan
    months = df['Bulan'].unique()

    # Tampilkan dropdown untuk memilih bulan
    selected_month = st.selectbox("Pilih Bulan", months, key="select_month_3")

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
        photo_path = row['Path Foto']
        attitude = row['Sikap']
        contribution = row['Kontribusi']
        attendance = row['Kehadiran']
        activity = row['Keaktifan']
        nilai_mutu = row['Nilai Mutu']
        foto_nilai_mutu = Image.open(nilai_mutu)
        foto_staff = Image.open(photo_path)
        
        st.subheader(name)
        display_staff_info( performance, attitude, contribution, attendance, activity, nilai_mutu, photo_path)
