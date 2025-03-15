import pandas as pd
import streamlit as st

inflation = pd.read_excel('./inflation.xlsx')
inflation_2000_2016 = inflation[inflation['Год']<=2016]
inflation_2000_2016 = inflation_2000_2016[inflation_2000_2016['од']>=2000]
inflation_2017_2024 = inflation[inflation['Год']>2016]

xls = pd.ExcelFile('./Tab3_zpl_2024.xlsx')
zp_2017_2024 = pd.read_excel(xls,0)
zp_2000_2016 = pd.read_excel(xls,1)

st.write('инфляция по годам')
st.dataframe(inflation)

v1 = ['с 2000 по 2016','с 2017 по 2025']
x1 = st.pills('Выберите года: либо с 2000 по 2016,либо с 2017 по 2025',options=v1,selection_mode='single',default=v1[0])
if x1==v1[0]:
    zp = zp_2000_2016
    inf = inflation_2000_2016
else:
    zp = zp_2017_2024
    inf = inflation_2017_2024
st.dataframe(zp)
st.dataframe(inf)
