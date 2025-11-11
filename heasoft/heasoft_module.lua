help([[
Heasoft environment module
]])

version = "6.36"
dir = "/opt/software/heasoft/heasoft-" .. version
builddir = dir .. "/aarch64-apple-darwin25.0.0"

whatis("Version: " .. version)

setenv("HEADAS", builddir)

--the lines below set the default compilers (usually required on macOS) 
--[[
setenv("CC", "/usr/bin/clang")
setenv("CXX", "/usr/bin/clang++")
setenv("FC", "/opt/local/bin/gfortran-mp-15")
setenv("PERL", "/opt/local/bin/perl")
setenv("PYTHON", "/opt/anaconda3/bin/python3")
]]

setenv("EXT", "lnx")
setenv("FTOOLSINPUT", "stdin")
setenv("FTOOLS", builddir)
setenv("FTOOLSOUTPUT", "stdout")
setenv("LHEA_DATA", builddir .. "/refdata")
setenv("LHEA_HELP", builddir .. "/help")
setenv("LHEAPERL", "/usr/bin/perl")
setenv("LHEASOFT", builddir)
setenv("PFCLOBBER", "1")
setenv("PGPLOT_DIR", builddir .. "/lib")
setenv("PGPLOT_FONT", builddir .. "/lib/grfont.dat")
setenv("PGPLOT_RGB", builddir .. "/lib/rgb.txt")
setenv("POW_LIBRARY", builddir .. "/lib/pow")
setenv("TCLRL_LIBDIR", builddir .. "/lib")
setenv("XANADU", dir)
setenv("XANBIN", builddir)
setenv("XRDEFAULTS", builddir .. "/xrdefaults")

setenv("LMODDIR", "/opt/software/xspec_models/build/" .. version)

setenv("WARMABS_DATA", "/opt/software/xspec_models/warmabs/data")
setenv("WARMABS_POP", "pops.fits")

setenv("RELXILL_TABLE_PATH", "/opt/software/xspec_models/relxill/data")

prepend_path("PATH", builddir .. "/bin")
prepend_path("LD_LIBRARY_PATH", builddir .. "/lib")
prepend_path("PERLLIB", builddir .. "/lib/perl")
prepend_path("PERL5LIB", builddir .. "/lib/perl")
prepend_path("PYTHONPATH", builddir .. "/lib")
prepend_path("PYTHONPATH", builddir .. "/lib/python")

setenv("PFILES", builddir .. "/syspfiles")
prepend_path("PFILES", "~/pfiles;")

