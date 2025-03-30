import pandas
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import scipy

inflation = pd.read_excel('./inflation.xlsx',index_col='Год')
inflation = inflation.loc[[i for i in range(2000,2025)]]

xls = pd.ExcelFile('./Tab3_zpl_2024.xlsx')
zp_2017_2024 = pd.read_excel(xls,0,index_col='Вид деятельности')
zp_2000_2016 = pd.read_excel(xls,1,index_col='Вид деятельности')
st.write("Привет Алиса)")
st.write("здесь в целом не какое то ноу-хау,просто небольшая работа с данными.я взял данные с РосСтата по годовой инфляции и годовые изменения зарплат по секторам относительно нее")
st.write("Основная проблема в том,что с 2017г Росстат сильно раздробил данные на мелкие сектора,поэтому данные приходится сопоставлять вручную)")

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
zp_2017_2024 = zp_2017_2024.rename({x2:x1})
res1 = pd.concat([zp_2000_2016.loc[x1],zp_2017_2024.loc[x1]])
res1.index.names=['Год']
calculate_zp_on_inf = [res1.iloc[0]]
for i in inflation['Всего']:
    calculate_zp_on_inf.append(calculate_zp_on_inf[-1]*((100+i)/100))
calculate_zp_on_inf.pop(0)
res1 = pd.DataFrame({'Зарплата':res1,'Зарплата по инфляции':calculate_zp_on_inf})
zp_minus = res1['Зарплата'].copy()
zp_minus_inf = res1['Зарплата по инфляции'].copy()
for i in zp_minus.index[-1:0:-1]:
   zp_minus[i] = zp_minus[i]-zp_minus[i-1]
   zp_minus_inf[i] = zp_minus_inf[i] - zp_minus_inf[i-1]
zp_minus.loc[zp_minus.index[0]]=0
zp_minus_inf.loc[zp_minus_inf.index[0]]=0
res2 = pd.DataFrame({'фактический прирост к зарплате':zp_minus,'ожидаемый прирост к зарплате по инфляции':zp_minus_inf})
res2.index.names=['Год']
st.dataframe(res1)
st.dataframe(res2)
st.write('фактический и ожидаемый рост зарплаты относительно инфляции')
st.plotly_chart(px.scatter(data_frame=res1))
st.plotly_chart(px.scatter(res2))
st.write('График инфляции')
st.plotly_chart(px.scatter(inflation['Всего']))
st.write('Вывод 1: во всех секторах экономики произошел рост зарплат,в целом это указывает на равномерное развитие всех отраслей экономики')
st.write('Вывод 2:если судить поверхностно-выглядит будто инфляция напрямую влияет на рост зарплат,однако на практике -не хватает данных при отрицательном росте инфляции(дефляции)')
st.write('Вывод 3: При сравнении фактического прироста к зарплате видно что при повышении инфляции фактический прирост падает ,однако в последующие годы нагоняет и обгоняет ожидаемый прирост ')
