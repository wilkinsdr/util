import numpy as np
import os
from astropy.io import fits


def add_arf(arf_files, weights=None, spec_files=None, outfile='src_comb.arf', weight_mode='exposure'):
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

    with fits.open(arf_files[0]) as f:
        elow = f['SPECRESP'].data['ENERG_LO']
        ehigh = f['SPECRESP'].data['ENERG_HI']

        specresp_hdr = f['SPECRESP'].header

    arf = np.zeros_like(elow)

    for arf_file, weight in zip(arf_files, weights):
        with fits.open(arf_file) as f:
            arf += weight * f['SPECRESP'].data['SPECRESP']

    elow_col = fits.Column(name='ENERG_LO', format='E', array=elow)
    ehigh_col = fits.Column(name='ENERG_HI', format='E', array=ehigh)
    specresp_col = fits.Column(name='SPECRESP', format='E', array=arf)

    pri_hdu = fits.PrimaryHDU()

    specresp_hdu = fits.BinTableHDU.from_columns([elow_col, ehigh_col, specresp_col])
    specresp_hdu.header['EXTNAME'] = 'SPECRESP'
    specresp_hdu.header['TELESCOP'] = specresp_hdr['TELESCOP']
    specresp_hdu.header['INSTRUME'] = specresp_hdr['INSTRUME']
    try:
        specresp_hdu.header['FILTER'] = specresp_hdr['FILTER']
    except:
        pass
    specresp_hdu.header['HDUCLASS'] = 'OGIP'
    specresp_hdu.header['HDUCLAS1'] = 'RESPONSE'
    specresp_hdu.header['HDUCLAS2'] = 'SPECRESP'
    specresp_hdu.header['HDUVERS'] = '1.1.0'

    hdulist = fits.HDUList([pri_hdu, specresp_hdu])

    if (os.path.exists(outfile)):
        os.remove(outfile)

    hdulist.writeto(outfile)
    print("Done")
