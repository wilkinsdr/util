help([[
CalDB environment module
]])

version = "local"
whatis("Version: " .. version)

dir = "/opt/caldb"

setenv("CALDB", dir)
setenv("CALDBCONFIG", dir .. "/software/tools/caldb.config")
setenv("CALDBALIAS", dir .. "/software/tools/alias_config.fits")

setenv("GEOMAG_PATH", "/opt/caldb/geomag")

