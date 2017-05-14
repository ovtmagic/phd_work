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
}

# install python/conda libs
function install_conda_libs(){
    /anaconda/bin/conda update conda
    /anaconda/bin/conda update anaconda
    /anaconda/bin/conda update scikit-learn -y
    /anaconda/bin/conda install theano -y
    /anaconda/bin/pip install keras

}



# Main ----------------------------

install_compiler
install_anaconda
install_conda_libs

