import numpy as np
import itertools
import operator
import os
from astropy.io import fits


def unpack_rmf(rmf_file):
    with fits.open(rmf_file) as f:
        elow = f['MATRIX'].data['ENERG_LO']
        ehigh = f['MATRIX'].data['ENERG_HI']
        fchan = f['MATRIX'].data['F_CHAN']
        nchan = f['MATRIX'].data['N_CHAN']
        mat = f['MATRIX'].data['MATRIX']
        chan = f['EBOUNDS'].data['CHANNEL']

    en = 0.5 * (elow + ehigh)

    rmf = np.zeros((len(en), len(chan)))

    for i in range(len(en)):
        en_chan = np.concatenate([f + np.arange(n) for f, n in zip(fchan[i], nchan[i])])
        en_mat = mat[i]
        rmf[i][en_chan] = en_mat

    return rmf, en, chan


def pack_rmf(rmf):
    ngrp = []
    fchan = []
    nchan = []
    matrix = []

    for i in range(rmf.shape[0]):
        chan_groups = [[i for i, value in it] for key, it in
                       itertools.groupby(enumerate(rmf[i] > 0), key=operator.itemgetter(1)) if key != 0]

        ngrp.append(len(chan_groups))
        fchan.append([c[0] for c in chan_groups])
        nchan.append([len(c) for c in chan_groups])
        matrix.append(rmf[i][rmf[i] > 0])

    ngrp = np.array(ngrp)
    fchan = np.array(fchan, dtype=object)
    nchan = np.array(nchan, dtype=object)
    matrix = np.array(matrix, dtype=object)

    return ngrp, fchan, nchan, matrix


def add_rmf(rmf_files, weights=None, spec_files=None, outfile='src_comb.rmf', weight_mode='exposure'):
    if weights is None:
        if spec_files is not None:
            weights = []
            for spec_file in spec_files:
                with fits.open(spec_file) as f:
                    if weight_mode == 'exposure':
                        weights.append(f['SPECTRUM'].header['EXPOSURE'])
                    elif weight_mode == 'counts':
                        weights.append(np.sum(f['SPECTRUM'].data['COUNTS']))
            weights = np.array(weights, dtype=float)
            weights /= np.sum(weights)
        else:
            weights = np.ones(len(rmf_files)) / len(rmf_files)

    with fits.open(rmf_files[0]) as f:
        chan = f['EBOUNDS'].data['CHANNEL']
        emin = f['EBOUNDS'].data['E_MIN']
        emax = f['EBOUNDS'].data['E_MAX']
        elow = f['MATRIX'].data['ENERG_LO']
        ehigh = f['MATRIX'].data['ENERG_HI']

        ebounds_hdr = f['EBOUNDS'].header
        matrix_hdr = f['MATRIX'].header

    rmf_matrix = np.zeros((len(elow), len(chan)))

    for rmf_file, weight in zip(rmf_files, weights):
        print('Unpacking ' + rmf_file)
        r, _, _ = unpack_rmf(rmf_file)
        rmf_matrix += weight * r

    ngrp, fchan, nchan, matrix = pack_rmf(rmf_matrix)

    chan_col = fits.Column(name='CHANNEL', format='J', array=chan)
    emin_col = fits.Column(name='E_MIN', format='E', array=emin)
    emax_col = fits.Column(name='E_MAX', format='E', array=emax)
    elow_col = fits.Column(name='ENERG_LO', format='E', array=elow)
    ehigh_col = fits.Column(name='ENERG_HI', format='E', array=ehigh)
    ngrp_col = fits.Column(name='N_GRP', format='I', array=ngrp)
    fchan_col = fits.Column(name='F_CHAN', format='PI', array=fchan)
    nchan_col = fits.Column(name='N_CHAN', format='PI', array=nchan)
    matrix_col = fits.Column(name='MATRIX', format='PE', array=matrix)

    pri_hdu = fits.PrimaryHDU()

    ebounds_hdu = fits.BinTableHDU.from_columns([chan_col, emin_col, emax_col])
    ebounds_hdu.header['EXTNAME'] = 'EBOUNDS'
    ebounds_hdu.header['TELESCOP'] = ebounds_hdr['TELESCOP']
    ebounds_hdu.header['INSTRUME'] = ebounds_hdr['INSTRUME']
    try:
        ebounds_hdu.header['FILTER'] = ebounds_hdr['FILTER']
    except:
        pass
    ebounds_hdu.header['CHANTYPE'] = ebounds_hdr['CHANTYPE']
    ebounds_hdu.header['DETCHANS'] = len(chan)
    ebounds_hdu.header['HDUCLASS'] = 'OGIP'
    ebounds_hdu.header['HDUCLAS1'] = 'RESPONSE'
    ebounds_hdu.header['HDUCLAS2'] = 'EBOUNDS'
    ebounds_hdu.header['HDUVERS'] = '1.2.0'

    matrix_hdu = fits.BinTableHDU.from_columns([elow_col, ehigh_col, ngrp_col, fchan_col, nchan_col, matrix_col])
    matrix_hdu.header['EXTNAME'] = 'MATRIX'
    matrix_hdu.header['TELESCOP'] = matrix_hdr['TELESCOP']
    matrix_hdu.header['INSTRUME'] = matrix_hdr['INSTRUME']
    try:
        matrix_hdu.header['FILTER'] = matrix_hdr['FILTER']
    except:
        pass
    matrix_hdu.header['CHANTYPE'] = matrix_hdr['CHANTYPE']
    matrix_hdu.header['DETCHANS'] = len(chan)
    matrix_hdu.header['HDUCLASS'] = 'OGIP'
    matrix_hdu.header['HDUCLAS1'] = 'RESPONSE'
    matrix_hdu.header['HDUCLAS2'] = 'RSP_MATRIX'
    matrix_hdu.header['HDUVERS'] = '1.3.0'
    matrix_hdu.header['TLMIN4'] = np.min(chan)
    matrix_hdu.header['TLMAX4'] = np.max(chan)
    matrix_hdu.header['NUMGRP'] = np.sum(ngrp)
    matrix_hdu.header['NUMELT'] = np.sum([np.sum(c) for c in nchan])
    try:
        matrix_hdu.header['HDUCLAS3'] = matrix_hdr['HDUCLAS3']
    except:
        pass

    hdulist = fits.HDUList([pri_hdu, ebounds_hdu, matrix_hdu])

    if (os.path.exists(outfile)):
        os.remove(outfile)

    hdulist.writeto(outfile)
    print("Done")
