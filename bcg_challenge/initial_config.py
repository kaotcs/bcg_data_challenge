def initial_settings():
    '''
    Set initial settings for dataframes and plotting diplays
    '''
    # import required libraries
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from IPython.display import display, HTML

    # set cientific notation for pandas
    pd.set_option('display.float_format', '{:,.3f}'.format)

    # don't truncate columns
    pd.set_option('display.max_colwidth', None)

    # set default plt figure size
    plt.rcParams['figure.figsize'] = [10, 5]
    # set default plt font size
    plt.rcParams['font.size'] = 24

    # set cell size to be expanded
    display( HTML( '<style>.container { width:100% !important; }</style>') )

    # set figures to seaborn style
    sns.set()

    # set ggplot pallete 
    plt.style.use('ggplot')

    # set the face color globally for all axes objects
    plt.rcParams['axes.facecolor']='lightgrey'

    return None