#!/bin/bash

export MIR_HOME=$(pwd)


function echo_msg(){
    echo "=========================================="
    echo $1
    echo "=========================================="
}
 
function check_result(){
    local result=$1
    local msg=$2
    if [ $result -ne 0 ]; then
        echo_msg "Error: $msg (rc=$result)"
        exit 1
    fi
}
 
function compile_metamidi(){
    cd src
    # metamidi
    echo_msg "Compiling metamidi"
    cd metamidi
    make
    check_result $? "error compiling metamidi."
    cp metamidi $MIR_HOME/bin
    make clean
    cd ..

    # smf2txt
    echo_msg "Compiling smf2txt/txt2smf"
    cd smf2txt
    make
    check_result $? "error compiling smf2txt"
    ls -lart
    echo "$MIR_HOME"
    cp smf2txt $MIR_HOME/bin
    cp txt2smf $MIR_HOME/bin
    make clean
    cd $MIR_HOME
    
    echo_msg "metamidi, smf2txt, txt2smf copied to bin"
}



#============================================================
# Main
#============================================================

echo_msg "MIR_HOME: $MIR_HOME"
mkdir -p $MIR_HOME/bin
export PATH=$MIR_HOME/bin:$PATH

compile_metamidi