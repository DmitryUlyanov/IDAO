FROM ubuntu:16.04

RUN locale-gen en_US.UTF-8 && update-locale

RUN (echo "deb http://cran.mtu.edu/bin/linux/ubuntu xenial/" >> /etc/apt/sources.list && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9) && \
apt-get update -q && apt-get upgrade -y -q && apt-get install -y -q --no-install-recommends r-base \
                                              r-base-dev \
                                              gdebi-core \
                                              libapparmor1  \
                                              sudo \
                                              libcurl4-openssl-dev \
                                              libssl1.0.0 \
                                              build-essential \
                                              cmake \
                                              curl \
                                              vim \
                                              ca-certificates \
                  && apt-get clean \
                  && rm -rf /tmp/* /var/tmp/* \
                  && rm -rf /var/lib/apt/lists/*

RUN curl -o ~/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /usr/conda && \     
     rm ~/miniconda.sh && \
     /usr/conda/bin/conda create -y --name py3 python=3.6 numpy scipy pandas scikit-learn matplotlib joblib tqdm ipython pip && \
     /usr/conda/bin/conda clean -ya && \ 
     /usr/conda/envs/py3/bin/pip install xgboost lightgbm catboost && \
     /usr/conda/bin/conda create -y --name py2 python=2.7 numpy scipy pandas scikit-learn matplotlib joblib tqdm ipython pip && /usr/conda/bin/conda clean -ya && \
     /usr/conda/envs/py2/bin/pip install xgboost lightgbm catboost