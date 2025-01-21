import omicverse as ov
import matplotlib.pyplot as plt
import pandas as pd



def analyze_ppi():


    # list_genes = ['FAA4','POX1','FAT1','FAS2','FAS1','FAA1','OLE1']
    # taxonomy_id = 4932


    
    list_genes = [
        'SORT1',
        'ITGB1BP1',
        'ADAM17',
        'EIF2AK2',
        'CEBPZOS',
        'PRKD3',
        'NCK2',
        'ICA1L'
    ]
    taxonomy_id = 9606


    gene_type_dict=dict(zip(list_genes,['Type1']*3+['Type2']*5))
    gene_color_dict=dict(zip(list_genes,['#F7828A']*3+['#9CCCA4']*5))


    ppi=ov.bulk.pyPPI(
        gene=list_genes,
        gene_type_dict=gene_type_dict,
        gene_color_dict=gene_color_dict,
        species=taxonomy_id
    )

    # connect to string-db to calculate the protein-protein interaction
    ppi.interaction_analysis()

    # plot the network
    fig,ax = ppi.plot_network()


    plt.show()



def request_kegg():

    # Define the base URL for KEGG API
    kegg_base_url = "https://rest.kegg.jp/list/disease"

    # Send the GET request to KEGG API
    response = requests.get(kegg_base_url)

    # Check for successful response
    if response.status_code == 200:
        data = response.text
        
        # Split the response into lines and parse into a list of tuples
        data_lines = [line.split('\t') for line in data.strip().split('\n')]
        
        # Create a DataFrame from the parsed data
        df = pd.DataFrame(data_lines, columns=["Disease_ID", "Disease_Name"])
        
        # Save DataFrame to CSV
        df.to_csv("kegg_disease_data.csv", index=False)
        print("Data saved to kegg_disease_data.csv")
    else:
        print(f"Error: {response.status_code}")




def string_interaction(gene:list,species:int) -> pd.DataFrame:
    r"""A Python library to analysis the protein-protein interaction network by string-db
  
    Arguments:
        gene: The gene list to analysis PPI
        species: NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).
    
    Returns:
        res: the dataframe of protein-protein interaction
    
    """
    import requests ## python -m pip install requests
    string_api_url = "https://string-db.org/api"
    output_format = "tsv-no-header"
    method = "network"
    request_url = "/".join([string_api_url, output_format, method])
    my_genes = gene

    params = {

        "identifiers" : "%0d".join(my_genes), # your protein
        "species" : species, # species NCBI identifier 
        "caller_identity" : "www.awesome_app.org" # your app name

    }
    response = requests.post(request_url, data=params)
    res=pd.DataFrame()
    res['stringId_A']=[j.strip().split("\t")[0] for j in response.text.strip().split("\n")]
    res['stringId_B']=[j.strip().split("\t")[1] for j in response.text.strip().split("\n")]
    res['preferredName_A']=[j.strip().split("\t")[2] for j in response.text.strip().split("\n")]
    res['preferredName_B']=[j.strip().split("\t")[3] for j in response.text.strip().split("\n")]
    res['ncbiTaxonId']=[j.strip().split("\t")[4] for j in response.text.strip().split("\n")]
    res['score']=[j.strip().split("\t")[5] for j in response.text.strip().split("\n")]
    res['nscore']=[j.strip().split("\t")[6] for j in response.text.strip().split("\n")]
    res['fscore']=[j.strip().split("\t")[7] for j in response.text.strip().split("\n")]
    res['pscore']=[j.strip().split("\t")[8] for j in response.text.strip().split("\n")]
    res['ascore']=[j.strip().split("\t")[9] for j in response.text.strip().split("\n")]
    res['escore']=[j.strip().split("\t")[10] for j in response.text.strip().split("\n")]
    res['dscore']=[j.strip().split("\t")[11] for j in response.text.strip().split("\n")]
    res['tscore']=[j.strip().split("\t")[12] for j in response.text.strip().split("\n")]
    return res




####
if __name__ == "__main__":

    # analyze_ppi()
    # request_kegg()

    # res = string_interaction(gene=['SORT1'],species=9606)
    res = string_interaction(gene=['EIF2AK2'],species=9606)
    print(res)