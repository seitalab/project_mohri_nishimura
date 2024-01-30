
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import scanpy as sc
import pandas as pd
import seaborn as sns
import mygene


def data_import(data_base_path):
    # data import
    adata = sc.read_10x_mtx(
        data_base_path, 
        var_names='gene_symbols',
        cache=True) 
    
    # add label
    pre_batch = adata.obs.copy().index.tolist()
    sequence = [1, 2, 5, 6, 3, 4, 7, 8] #s1, s2, s5, s6, s3, s4, s7, s8
    adata.obs['batch'] = [str(sequence[int(x[-1]) - 1]) for x in pre_batch if x[-1].isdigit()]
    adata.obs['y_o'] = ['young' if int(x) < 5 else 'old' for x in adata.obs['batch']]
    print(adata.obs['batch'][:3])
    print(adata.obs['y_o'][:5])

    # save infomation
    adata.raw = adata
    
    # check data
    print(adata)
    sc.pl.highest_expr_genes(adata, n_top=20)
    
    return adata    


# calcurate
def basic_computing(adata, seed):
    print(adata)
    sc.tl.pca(adata, n_comps=50, random_state=seed)
    sc.pp.neighbors(adata)
    sc.tl.umap(adata, min_dist=0.01,spread=1, n_components=2, random_state=seed)
    sc.tl.louvain(adata, random_state=seed)

    return adata


def basic_plot(adata):
    sc.settings.verbosity = 3  
    sc.settings.set_figure_params(dpi=100, dpi_save=300)
    
    adata.obs.groupby('louvain')

    sc.pl.pca(adata, color=['louvain'], components = ['1,2'], ncols=1, size=2)
    sc.pl.umap(adata, color=['batch'], components = ['1,2'], ncols=1, size=2)
    sc.pl.umap(adata, color=['y_o'], components = ['1,2'], ncols=1, size=2)
    sc.pl.umap(adata, color=['louvain'], components = ['1,2'], ncols=1, size=2)
    
    
def dct_check(adata):
    sc.pl.umap(adata, color=['Dct'], components = ['1,2'], ncols=1, size=1)
    sc.pl.stacked_violin(adata, ['Dct'], groupby='louvain', rotation=90)

    

# Protein coding's RNA
def gene_only_cds(adata):
    gene_id_list = adata.var['gene_ids'].to_list()
    
    # mygene ENSMUSG ID to RNA type
    mg = mygene.MyGeneInfo()
    new_gene_id_list = mg.getgenes(gene_id_list, fields='name,symbol,type_of_gene,genomic_pos')
    
    new_gene_symbol_list = []
    gene_id_lists =  gene_id_list.copy()
    for x in new_gene_id_list:
        if x['query'] in gene_id_lists:
            gene_id_lists.remove(x['query'])

            try:
                if x['genomic_pos']['chr'] == 'MT':
                    new_gene_symbol_list += [[x['query'], x['type_of_gene']]] 

                else:
                    new_gene_symbol_list += [[x['query'], x['type_of_gene']]]
            except:
                new_gene_symbol_list += [[x['query'], 'not found']]

        else:
            pass
        
    
    # check
    print('*' * 100)
    print('{}={} ?'.format(len(gene_id_list), len(new_gene_symbol_list)))
          
    # combine adata  
    new_gene_symbol_list_df = pd.DataFrame(new_gene_symbol_list)
    new_gene_symbol_list_df.set_index(0,inplace=True)
          
    adata.var['gene_type'] = 'default'
    for num, x in enumerate(adata.var['gene_ids']):
        adata.var['gene_type'][num] = new_gene_symbol_list_df[1][x]
    
    # Protein coding's RNA
    adata_gene_only_cds = adata[:, adata.var['gene_type'] == 'protein-coding']
    adata_gene_only_cds.raw = adata_gene_only_cds
    
    sc.pl.highest_expr_genes(adata_gene_only_cds, n_top=20)
          
    return adata_gene_only_cds


# exclude mitocondrian's RNA
def cut_gene_mitocondrian(adata):
    mito_genes = adata.var_names.str.startswith('mt-')
    not_mito_genes = [not x for x in mito_genes]
    
    not_mito_adata = adata[:, not_mito_genes]
    not_mito_adata.raw = not_mito_adata
    
    sc.pl.highest_expr_genes(not_mito_adata, n_top=20)
    
    return not_mito_adata


# exclude ribosome's RNA
def cut_gene_ribosome(adata):
    rp_genes = adata.var_names.str.startswith('Rps')
    rp_genes += adata.var_names.str.startswith('Rpl')

    not_rp_genes = [not x for x in rp_genes]
    not_rp_adata = adata[:, not_rp_genes]
    not_rp_adata.raw = not_rp_adata
    
    sc.pl.highest_expr_genes(not_rp_adata, n_top=20)
    
    return not_rp_adata


# # droplet
def qcA_linear(adata, out_dir,  model_name):
    # reads / droplet 
    adata.obs['n_counts'] = adata.X.sum(axis=1)
    
    # total : total reads / droplet's mean , sd
    read_mean = adata.obs['n_counts'].mean()
    read_std = adata.obs['n_counts'].std()

    print('qcA : mean : {}'.format(read_mean))
    print('qcA : sd : {}'.format(read_std))

    print('qcA : mean + sd : {}'.format(read_mean + read_std))
    print('qcA : mean - sd : {}'.format(read_mean - read_std))

    qc_top = read_mean + read_std
    qc_bottom = read_mean - read_std
    
    # total : total reads / droplet 
    sns.displot(adata.obs['n_counts'], kde=False)
    # plt.xlim( 0,  20000)
    # plt.xlim( 0,  1500)
    plt.title('total reads')
    plt.xlabel('total reads / droplet')
    plt.ylabel('droplet counts')
    # plt.savefig('read_counts_qcA_linear_{}.png'.format(model_name), bbox_inches='tight')
    
    # cluster : total reads / droplet 
    df = []
    exclude_cluster = []
    
    print('*' * 100)
    
    for num in adata.obs['louvain'].cat.categories:
        data = adata[adata.obs['louvain'] == num]
        c_mean = data.obs['n_counts'].mean()
        df.append(c_mean)
        
        if c_mean > qc_top:
            print('Cluster{}, qcA linear top over'.format(num))
            exclude_cluster += [num]
        elif c_mean < qc_bottom:
            print('Cluster{}, qcA linear bottom over'.format(num))
            exclude_cluster += [num]
        else:
            print('Cluster{}'.format(num))

        print('Mean : {}'.format(c_mean))
    
    pd.DataFrame(df).T.to_csv('{}/read_counts_qcA_linear_{}_cluster_mean.csv'.format(out_dir, model_name))
    print('*' * 100)
    print('exclude cluster :' + ','.join(exclude_cluster))
    
    # exclude cluster by (mean+_1sd) 
    adata_qcA = adata.copy()
    adata_qcA.obs['louvain'] = adata.obs['louvain'] 

    for ec in exclude_cluster:
        adata_qcA = adata_qcA[adata_qcA.obs['louvain'] != ec]

    print('*' * 100)
    print(adata_qcA)
    
    return adata_qcA

# # visualize
def add_computing(adata, seed):
    sc.tl.rank_genes_groups(adata, use_raw=False, groupby='louvain')
    sc.tl.dendrogram(adata, groupby='louvain')
    
    return adata


def data_output(adata, model_name):
    f_name = 'output/{}'.format(model_name)
    
    # save label infomation
    adata.obs.to_csv('{}_obs.csv'.format(f_name))
    
    # UMAP1, UMAP2
    pd.DataFrame(adata.obsm['X_umap'],                        index=adata.obs.index).to_csv('{}_umap_coordinate_information.csv'.format(f_name))
    
    # 
    pd.DataFrame(adata.obs.groupby('louvain').size()).T.to_csv('{}_cluster_counts.csv'.format(f_name))

    # UMAP Figure
    sc.pl.umap(adata, color=['louvain'], components = ['1,2'], ncols=1, size=2, save=model_name)
    
    # t-test
    pd.DataFrame(adata.uns['rank_genes_groups']['names']).to_csv('{}_t_test.csv'.format(f_name))
