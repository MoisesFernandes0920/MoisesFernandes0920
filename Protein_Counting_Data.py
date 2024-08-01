import requests
import gzip
import shutil
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Step 1: Retrieve and unzip the file
def download_and_unzip(url, output_filename):
    response = requests.get(url, stream=True)
    with open(output_filename + '.gz', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    with gzip.open(output_filename + '.gz', 'rb') as f_in:
        
        with open(output_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

download_and_unzip("https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz", "Homo_sapiens.gene_info.txt")

# Step 2: Parse the file
def parse_file(filename):
    df = pd.read_csv(filename, sep="\t", dtype=str)
    df['#tax_id'] = df['#tax_id'].astype(int)
    return df

df = parse_file("Homo_sapiens.gene_info.txt")  # Humans gene information

# Step 3: Write to JSON
def write_to_json(df, output_filename):
    df.to_json(output_filename, orient="records", lines=True)

write_to_json(df, "Homo_sapiens_gene_info.json")

# Step 4: Count Protein-coding genes per chromosome
def count_protein_coding_genes(df):
    protein_coding_genes = df[df['type_of_gene'] == 'protein-coding']
    chromosome_counts = protein_coding_genes['chromosome'].value_counts()
    return chromosome_counts

chromosome_counts = count_protein_coding_genes(df)
print(chromosome_counts)

# Step 5: Create Visualization
def create_visualization(chromosome_counts):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=chromosome_counts.index, y=chromosome_counts.values)
    plt.xlabel('Chromosome')
    plt.ylabel('Protein-Coding Gene Count')
    plt.title('Protein-Coding Gene Count Per Chromosome')
    plt.xticks(rotation=90)
    plt.show()

create_visualization(chromosome_counts)
