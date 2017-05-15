#/bin/bash




# echo message
function echo_msg(){
    echo "============================================"
    echo "$1"
    echo "============================================"
}

# Install compiler
function install_compiler(){
    echo_msg "Installing gcc, g++ and make"
    sudo apt-get install -y gcc
    sudo apt-get install -y g++
    sudo apt-get install -y make
}


# Install Anaconda
function install_anaconda(){
    echo_msg "Installing Anaconda"
    wget https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh
    sudo bash Anaconda3-4.3.1-Linux-x86_64.sh -b -p /anaconda
    /anaconda/bin/conda update -y conda
    /anaconda/bin/conda update -y anaconda
    # install libs
    echo_msg "Installing conda/python libraries"
    /anaconda/bin/conda install -y numpy
    /anaconda/bin/conda install -y matplotlib
    /anaconda/bin/conda install -y pandas
    /anaconda/bin/conda update scikit-learn -y
    /anaconda/bin/conda install theano -y
    /anaconda/bin/pip install keras


}

# Install Miniconda
function install_miniconda(){
    echo_msg "Installing Miniconda"
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    sudo bash Miniconda3-latest-Linux-x86_64.sh -b -p /anaconda
    #/anaconda/bin/conda update -y conda
    # install libs
    echo_msg "Installing conda/python libraries"
    /anaconda/bin/conda install -y numpy
    #/anaconda/bin/conda install -y matplotlib
    /anaconda/bin/conda install -y pandas
    /anaconda/bin/conda install scikit-learn -y
    /anaconda/bin/conda install theano -y
    /anaconda/bin/pip install keras

}




# Main ----------------------------


if [ "$1" == "miniconda" ]
then
    INSTALL_MINICONDA="yes"
fi

cd /tmp

install_compiler
if [ $INSTALL_MINICONDA == "yes" ]
then
    install_miniconda
else
    install_anaconda
fi

