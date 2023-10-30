Module1.0#####################################################################
##
## modules heasoft/6.32
##
## modulefiles/heasoft - D. Wilkins, April 2014
## a TCL modulefile to use with environment modules or lmod
## need to update version, dir and builddir for each Heasoft installation
##
proc ModulesHelp { } {
        global version modroot

        puts stderr "heasoft - sets up HEASOFT in the current environment"
}

module-whatis   "Sets up HEASOFT in the current environment"

set	version		6.32
set	dir		/software/heasoft/heasoft-$version
set	builddir	$dir/x86_64-pc-linux-gnu-libc2.37

setenv	HEADAS		$builddir

setenv	EXT		lnx
setenv	FTOOLSINPUT	stdin
setenv	FTOOLS 		$builddir
setenv	FTOOLSOUTPUT	stdout
setenv	LHEA_DATA	$builddir/refdata
setenv	LHEA_HELP	$builddir/help
setenv	LHEAPERL	/usr/bin/perl
setenv	LHEASOFT	$builddir
setenv	PFCLOBBER	1
setenv	PGPLOT_DIR	$builddir/lib
setenv	PGPLOT_FONT	$builddir/lib/grfont.dat
setenv	PGPLOT_RGB	$builddir/lib/rgb.txt
setenv	POW_LIBRARY	$builddir/lib/pow
setenv	TCLRL_LIBDIR	$builddir/lib
setenv	XANADU		$dir
setenv	XANBIN		$builddir
setenv	XRDEFAULTS	$builddir/xrdefaults

setenv	LMODDIR		/software/xspec_models/build/$version

setenv	WARMABS_DATA	/software/xspec_models/warmabs/data
setenv	WARMABS_POP	pops.fits

prepend-path	PATH		$builddir/bin
prepend-path	LD_LIBRARY_PATH	$builddir/lib
prepend-path	PERLLIB		$builddir/lib/perl
prepend-path	PERL5LIB	$builddir/lib/perl
prepend-path	PYTHONPATH	$builddir/lib
prepend-path	PYTHONPATH	$builddir/lib/python
append-path 	PFILES	$builddir/syspfiles
prepend-path --delim ":;" PFILES	~/pfiles

#module load caldb/local

