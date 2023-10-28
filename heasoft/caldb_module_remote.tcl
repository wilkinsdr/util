#%Module1.0#####################################################################
##
## modules caldb/remote
##
## modulefiles/caldb/remote - D. Wilkins, Septemebr 2014
## a TCL modulefile to use with environment modules or lmod
## sets up CALDB to pull files as needed from the HEASARC server
## need to point each of the paths to your CALDB installation
##
proc ModulesHelp { } {
        global version modroot

        puts stderr "caldb/remote - sets up the current environment to use the remote CALDB"
}

module-whatis   "Sets up HEASOFT in the current environment"

setenv CALDB		http://heasarc.gsfc.nasa.gov/FTP/caldb
setenv CALDBCONFIG	/data/caldb/software/tools/caldb.config
setenv CALDBALIAS	/data/caldb/software/tools/alias_config.fits

