"""
HOME PAGE


##################
Authors: Cuong Pham
Email: cuongquocpham151@gmail.com

"""
import streamlit as st
from src.config import *
import src.utils as utils



#################
def write():

    # TITLE
    st.header(":red[Genes/Protein Platform for Students (ver 1.0)]")
    st.info(
        "This is an ongoing project for Data Mining course (COMP5110). \
        Author: Cuong Pham"
    )

    # INIT AWS S3
    utils.init_s3()
    st.success(
        "Bucket Initiated ([access link](%s))" % st.secrets.aws["S3_URL"]
    )
    st.write(st.session_state.aws)