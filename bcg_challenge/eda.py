##############################
####### INITIAL CONFIG #######
##############################

# import required library to configure module
from bcg_challenge.initial_config import initial_settings

# set the basic cofiguration for this module
initial_settings()

################################
####### MODULE FUNCTIONS #######
################################


def numerical_plot( dataframe, column, figsize = (8, 7), hist = True ):
    '''
    Plot histogram (or kde) on the hist_axs and boxplot on the box_axs
    
    Args
        dataframe: datataframe with numerical features
        column: numerical feature to be plotted
        figsize: tuple with figsize (width, height) in inches
        hist: boolean to indicate if user wants a histplot or a kdeplot.
            This may be useful when histplot is too slow.
    
    Return
        None: a None Type object
    '''

    # import required libraries
    import matplotlib.pyplot as     plt
    from   matplotlib        import gridspec 
    import seaborn           as     sns
       
    # create a figure object
    fig = plt.figure( figsize = (8, 7), constrained_layout = True );

    # create a grid for plotting
    specs = gridspec.GridSpec( ncols = 1, nrows = 2, figure = fig);

    # check sales distribution
    hist_axs = fig.add_subplot( specs[ 0, 0 ] )
    box_axs = fig.add_subplot( specs[ 1, 0 ] )

    # check if user wants histplot
    if hist:
        # set title
        hist_axs.set_title( column.upper() )
        # plot histogram
        sns.histplot( x = column, data = dataframe, ax = hist_axs, kde = True )

    # in case user want kdeplot instead of histplot
    else:
        # set title
        hist_axs.set_title( column.upper() )
        # plot kdeplot
        sns.kdeplot( x = column, data = dataframe, ax = hist_axs, fill = True )

    # set title
    box_axs.set_title( column.upper() )

    # plot boxplot
    sns.boxplot(  x = column, data = dataframe, ax = box_axs )

    
    return None


def categorical_plot( df_cat, n_cols = 3, countplot = True, figsize = None ):
    '''
    Plot histogram for all features in the dataframe. 
    Dataframe is supposed to have only categorical features.
    
    Args
        df_cat: datataframe with categorical features
        n_cols: is a integer with the number of columns on the final chart
        countplot: a boolean to indicate if user wants to plot a countplot (count = True)
            or a histplot (countplot = False)
        figsize: tuple with figsize (width, height) in inches       
    
    Return
        None
    '''

    # import required libraries
    import matplotlib.pyplot as plt
    from matplotlib import gridspec
    import seaborn as sns

    # define number of rows
    n_rows = df_cat.shape[1] // n_cols + 1
    
    # check if user input figsize
    if figsize is None:
        # assign th default figsize
        figsize = (n_cols*4.5, n_rows*4.5)
    
    # create a figure object
    fig = plt.figure( figsize = figsize, constrained_layout = True )

    # create grid for plotting
    specs = gridspec.GridSpec( ncols = n_cols, nrows = n_rows, figure = fig)

    # iterate over column to plot countplot figure
    for index, column in enumerate( df_cat.columns ):
        # create a subplot to plot the given feature
        ax1 = fig.add_subplot( specs[index // n_cols, index % n_cols] )
        # set the title for the subplot
        ax1.set_title( column.upper() )
        # check if user wants a countplot
        if countplot:
            # plot countplot
            sns.countplot( x = column, data = df_cat, ax = ax1 )
        # user wants a histplot
        else:
            # plot histplot
            sns.histplot( x = column, data = df_cat, ax = ax1 )
        # rotate x ticks
        plt.xticks( rotation = 90 );
        
    
    return None


def cramer_v_corrected_stat( series_one, series_two ):
    '''
    Calculate crame v statistics for two categorical series 
    
    Args:
        series_one: first categorical dataframe column
        series_two: second categorical dataframe column
    
    Return:
        corr_cramer_v: corrected Cramer-V statistic

    NOTE: This implementation doesn't handle missing value (e.g. np.nan). It will raise warnings in this case.
    '''
    # import required libraries
    import numpy as np
    import pandas as pd
    from scipy.stats import chi2_contingency

    # create confusion matrix
    cm = pd.crosstab( series_one, series_two )
    # calculate the sum along all dimensions
    n = cm.sum().sum()
    # calculate number of row and columns of confusion matrix
    r, k = cm.shape

    # calculate chi_squared statistics
    chi2 = chi2_contingency( cm )[0]
    
    # calculate chi_squared correction
    chi2corr = max( 0, chi2 - (k-1)*(r-1)/(n-1) )
    # calculate k correction
    kcorr = k - (k-1)**2/(n-1)
    # calculate r correction
    rcorr = r - (r-1)**2/(n-1)

    # calculate corrected cramer-v
    corr_cramer_v = np.sqrt( (chi2corr/n) / ( min( kcorr-1, rcorr-1 ) ) )
   
    
    return corr_cramer_v


def create_cramer_v_dataframe( categ_features_analysis_dataframe ):
    '''
    Create a correlation matrix for features on categorical dataframe
    
    Args:
        categ_features_analysis_dataframe: dataframe with only categorical features
    
    Return:
        categ_corr_matrix: dataframe with cramer-v for every row-column pair 
                           in the input dataframe'''
    # import required libraries
    import numpy as np
    import pandas as pd
    
    # create final dataframe skeleton
    df_cramer_v = pd.DataFrame( columns = categ_features_analysis_dataframe.columns, 
                                index = categ_features_analysis_dataframe.columns )

    # fill final dataframe with cramer-v statistics for every row-column pair
    for row in df_cramer_v:
        for column in df_cramer_v:   
            df_cramer_v.loc[row, column] = float( cramer_v_corrected_stat( categ_features_analysis_dataframe[ row ],
                                                                           categ_features_analysis_dataframe[ column] ) )

    # ensure cramer-v is float
    categ_corr_matrix = df_cramer_v.astype( 'float' )
        
        
    return categ_corr_matrix


def plot_spearman_heatmap(df_num, figsize = None, saving_path = None):
    """Calculate and plot the correlation matrix of all columns in df_num 
    using Spearman correlation coefficient (so as to get non-linear relationships).
    
    Args
        df_num: a pandas dataframe with numerical columns only.
        figsize: a tuple with the figure size (width, height) in case user wants to save it.
        saving_path: a string with the path to save heatmap in case user wants to save it.
    
    Return
        df_spearman_corr: a pandas dataframe with spearman correlation coefficient among features.
    """

    # import required libraries
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    # checking df_num type
    assert type( df_num ) == pd.DataFrame, "df_num must be a pandas dataframe!"
    # check if a figsize as defined
    if figsize is not None:
        # check figsize type          
        assert type( figsize ) == tuple, "figsize must be a tuple!"
    # check if a figsize as defined
    if saving_path is not None:
        # check figsize type          
        assert type( saving_path ) == str, "saving_path must be a string!"

    # calculate spearman correlation for numerical features
    df_spearman_corr = df_num.corr( method = 'spearman' ) # get non-linear relationships

    # check if user set a figsize
    if figsize is None:
        # define figure size reference
        fig_size_ref = df_num.shape[1]
        # define a multiplier
        multiplier = 0.75
        # define fig_size variable
        figsize = (multiplier*fig_size_ref, multiplier*fig_size_ref)

    # create figure and ax object
    fig, ax = plt.subplots( figsize = figsize)

    # display heatmap of correlation on figure
    sns.heatmap(df_spearman_corr, annot = True, 
                vmin = -1, vmax = 1, center = 0, square = True,
                ax = ax, cmap = sns.diverging_palette(20, 220, n=256)
               )
    # define figure details
    plt.title("SPEARMAN CORRELATION COEFFICIENT")
    plt.yticks( rotation = 0 );

    # check if user want to save heatmap
    if saving_path is not None:
        # save figure to inspect outside notebook
        plt.savefig( saving_path, dpi=200, transparent=False, 
                    bbox_inches="tight", facecolor='white')

    
    return df_spearman_corr


def plot_cramer_v_heatmap(df_cat, figsize = None, saving_path = None):
    """Calculate and plot the correlation matrix of all columns in df_cat
    using corrected cramer-v correlation coefficient.
    
    Args
        df_cat: a pandas dataframe with categorical columns only.
        figsize: a tuple with the figure size (width, height) in case user wants to save it.
        saving_path: a string with the path to save heatmap in case user wants to save it.
    
    Return
        df_cramer_v_corr: a pandas dataframe with corrected cramer-v correlation coefficient among features.
    """

    # import required libraries
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    # checking df_num type
    assert type( df_cat ) == pd.DataFrame, "df_cat must be a pandas dataframe!"
    # check if a figsize as defined
    if figsize is not None:
        # check figsize type          
        assert type( figsize ) == tuple, "figsize must be a tuple!"
    # check if a figsize as defined
    if saving_path is not None:
        # check figsize type          
        assert type( saving_path ) == str, "saving_path must be a string!"

    # create a dataframe with cramer-v for every row-column pair
    df_cramer_v_corr = create_cramer_v_dataframe( df_cat )

    # check if user set a figsize
    if figsize is None:
        # define figure size reference
        fig_size_ref = df_cat.shape[1]
        # define a multiplier
        multiplier = 0.75
        # define fig_size variable
        figsize = (multiplier*fig_size_ref, multiplier*fig_size_ref)

    # create figure and ax object
    fig, ax = plt.subplots( figsize = figsize)

    # display heatmap of correlation on figure
    sns.heatmap( df_cramer_v_corr, annot = True, 
                vmin = 0, vmax = 1, center = 0.5, square = True,
                ax = ax, cmap = sns.diverging_palette(20, 220, n=256)
               )
    # define figure details
    plt.title("SPEARMAN CORRELATION COEFFICIENT")
    plt.yticks( rotation = 0 );


    # check if user want to save heatmap
    if saving_path is not None:
        # save figure to inspect outside notebook
        plt.savefig( saving_path, dpi=200, transparent=False, 
                    bbox_inches="tight", facecolor='white')


    return df_cramer_v_corr


def correlation_tests( array_one, array_two ):
    """Calculate pearson correlation test and spearman correlation test to check
    linear and non-linear independence between two arrays of numeric values.

    Args
        array_one: a numpy ndarray with first sequence of values
        array_two: a numpy ndarray with second sequence of values

    Return
        pearson_correlation: a float with the pearson correlation coefficient 
        pearson_pvalue: a float with the p-value for the pearson correlation test 
        spearman_test: a float with the spearman correlation coefficient 
        spearman_test.pvalue: a float with the p-value for the spearman correlation test 
    """
    
    # import required libraries
    import numpy as np
    from scipy.stats import pearsonr, spearmanr

    # checking df_num type
    assert isinstance(array_one, np.ndarray ), "array_one must be a numpy ndarray!"
    assert isinstance(array_two, np.ndarray ), "array_one must be a numpy ndarray!"

    ################################
    ####### CORRELATION TEST #######
    ################################

    ####### LINEARITY #######
    # do spearman correlation test
    pearson_correlation, pearson_pvalue = pearsonr(array_one, array_two)

    # print report
    print("\t", "\033[91m", "PEARSON CORRELATION TEST", "\033[0m", "\n\n\n",
        "\033[1m", "NULL HYPOTHESIS: two sets of data are uncorrelated.", "\033[0m", "\n\n",
        "\033[1m", "Calculated p-value assumes that each dataset is normally distributed.", "\033[0m", "\n\n",      
        "\033[1m", f"Pearson correlation coef: {pearson_correlation:.3f}", "\033[0m", "\n\n",
        "\033[1m", f"p-value: {pearson_pvalue:.3f}", "\033[0m", "\n",
        )


    ####### NON-LINEARITY #######
    # do spearman correlation test
    spearman_test = spearmanr(array_one, array_two)

    # print report
    print("\t", "\033[91m", "SPEARMAN CORRELATION TEST", "\033[0m", "\n\n\n",
        "\033[1m", "NULL HYPOTHESIS: two sets of data are uncorrelated.", "\033[0m", "\n\n",
        "\033[1m", "Nonparametric test. It does NOT assume that both datasets are normally distributed.", "\033[0m", "\n\n",      
        "\033[1m", f"Spearman correlation coef: {spearman_test.correlation:.3f}", "\033[0m", "\n\n",
        "\033[1m", f"p-value: {spearman_test.pvalue:.3f}", "\033[0m", "\n",
        )

    return pearson_correlation, pearson_pvalue, spearman_test.correlation, spearman_test.pvalue