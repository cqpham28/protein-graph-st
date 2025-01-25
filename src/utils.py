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

from typing import List
import os
import pandas as pd
import streamlit as st
import omicverse as ov
from Bio import Entrez, Medline
# from pyspark.sql import SparkSession
# from datasketch import MinHash, MinHashLSH
# import re
from collections import defaultdict
import boto3



#################
# @st.cache_data
def init_s3() -> None:
    """Initialize AWS S3 storage bucket, add to st.session_state"""

    with st.spinner(f'Connect S3...'):
        # boto3
        session = boto3.Session(
            aws_access_key_id = st.secrets.aws["AWS_ACCESS_KEY_ID"], 
            aws_secret_access_key = st.secrets.aws["AWS_SECRET_ACCESS_KEY"]
        )
        if "aws" not in st.session_state:
            st.session_state.aws = {
                "s3": session.resource("s3"), 
                # "bucket": session.resource("s3").Bucket(st.secrets.aws["BUCKET_NAME"]), 
                "s3_client": session.client("s3")
            }


#################
def analyze_ppi(
    list_genes:List[str],
    taxonomy_id:int,
):
    """Function omicverse API for protein-protein-interaction analysis by string-db

    Args:
        list_genes:
        taxonomy_id:
    
    Returns:
        fig:
    """

    gene_type_dict=dict(zip(list_genes,['type']*len(list_genes)))
    gene_color_dict=dict(zip(list_genes,['#F7828A']*len(list_genes)))
    # gene_type_dict=dict(zip(list_genes,['Type1']*3+['Type2']*4))
    # gene_color_dict=dict(zip(list_genes,['#F7828A']*3+['#9CCCA4']*4))

    ppi=ov.bulk.pyPPI(
        gene=list_genes,
        gene_type_dict=gene_type_dict,
        gene_color_dict=gene_color_dict,
        species=taxonomy_id,
        # score=0.7,
    )

    # connect to string-db to calculate the protein-protein interaction
    try:
        ppi.interaction_analysis()

        # show results
        _c1, _c2 = st.columns(2)
        with _c1:
            # plot the network
            fig, ax = ppi.plot_network(
                node_alpha=0.8,
                node_linewidths=2,
                legend_fontsize=14,
            )
            fig.set_dpi(200)
            st.pyplot(fig)
            # st.plotly_chart(fig)
            # html_str = mpld3.fig_to_html(fig)
            # components.html(html_str, height=800)

            # path = "refs/network.png"
            # fig.savefig(path)
            # img = Image.open(path)
            # st.image(img, use_column_width=True)

        with _c2:
            df = ov.bulk.string_interaction(list_genes, taxonomy_id)
            st.write("Protein-Protein Interaction (sorted by STRING confidence)")
            st.dataframe(
                df.iloc[:,2:6].sort_values(by=['score'], ascending=False),
                use_container_width=True
            )

    except:
        st.warning("No interaction was found!")



#################
@st.cache_data
def _get_list_human_diseases():
    df = pd.read_csv("refs/kegg_disease_data.csv", delimiter=",")
    return df['Disease_Name'].to_list()



#################
@st.cache_data
def _get_df_human_protein():
    return pd.read_csv(
        "refs/9606_human_protein.info.txt", 
        sep='\t', 
        on_bad_lines='skip'
    ) 

@st.cache_data
def _get_list_genes():
    df = _get_df_human_protein()
    return df['preferred_name'].to_list()


def _get_df_mapping_genes(list_genes:List[str]):
    df = _get_df_human_protein()
    return df[df['preferred_name'].isin(list_genes)]



#################
def _check_valid_genes(genes:str) -> None:
    """
    """
    pass


def handle_genes(
    input_genes:List[str]
) -> List[str]:
    """
    
    """
    if "," in input_genes:
        list_genes = [g.strip() for g in input_genes.split(",")]
        flag = [_check_valid_genes(g) for g in list_genes]

    return list_genes



#################
def matching_papers_with_gene(
    disease_name:str,
    gene_list:List[str],
) -> None:
    """
    """
    # Fetch PubMed papers
    papers = _fetch_papers(
        query=f"{disease_name} AND gene", 
        retmax=100
    )

    # Convert papers to a pandas DataFrame
    data = []
    for paper in papers:
        data.append({
            "Title": paper.get("TI", "No Title"),
            "Publication Date": paper.get("DP", "No Date"),
            "Authors": ", ".join(paper.get("AU", [])) if "AU" in paper else "No Authors",
        })
    df = pd.DataFrame(data).sort_values(by="Publication Date", ascending=False)


    # Matching
    def preprocess(text):
        """lowercasing and splitting into words."""
        return set(text.lower().split())

    matches = defaultdict(list)
    
    # Preprocess gene names into sets of words
    gene_sets = {gene: preprocess(gene) for gene in gene_list}
    
    # Loop over paper titles and check for intersection with gene names
    paper_titles = df['Title'].to_list()
    for title in paper_titles:
        processed_title = preprocess(title)
        for gene, gene_set in gene_sets.items():
            # Check for intersection between the processed title and gene set
            if processed_title & gene_set:  # If there is any intersection
                matches[gene].append(title)

    matches = dict(matches)


    # Flatten the matches dictionary and associate genes with titles
    matched_rows = []
    for gene, titles in matches.items():
        for title in titles:
            matched_rows.append((gene, title))

    # Create a DataFrame with the matched rows, adding the 'Gene' column
    matched_df = pd.DataFrame(matched_rows, columns=['Gene', 'Title'])

    # Merge the matched DataFrame with the original DataFrame to include additional details
    result_df = pd.merge(matched_df, df, on='Title', how='left')

    return result_df





#################
def _fetch_papers(query:str, retmax:int):
    """Fetches paper titles related to a disease from PubMed.
    
    Args:
        query (str): the search query 
        retmax (int): # UIDs from the retrieved set in output 

    Returns:
        records
    """

    Entrez.email = 'your_email@example.com'

    handle = Entrez.esearch(
        db="pubmed", 
        term=query, 
        retmax=retmax, 
        sort='relevance', 
        retmode='text'
    )
    record = Entrez.read(handle)

    # Fetch the details of the papers
    ids = record['IdList']
    handle = Entrez.efetch(
        db="pubmed",
        id=ids,
        retmode="text",
        rettype="medline", # "abstract"
    )
    records = Medline.parse(handle)

    return records