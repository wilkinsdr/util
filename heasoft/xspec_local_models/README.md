XSPEC Local Model Library Builder
D.R. Wilkins
Last updated: July 2023

Script to comile a single XSPEC local model package from multiple packages, for example if you have multiple local models that you have obtained from different sources

To use:
1) Create your xspec local model directory, e.g. /opt/software/xspec_models
2) Put build.sh inside that directory
3) Put each of your local models in a subdirectory of your xspec_models directory (for example, create separate subdirectories for relxill, warmabs, etc, etc). Each model directory should contain all of the source code for the model, as well as its lmodel.dat (or lmodel_modelname.dat).
4) Make sure Heasoft is initialised in your current shell environment
5) Run "./build.sh build/[heasoft_version]"

This will copy all of the code for the individual models into the build/[heasoft_version] subdirectory, and will compile a single lmodel.dat file, describing all of the models to XSPEC. Of course, you can choose the directory it compiles into, I just find it useful to create separate build directories fot each version of Heasoft, in case I ever need to go back to an older version.

Example directory structure
- /opt/software/xspec_models
- - build.sh
- - relxill
- - warmabs
- - (other model packages)
- - build (this wil be created by build.sh)
- - - 6.32
- - - - (code for each model)
- - - - lmodel.dat (describing all of the models to XSPEC)
- - - - liblocal.so (liblocal.dylib on Mac - the actual compiled model package)
- - - 6.31
- - - (other Heasoft versions you have built the package for)

Once compiled, you will be able to load this local model package just like any other with the XSPEC command:
XSPEC12> lmod local /opt/software/xspec_models/build/[heasoft_version]

You can also get XSPEC to load the model package automatically on start up. To do this for every user on your computer, 
1) Go to the Xspec/src/scripts directory within your Heasoft installation
2) Add the line "load /opt/software/xspec_models/build/[heasoft_version]/liblocal.so" to the end of the file glocal_customize.tcl (note that it's liblocal.dylib on mac, instead of .so) 
3) Run "hmake install" within that directory (you will need Heasoft initialised in the shell to do this)

