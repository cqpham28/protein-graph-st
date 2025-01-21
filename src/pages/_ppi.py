import streamlit as st
from src.config import *
import src.utils as utils



#################
def write():


    ##-------- (2) STRING PPI
    st.subheader("Protein-Protein Interaction (PPI)", divider=True)
    st.markdown(
        """
        :blue[We incoporate API from STRING database to plot the PPI network]        
        """
    )
    with st.expander("", expanded=True):

        # column view
        col1,col2,_ = st.columns([1,3,2])
        # Choose species
        with col1:
            (taxonomy_id, species) = st.selectbox(
                "Species/Organism", 
                TAXONOMY_TO_SPECIES.items(),
                key="species-2",
            )
        # Type a list strings, e.g., FAA4, POX1, FAT1, FAS2, FAS1, FAA1, OLE1
        with col2:
            input_genes = st.text_input(
                "List of Genes/Proteins"
            )
            if input_genes:
                list_selected_genes = utils.handle_genes(input_genes)
        # start
        button = st.button(':blue[analyze]', key="button-2")
        if button:
            utils.analyze_ppi(list_selected_genes, int(taxonomy_id))