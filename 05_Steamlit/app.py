import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

df = pd.read_excel('05_Steamlit/Negtgel_office.xlsx', sheet_name="2", header=1)

st.title("Барилга объектын мэдээлэл оруулах апп")

# Зээл хүсэгчийн нэр
customer_name = st.text_input("Зээл хүсэгчийн нэр")

# Зээлийн зориулалт
loan_purpose = st.selectbox("Зээлийн зориулалт", ["Бизнесийн зээл", "Санхүүгийн түшиг зээл", "Шуурхай үээл"])

if loan_purpose == "Бизнесийн зээл":
    loan_purpose_value = 0.7
elif loan_purpose == "Санхүүгийн түшиг зээл":
    loan_purpose_value = 0.5
elif loan_purpose == "Шуурхай үээл":
    loan_purpose_value = 0.5
else:
    loan_purpose_value = 1


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

# ТАЛБАЙН ХЭМЖЭЭГ ГАРААС ОРУУЛАХ
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

# Засвар хийх шаардлагатай эсэх
zaswar = st.selectbox(
    "Засвар үйлчилгээ хийх шаардлагатай эсэх ?",
    ["Үгүй", "Тийм"]
)

zaswar_value = 0.95 if zaswar == "Тийм" else 1
#st.write("Засварын утга:", zaswar_value)


#ЦОНХНЫ ТОХИРУУЛГА
col1, col2 = st.columns([2.5, 1.5])

with col1:
# Цонхны байрлал
    orientation = st.selectbox(
        "Нийт цонхны 50%-аас дээш нь урд болон баруун зүг рүү харсан уу?",
        [ "Тийм", "Үгүй"]
    )

    orientation_value = 1 if orientation == "Тийм" else 0.95
    #st.write("Засварын утга:", orientation_value)

with col2:
# Цонх хаагдсан эсэх
    orchin = st.selectbox(
        "Үзэгдэх орчин хязгаарлагдсан эсэх",
        ["Үгүй", "Нийт цонхны 25% таглагдсан", "Нийт цонхны 50% таглагдсан", "Нийт цонхны 75% таглагдсан", "Нийт цонхны 100% таглагдсан"]
    )

    if orchin == "Үгүй":
        orchin_value = 1
    elif orchin == "Нийт цонхны 25% таглагдсан":
        orchin_value = 0.9
    elif orchin == "Нийт цонхны 50% таглагдсан":
        orchin_value = 0.8
    elif orchin == "Нийт цонхны 75% таглагдсан":
        orchin_value = 0.7
    elif orchin == "Нийт цонхны 100% таглагдсан":
        orchin_value = 0.5
    else:
        orchin_value = 1  # Default утга

    #st.write("Очины үнэлгээ:", orchin_value)

# ТОХИРСОН ҮНЭЛГЭЭГ АВАХ
matched_row = df[
    (df['Дүүрэг'] == selected_district) &
    (df['Хороо'] == selected_khoroo) &
    (df['Байрны дугаар'] == selected_bair)
]

if not matched_row.empty:
    base_price = matched_row.iloc[0]['Үнэлгээ']
    
    # --- 5. Эцсийн үнэлгээ тооцох ---
    mkw = base_price * zaswar_value * orientation_value * orchin_value

    # --- 6. Үр дүн харуулах ---
    st.success(f"Оффиссын 1м2 талбай суурь үнэлгээ: {mkw:,.0f} ₮")
else:
    st.warning("⚠️ Сонгосон мэдээлэлд тохирох үнэлгээ олдсонгүй.")


if area_input:
    try:
        area = float(area_input)
        final_price = area * mkw
        st.success(f"Оффисын нийт үнэлгээ: {final_price:,.0f} ₮")

        zzdu = final_price * loan_purpose_value
        st.info(f"Зээл зөвшөөрөх дээд үнэ: {zzdu:,.0f} ₮")

    except ValueError:
        st.error("📏 Талбайн хэмжээг зөв оруулна уу (тоо хэлбэрээр).")
else:
    st.warning("📏 Талбайн хэмжээг оруулна уу.")