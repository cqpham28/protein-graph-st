"""
MIT License

Copyright (c) 2025 Cuong Pham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

##################
Authors: Cuong Pham
Email: cuongquocpham151@gmail.com

"""
import os
import streamlit as st
from src.pages import _home, _search, _ppi, _matching, _node



#################
st.set_page_config(
    page_title="app",
    layout="wide",
)

PAGES = {
    "Home": _home,
    "Genes Search": _search,
    "PPI": _ppi,
    "Genes-Disease": _matching,
    "Data Node Property": _node,
}


#################
def main():

    selection = st.sidebar.radio(
        "Select pages", 
        list(PAGES.keys())
    )
    os.makedirs("refs", exist_ok=True)
    
    page = PAGES[selection]
    with st.spinner(f"Loading {selection} ..."):
        page.write()



#################
if __name__ == "__main__":
    main()