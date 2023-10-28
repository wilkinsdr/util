#%Module1.0#####################################################################
##
## modules caldb/local
##
## modulefiles/caldb/local - D. Wilkins, Septemebr 2014
## a TCL modulefile to use with environment modules or lmod
## sets up a CALDB that you have locally on your computer
## need to point each of the paths to your CALDB installation
##
proc ModulesHelp { } {
        global version modroot

        puts stderr "caldb/local - sets up the current environment to use the local CALDB"
}

module-whatis   "Sets up HEASOFT in the current environment"

setenv CALDB		/data/caldb
setenv CALDBCONFIG	/data/caldb/software/tools/caldb.config
setenv CALDBALIAS	/data/caldb/software/tools/alias_config.fits

setenv GEOMAG_PATH	/data/caldb/geomag

