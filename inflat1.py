import pandas as pd
import streamlit as st
import plotly.express as px

inflation = pd.read_excel('./inflation.xlsx',index_col='Год')
inflation = inflation.loc[[i for i in range(2000,2025)]]

xls = pd.ExcelFile('./Tab3_zpl_2024.xlsx')
zp_2017_2024 = pd.read_excel(xls,0,index_col='Вид деятельности')
zp_2000_2016 = pd.read_excel(xls,1,index_col='Вид деятельности')
st.write("Привет Алиса)")
st.write("здесь в целом не какое то ноу-хау,просто небольшая работа с данными.я взял данные с РосСтата по годовой инфляции и годовые изменения зарплат по секторам относительно нее")
st.write("Оснвная проблема что с 2017г Росстат сильно раздробил данные на мелкие сектора,поэтому данные приходится сопоставлять вручную)")

st.write('инфляция по годам в %')
st.dataframe(inflation)
v1 = ['с 2000 по 2016','с 2017 по 2024']
st.write('Уровень средней зарплаты по секторам')
x1 = st.pills('Выберите года: либо с 2000 по 2016,либо с 2017 по 2024',options=v1,selection_mode='single',default=v1[0])
if x1==v1[0]:
    zp = zp_2000_2016
else:
    zp = zp_2017_2024
st.dataframe(zp)
st.write('вывести полную информацию по конкретному сектору с 2000 по 2024 год')
st.write('Выберите совмещаемые столбцы')
vid = 'Вид деятельности'

x1 =  st.selectbox('Сопоставьте совмещаемые сектора по названию,здесь выбираются данные с 2000 по 2016г',options=zp_2000_2016.index)
x2 = st.selectbox('Сопоставьте совмещаемые сектора по названию,здесь выбираются данные с 2017 по 2024г',options=zp_2017_2024.index)
res1 = pd.concat([zp_2000_2016.loc[x1],zp_2017_2024.loc[x2]])
st.write('Фактический рост зарплаты')
st.plotly_chart(px.scatter(res1))
st.write('ожидаемый рост зарплаты относительно инфляции')
calculate_zp_on_inf = [res1.iloc[0]]
st.write(calculate_zp_on_inf[0])
for i in inflation['Всего']:
    calculate_zp_on_inf.append(calculate_zp_on_inf[-1]*((100+i)/100))
st.plotly_chart(px.scatter(calculate_zp_on_inf))
st.plotly_chart(px.scatter(inflation['Всего']))