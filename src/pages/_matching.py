import streamlit as st
from src.config import *
import src.utils as utils



#################
def write():


    ##-------- (3) HUMAN DISEASES
    st.subheader("Genes/Proteins with Human Diseases", divider=True)
    st.markdown(
        """
        :blue[We obtain list of relevant articles with Disease & Genes, by the following:]        
        :blue[1) Fetch the disease database from KEGG (Kyoto Encyclopedia of Genes and Genomes)]              
        :blue[2) Fetch 100 PubMed recent papers which is relevant (titles/abstracts) with the selected disease.]        
        :blue[3) Perform keyword matching with the genes/protein database (STRING)]        
        """
    )
    with st.expander("", expanded=True):

        # column view
        col1,col2,_ = st.columns([2,2,1])
        # Type a disease
        with col1:
            list_diseases = utils._get_list_human_diseases()
            input_disease = st.selectbox(
                "Disease (from KEGG)",
                list_diseases,
                index=None
            )

        # list of prioritized genes
        # e.g., SORT1, ITGB1BP1, ADAM17, EIF2AK2, CEBPZOS, PRKD3, NCK2, ICA1L
        # with col2:
        #     input_genes = st.text_input(
        #         "Prioriztied genes/proteins"
        #     )
        #     if input_genes:
        #         list_selected_genes = utils.handle_genes(input_genes)
        # start
        button = st.button(':blue[Text Mining]', key="button-3")
        if button:
            list_all_genes = utils._get_list_genes()
            df_matches = utils.matching_papers_with_gene(
                "Alzheimer", list_all_genes)

            st.success(":blue[Recent PubMed Papers with specific genes/proteins found]")
            st.dataframe(df_matches)