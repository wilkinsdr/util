'''
pyxspec_util.py - useful functions for working with pyXSPEC

D.R. Wilkins - 02/11/2021
'''
import xspec
import numpy as np
import pandas as pd
import pylag.plotter as plotter

def plot_spectra(mode='data', minSig=10, maxBins=10, figsize=(10,6), model=True, colours=['k','r','b','g','m','c'], **kwargs):
    '''
    Plots the spectra and associated models using the pyLag matplotlib wrapper.

    Parameters
    ----------
    mode: The XSPEC plot mode to use: data, ldata (does the same as data), euf or eeuf (default = 'data')
    minSig: Minimum significance per bin (default = 10)
    maxBins: Maximum number of adjacent channels to combine to reach minSig (default = 10)
    figSize: Tuple with the x,y dimensions of the figure to be produced (default=(10,6))
    model: Plot the models in addition to the spectra (default=True)
    colours: List of matplotlib colour codes representing tje sequence colours to be used to the spectra.
             When the list runs out, will start again from the beginning (default=['k','r','b','g','m','c'])
    **kwargs: passed to Plot class constructor
    '''
    if mode == 'eeuf':
        ylabel = '$EF_{E}~/~keV^2~ct~s^{-1}~keV^{-1}$'
    else:
        ylabel = '$Count~rate~/~ct~s^{-1}~keV^{-1}$'
    xspec.Plot.xAxis = 'keV'
    xspec.Plot.setRebin(minSig, maxBins, -1)
    xspec.Plot(mode)
    plot_series = []
    marker_series = []
    colour_series = []
    for group in range(1,xspec.AllData.nGroups+1):
        try:
            x = np.array(xspec.Plot.x(group))
            xe = np.array(xspec.Plot.xErr(group))
            y = np.array(xspec.Plot.y(group))
            ye = np.array(xspec.Plot.yErr(group))
            if model:
                try:
                    mod = np.array(xspec.Plot.model(group))
                except:
                    model=False
            plot_series.append(plotter.DataSeries(x=(x,xe),y=(y,ye), xscale='log', yscale='log', xlabel='Energy / keV', ylabel=ylabel))
            if model:
                plot_series.append(plotter.DataSeries(x=x,y=mod, xscale='log', yscale='log'))
            marker_series.append('+')
            if model:
                marker_series.append('-')
            colour_series.append(colours[(group-1) % len(colours)])
            if model:
                colour_series.append(colours[(group-1) % len(colours)])
        except:
            break
    p = plotter.Plot(plot_series, figsize=figsize, **kwargs)
    p.marker_series = marker_series
    p.colour_series = colour_series
    return p


def plot_ratio(mode='ratio', minSig=10, maxBins=10, figsize=(10,6), colours=['k','r','b','g','m','c'], **kwargs):
    '''
    Plots the ratio of the spectra to their respective models.

    Parameters
    ----------
    minSig: Minimum significance per bin (default = 10)
    maxBins: Maximum number of adjacent channels to combine to reach minSig (default = 10)
    figSize: Tuple with the x,y dimensions of the figure to be produced (default=(10,6))
    colours: List of matplotlib colour codes representing tje sequence colours to be used to the spectra.
             When the list runs out, will start again from the beginning (default=['k','r','b','g','m','c'])
    **kwargs: passed to Plot class constructor
    '''
    xspec.Plot.xAxis = 'keV'
    xspec.Plot.setRebin(minSig, maxBins, -1)
    xspec.Plot(mode)
    plot_series = []
    marker_series = []
    colour_series = []
    for group in range(1,xspec.AllData.nGroups+1):
        try:
            x = np.array(xspec.Plot.x(group))
            xe = np.array(xspec.Plot.xErr(group))
            y = np.array(xspec.Plot.y(group))
            ye = np.array(xspec.Plot.yErr(group))
            plot_series.append(plotter.DataSeries(x=(x,xe),y=(y,ye), xscale='log', yscale='linear', xlabel='Energy / keV', ylabel='chi2' if mode == 'delchi' else 'Data / Model'))
            marker_series.append('+')
            colour_series.append(colours[(group-1) % len(colours)])
        except:
            break
    p = plotter.Plot(plot_series, figsize=figsize, **kwargs)
    p.marker_series = marker_series
    p.colour_series = colour_series
    return p


def plot_model(mode='eem', figsize=(10,6), colours=['k','r','b','g','m','c'], **kwargs):
    '''
    Plots the model using the pyLag matplotlib wrapper.

    Parameters
    ----------
    mode: The XSPEC plot mode to use: data, ldata (does the same as data), euf or eeuf (default = 'data')
    figSize: Tuple with the x,y dimensions of the figure to be produced (default=(10,6))
    colours: List of matplotlib colour codes representing tje sequence colours to be used to the spectra.
             When the list runs out, will start again from the beginning (default=['k','r','b','g','m','c'])
    **kwargs: passed to Plot class constructor
    '''
    if mode == 'eeuf':
        ylabel = '$EF_{E}~/~keV^2~ct~s^{-1}~keV^{-1}$'
    else:
        ylabel = '$Count~rate~/~ct~s^{-1}~keV^{-1}$'
    xspec.Plot.xAxis = 'keV'
    xspec.Plot(mode)
    plot_series = []
    marker_series = []
    colour_series = []
    for group in range(1,xspec.AllData.nGroups+1):
        try:
            x = np.array(xspec.Plot.x(group))
            xe = np.array(xspec.Plot.xErr(group))
            mod = np.array(xspec.Plot.model(group))
            plot_series.append(plotter.DataSeries(x=x,y=mod, xscale='log', yscale='log'))
            marker_series.append('-')
            colour_series.append(colours[(group-1) % len(colours)])
        except:
            break
    p = plotter.Plot(plot_series, figsize=figsize, **kwargs)
    p.marker_series = marker_series
    p.colour_series = colour_series
    return p


def get_plot_spectra(mode='data', minSig=10, maxBins=10, model=True):
    '''
    Returns XSPEC plots in DataSeries objects

    Parameters
    ----------
    mode: The XSPEC plot mode to use: data, ldata (does the same as data), euf or eeuf (default = 'data')
    minSig: Minimum significance per bin (default = 10)
    maxBins: Maximum number of adjacent channels to combine to reach minSig (default = 10)
    model: Plot the models in addition to the spectra (default=True)
    **kwargs: passed to Plot class constructor
    '''
    if mode == 'eeuf':
        ylabel = '$EF_{E}~/~keV^2~ct~s^{-1}~keV^{-1}$'
    else:
        ylabel = '$Count~rate~/~ct~s^{-1}~keV^{-1}$'
    xspec.Plot.xAxis = 'keV'
    xspec.Plot.setRebin(minSig, maxBins, -1)
    xspec.Plot(mode)
    plot_series = []
    for group in range(1,xspec.AllData.nGroups+1):
        try:
            x = np.array(xspec.Plot.x(group))
            xe = np.array(xspec.Plot.xErr(group))
            y = np.array(xspec.Plot.y(group))
            ye = np.array(xspec.Plot.yErr(group))
            if model:
                try:
                    mod = np.array(xspec.Plot.model(group))
                except:
                    model=False
            plot_series.append(plotter.DataSeries(x=(x,xe),y=(y,ye), xscale='log', yscale='log', xlabel='Energy / keV', ylabel=ylabel))
            if model:
                plot_series.append(plotter.DataSeries(x=x,y=mod, xscale='log', yscale='log'))
        except:
            break

    return plot_series


def get_plot_ratio(minSig=10, maxBins=10):
    '''
    Returns the ratio of the spectra to their respective models in a DataSeries

    Parameters
    ----------
    minSig: Minimum significance per bin (default = 10)
    maxBins: Maximum number of adjacent channels to combine to reach minSig (default = 10)
    figSize: Tuple with the x,y dimensions of the figure to be produced (default=(10,6))
    colours: List of matplotlib colour codes representing tje sequence colours to be used to the spectra.
             When the list runs out, will start again from the beginning (default=['k','r','b','g','m','c'])
    **kwargs: passed to Plot class constructor
    '''
    xspec.Plot.xAxis = 'keV'
    xspec.Plot.setRebin(minSig, maxBins, -1)
    xspec.Plot('ratio')
    plot_series = []
    for group in range(1,xspec.AllData.nGroups+1):
        try:
            x = np.array(xspec.Plot.x(group))
            xe = np.array(xspec.Plot.xErr(group))
            y = np.array(xspec.Plot.y(group))
            ye = np.array(xspec.Plot.yErr(group))
            plot_series.append(plotter.DataSeries(x=(x,xe),y=(y,ye), xscale='log', yscale='linear', xlabel='Energy / keV', ylabel='Data / Model'))
        except:
            break
    return plot_series


def param_table(model=None, free=False):
    '''
    Returns a table of the model parameters in a pandas DataFrame.

    Parameters
    ----------
    model: Model (i.e. spectrum number) for which to return the parameters. 
           If None, will iterate through all models and concatenate parameters
           into a single list

    free: If True, will only return the free and unlinked parameters
    '''
    data = []
    
    mod_range = range(1,xspec.AllData.nGroups+1) if model is None else [model]
    for mod_num in mod_range:
        try:
            model = xspec.AllModels(mod_num)
        
            for comp_num, comp_name in enumerate(model.componentNames):
                comp = getattr(model, comp_name)
                for param_name in comp.parameterNames:
                    param = getattr(comp, param_name)
                    if len(param.values) == 6:
                        delta = param.values[1]
                        minval = param.values[2]
                        lowval = param.values[3]
                        highval = param.values[4]
                        maxval = param.values[5]
                        is_free = ((param.values[1]>0)*(param.link == ''))==1
                    else:
                        delta, minval, lowval, highval, maxval = 0, 0, 0, 0, 0
                        is_free = False

                    data.append([comp_name, comp_num+1, param_name, param.values[0], is_free, param.link, delta, minval, lowval, highval, maxval])

            df = pd.DataFrame(data=data, columns=['component', 'componentn', 'parameter', 'value', 'free', 'link', 'delta', 'min', 'low', 'high', 'max'])
            df.index += 1
        except:
            break
    
    return df[df['free']] if free else df


def get_params(model=None, free=False):
    '''
    Returns a list of all of the model parameter objects.

    Parameters
    ----------
    model: Model (i.e. spectrum number) for which to return the parameters. 
           If None, will iterate through all models and concatenate parameters
           into a single list

    free: If True, will only return the free and unlinked parameters
    '''
    param_list = []
    mod_range = range(1,xspec.AllData.nGroups+1) if model is None else [model]
    for mod_num in mod_range:
        try:
            model = xspec.AllModels(mod_num)
            
            for comp_name in model.componentNames:
                comp = getattr(model, comp_name)
                for param_name in comp.parameterNames:
                    if not free or (len(getattr(comp, param_name).values)==6 and getattr(comp, param_name).values[1]>0 and getattr(comp, param_name).link == ''):
                        param_list.append(getattr(comp, param_name))      
        except:
            break
    
    return param_list


def chain2df(chainfile):
    import pandas as pd
    from astropy.io import fits

    with fits.open(chainfile) as chain_fits:
        chain_data = np.array(chain_fits['CHAIN'].data)
        df = pd.DataFrame(chain_data.byteswap().newbyteorder(), columns=[c.name for c in chain_fits['CHAIN'].columns])

    return df


def plot_corner(df, truth='bestfit', quantiles=None, params=None):
    import corner
    chaindf = df.drop(labels='FIT_STATISTIC', axis=1)

    if params is not None:
        # l = [[x for x in df.columns if y + '__' in x] for y in params]
        # param_list = [item for sublist in l for item in sublist]
        # chaindf = chaindf[param_list]
        chaindf = chaindf[[[x for x in df.columns if y+'__' in x][0] for y in params]]

    if truth == 'bestfit':
        bestfit = chaindf.iloc[[np.argmin(df.FIT_STATISTIC)]].to_numpy()[0]
    elif truth == 'mean':
        bestfit = chaindf.mean().to_numpy()[:-1]
    else:
        bestfit = None
        
    if quantiles == '1sigma':
        quantiles = [0.16, 0.5, 0.84]

    corner.corner(chaindf, labels=chaindf.columns, truths=bestfit, quantiles=quantiles)


def chain_dic(df):
    stat = df['FIT_STATISTIC']

    # deviance is -2*log L, which is the same as stat
    pD = np.mean(stat) - np.min(stat)
    dic = np.min(stat) + pD
    return dic

