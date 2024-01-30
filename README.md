# project_mohri_nishimura

## Directory

    .
    ├── data  
    |    ├── base
    |    |    └── 10x_results/filtered_feature_bc_matrix (10x's Output)
    |    | 
    |    └── calculated
    |         └── preprocessing (preprocessing data)
    ├── preprocessing
    |    ├── preprocessing.ipynb
    |    └── utils.py
    ├── fig_4b
    ├── fig_4c
    ├── fig_4d
    ├── fig_ex7b
    ├── fig_ex7c
    ├── poetry.lock  
    ├── pyproject.toml
    ├── .gitignore  
    └── README.md  



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
Set up the data in the following `data/base/10x_results/filtered_feature_bc_matrix` directory.


### jupyter run 
```sh
$ poetry run jupyter lab  
```


### preprocessing 
Run `preprocessing/preprocessing.ipynb`


### Figure
Run any figure creation process


### Failing to install python-igraph (if needed)  
Setup your computer environment for package compiling

(Ubuntu)
```sh
$ sudo apt update gcc build-essential python3-dev libxslt-dev libffi-dev libssl-dev libxml2 libxml2-dev zlib1g-dev
```

