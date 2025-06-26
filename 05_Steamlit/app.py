import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

df = pd.read_excel('D:/Projects/Office/04_Excel/Negtgel_office.xlsx', sheet_name="2", header=1)




st.title("Барилга объектын мэдээлэл оруулах апп")

# Зээл хүсэгчийн нэр
customer_name = st.text_input("Зээл хүсэгчийн нэр")

# Зээлийн зориулалт
loan_purpose = st.selectbox("Зээлийн зориулалт", ["Санхүүгийн түшиг зээл", "Орон сууцны зээл", "Бизнесийн зээл"])

# Барьцаа хөрөнгийн хаяг
collateral_reg_num = st.text_input("Барьцаа хөрөнгийн улсын бүртгэлийн дугаар")

# Дүүрэг сонгох
district_options = df['Дүүрэг'].dropna().unique().tolist()
selected_district = st.selectbox("Дүүрэг сонгоно уу:", district_options)

# Хороо сонгох
filtered_df = df[df['Дүүрэг'] == selected_district]
khoroo_options = filtered_df['Хороо'].dropna().unique().tolist()
selected_khoroo = st.selectbox("Хороо сонгоно уу:", khoroo_options)

# Байрны дугаар сонгох
filtered_df2 = filtered_df[filtered_df['Хороо'] == selected_khoroo]
bair_options = filtered_df2['Байрны дугаар'].dropna().unique().tolist()
selected_bair = st.selectbox("Байрны дугаар сонгоно уу:", bair_options)

# Байрны мэдээллүүдийг харуулах, байрны давхар сонгох
matched_row = filtered_df2[
    filtered_df2['Байрны дугаар'] == selected_bair
]

if not matched_row.empty:
    row = matched_row.iloc[0]

 # Байрны үндсэн мэдээлэл box дотор
    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"**Барилгын нэр:** {row['Барилгын нэр']}  \n"
            f"**Нийт давхарын тоо:** {row['Нийт давхарын тоо']}  \n"
            f"**Ашиглалтад орсон он:** {row['Ашиглалтад орсон он']}"
        )

    with col2:
        try:
            total_floors = int(row['Нийт давхарын тоо'])
            # Эхлээд тусгай давхаруудыг жагсаалтанд нэмэх
            floor_options = ['B1 (Доод давхар)'] + list(range(1, total_floors + 1)) + ['Техникийн давхар']
            
            # Сонголт хийх
            selected_floor = st.selectbox("Оффисын давхар сонгоно уу:", floor_options)
        except:
            st.warning("Нийт давхарын тоо тодорхойгүй байна, давхар сонгох боломжгүй.")



    # OpenStreetMap үүсгэх
    m = folium.Map(location=[row['lat'], row['lon']], zoom_start=17, tiles='OpenStreetMap')
    folium.Marker(
        [row['lat'], row['lon']],
        popup=f"{row['Барилгын нэр']}<br>Нийт давхар: {row['Нийт давхарын тоо']}<br>Он: {row['Ашиглалтад орсон он']}",
        tooltip=row['Барилгын нэр'],
        icon=folium.Icon(color='red')
    ).add_to(m)

    # Streamlit дээр харуулах
    st_folium(m, width=700, height=500)

else:
    st.warning("Мэдээлэл олдсонгүй.")

# Барьцаа хөрөнгийн хаяг
col1, col2 = st.columns([3, 1])  # Баруун талд жижиг багана үүсгэв

with col1:
    area_input = st.text_input("Талбайн хэмжээ оруулна уу (м²):")

with col2:
    if area_input:
        if area_input.replace('.', '', 1).isdigit():
            area = float(area_input)
            st.success(f"Таны оруулсан талбай {area} м²")
        else:
            st.error("Зөвхөн тоон утга оруулна уу!")


# Цонхны байрлал
orientation = st.selectbox(
    "Нийт цонхны 50%-аас дээш нь урд болон баруун зүг рүү харсан уу?",
    ["Тийм", "Үгүй"]
)

# Сонголтыг харуулах
st.write(f"Таны сонголт: {orientation}")
