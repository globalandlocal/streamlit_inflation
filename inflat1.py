simport pandas as pd
import streamlit as st
import plotly.express as px

inflation = pd.read_excel('./inflation.xlsx',index_col='Год')
inflation_2000_2016 = inflation.loc[[i for i in range(2000,2017)]]
inflation_2017_2024 = inflation.loc[[i for i in range(2017,2025)]]

xls = pd.ExcelFile('./Tab3_zpl_2024.xlsx')
zp_2017_2024 = pd.read_excel(xls,0,index_col='Вид деятельности')
zp_2000_2016 = pd.read_excel(xls,1,index_col='Вид деятельности')

st.write('инфляция по годам')
st.dataframe(inflation)
v1 = ['с 2000 по 2016','с 2017 по 2024']
st.write('Уровень средней зарплаты по секторам')
x1 = st.pills('Выберите года: либо с 2000 по 2016,либо с 2017 по 2024',options=v1,selection_mode='single',default=v1[0])
if x1==v1[0]:
    zp = zp_2000_2016
    inf = inflation_2000_2016
else:
    zp = zp_2017_2024
    inf = inflation_2017_2024
st.dataframe(zp)
st.dataframe(inf)
st.write('вывести полную информацию по конкретному сектору с 2000 по 2024 год')
st.write('Выберите совмещаемые столбцы')
vid = 'Вид деятельности'

x1 = st.pills('Сопоставьте совмещаемые сектора',options=zp_2000_2016.index,selection_mode='single',default=zp_2000_2016.index[0])
x2 = st.pills(label='1',label_visibility='hidden',options=zp_2017_2024.index,selection_mode='single',default=zp_2017_2024.index[0])
res1 = pd.concat([zp_2000_2016.loc[x1],zp_2017_2024.loc[x2]])
res2 = pd.concat([inflation_2000_2016,inflation_2017_2024])
st.plotly_chart(px.scatter(res1))
st.plotly_chart(px.scatter(res2['Всего']))
