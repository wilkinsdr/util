#!/usr/bin/env bash
#
# Merge XSPEC model packages in subdirectories into a single model package
# and compile it
#
# Subdirectories of packages are not copied so need to ensure model data files
# are accessible
#
shopt -s extglob

if [ -n $1 ]; then
	BUILD_DIR=$1
else
	BUILD_DIR=build
fi
LMODEL_DAT=lmodel.dat
LMODEL=${BUILD_DIR}/${LMODEL_DAT}
PACKAGE=local
#UDMGET=-udmget64

if [ -d $BUILD_DIR ]; then
    rm -r $BUILD_DIR
fi

mkdir -p $BUILD_DIR

BUILD_DIR_START=$(sed 's,/.*,,' <<< $BUILD_DIR)

for d in $(ls -d !($BUILD_DIR_START)); do
    if [ ! -d $d ]; then
        continue
    fi

    if [[ $d == *".off" ]]; then
	continue
    fi

    THIS_LMODEL=$(ls $d/*lmodel*.dat)
    THIS_LMODEL_NAME=$(basename $THIS_LMODEL)
    echo $THIS_LMODEL

    if [ -z $THIS_LMODEL ]; then
        continue
    fi

    cat "$THIS_LMODEL" >> $LMODEL
    echo "" >> $LMODEL
    echo "" >> $LMODEL
    cp $d/!(${THIS_LMODEL_NAME}) $BUILD_DIR
done

cd $BUILD_DIR
rm *.so *.dylib
echo "initpackage ${PACKAGE} ${LMODEL_DAT} . ${UDMGET}" | xspec
cd -
