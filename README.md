Antagonistic Stem Cell Fate under Stress Governs Decisions between Hair greying and Melanoma
Stem cell senescence-differentiation under stress governs decisions between hair greying and melanoma fate

<div align="center">

[![Paper](https://img.shields.io/badge/Project-Paper-Red.svg)]()&nbsp;&nbsp;
[![Code](https://img.shields.io/badge/Project-Code-2196F3.svg)](https://github.com/seitalab/project_mohri_nishimura/)&nbsp;&nbsp;
[![Data](https://img.shields.io/badge/Project-Data-009688.svg)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE252031)&nbsp;&nbsp;
</div>

## Directory

    .
    ├── data  
    |    ├── base
    |    |    └── 10x_results/filtered_feature_bc_matrix (10x's Output)
    |    | 
    |    └── calculated
    |         └── preprocessing
    |              └── normal_analysis.h5ad
    ├── preprocessing
    |    ├── preprocessing.ipynb
    |    └── utils.py
    ├── fig_5b
    ├── fig_5c
    ├── fig_5d
    ├── fig_5e
    ├── fig_ex8b
    ├── poetry.lock  
    ├── pyproject.toml
    ├── .gitignore  
    └── README.md  

## Data
The Gene Expression Omnibus (GEO) under accession code : [GSE252031](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE252031)

## Setup
### pyenv install (if needed)
```sh
$ git clone git://github.com/yyuu/pyenv.git ~/.pyenv  
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile  
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile  
$ echo 'eval "$(pyenv init --path)"' >> ~/.bash_profile  
$ source ~/.bash_profile  
```

### code clone
```sh
$ git clone git@github.com:seitalab/project_mohri_nishimura.git
```


### pyenv setup  
```sh
$ pyenv install 3.8.5  
$ cd ~/project_mohri_nishimura  # project directory name  
$ pyenv local 3.8.5  
```


### poetry install
```sh
$ pip3 install poetry
$ poetry config virtualenvs.in-project true
```


### package install
```sh
$ poetry install  
```  

### setup the data
Get the Procceded data `nishimura_scRNAseq_Yamanashi_20220407_JS_20240119.h5ad` from GEO ([GSE252031](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE252031)).
Rename it as `normal_analysis.h5ad` and set it in the following folder.


### jupyter run 
```sh
$ poetry run jupyter lab  
```


### preprocessing (skip if processed data exists)
Set up the data in the following `data/base/10x_results/filtered_feature_bc_matrix` directory.
Run `preprocessing/preprocessing.ipynb`


### Figure
Run any figure creation process


### Failing to install python-igraph (if needed)  
Setup your computer environment for package compiling

(Ubuntu)
```sh
$ sudo apt update gcc build-essential python3-dev libxslt-dev libffi-dev libssl-dev libxml2 libxml2-dev zlib1g-dev
```

