import streamlit as st
from src.config import *
import src.utils as utils




def write():

    ##-------- (1) GENES SEARCH
    st.subheader("Genes/Proteins Search", divider=True)
    st.markdown(
        """
        :blue[We use STRING v11 databasse - it contains 12535 ORGANISMS and 59.3 million of PROTEINS]        
        """
    )

    with st.expander("", expanded=True):

        # column view
        col1,col2,_ = st.columns([1,1,2])
        # Choose species
        with col1:
            (taxonomy_id, species) = st.selectbox(
                "Species/Organism", 
                TAXONOMY_TO_SPECIES.items(),
                key="species-1",
            )
        # Choose a gene
        with col2:
            list_all_genes = utils._get_list_genes()
            gene = st.selectbox(
                "Genes (symbol type)",
                list_all_genes,
                index=None
            )
        # Start search
        button = st.button(':blue[Search]', key="button-1")
        if button:
            st.dataframe(
                utils._get_df_mapping_genes([gene]),
                use_container_width=True
            )
