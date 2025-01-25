"""
NODE PROPERTY PAGE


##################
Authors: Cuong Pham
Email: cuongquocpham151@gmail.com

"""
import streamlit as st
from src.config import *
import src.utils as utils



#################
def write():

    ##-------- (4) NODES PROPERTY
    st.subheader("Protein Functions Clustering", divider=True)
    st.markdown(
        """
        'ogbn-proteins' dataset: Nodes represent proteins (from 8 species), and edges indicate different types of biologically meaningful associations between proteins.
        There are 112 kinds of labels to predict the presence of protein functions in a multi-label binary classification setup.         
        :blue[In order to extract insights about protein functions related to disease-specific genes, we perform the a clustering procedure as follows:]                
        :blue[1) Select disease-specific prioritized genes from an high-quality GWAS study.]                
        :blue[2) Extract nodes (proteins) representing human (homo sapiens) protein functions from the obgn-proteins]                
        :blue[3) Perform K-mean clustering on this data, with the inital cluster those with the prioritized genes]                
        :blue[4) Perform Dimensionality Reduction for Visualization]                
        """
    )
    with st.expander("We chose 8 prioritized AD-related genes from this study: :green[Bellenguez et al (2022). New insights into the genetic etiology of Alzheimer’s disease and related dementias. Nature genetics]", expanded=True):
        # column view
        col1,col2,_ = st.columns([2,2,2])
  
        # Type a list strings, e.g., FAA4, POX1, FAT1, FAS2, FAS1, FAA1, OLE1
        with col1:
            input_genes = st.text_input(
                "Prioritized Genes (evidence-based GWAS study)"
            )
            if input_genes:
                list_selected_genes = utils.handle_genes(input_genes)

        button = st.button(':blue[Start]', key="3")
        if button:
            st.image("refs/tsne.png")