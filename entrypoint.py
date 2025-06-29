import streamlit as st

pg = st.navigation(['app.py', 'pages/bibliometron.py', 'pages/by_request.py'])
pg.run()
