# heainit BASH function to initilise Heasoft in the current shell on macOS
# copy this function into your .bashrc or .zshrc
# then type "heainit" when you want to use Heasoft

# you will need to update the PYTHON environment variable to point to your Python binary
# set HEADAS environment variable to point to your Heasoft installation
# set LMODDIR to point to your local model library path (if you use this)
# WARMABS variables are only required if you use the warmabs model package

# (the loaded_modules line is for a zsh plugin I have written that keeps track what we've loaded into the environment and can be ignored)

heainit () {
        export CC=/opt/local/bin/gcc-mp-12
        export CXX=/opt/local/bin/g++-mp-12
        export FC=/opt/local/bin/gfortran-mp-12
        export PERL=/usr/bin/perl
        export PYTHON=~/anaconda3/bin/python3

        export HEADAS=/opt/software/heasoft/heasoft-6.32/aarch64-apple-darwin23.0.0
        export LMODDIR=/opt/software/xspec_models/build/6.32
        export WARMABS_DATA=/opt/software/xspec_models/warmabs/data
        export WARMABS_POP=pops.fits
        source $HEADAS/headas-init.sh

        loaded_modules+=(heasoft)
}
