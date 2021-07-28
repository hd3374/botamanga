from yfinance import download
import ta
import pandas as pd
import pickle
import dataframe_image as dfi



def apply_function_to_all_columns_in_second_level(df, column_second_level, function, new_column_name):
    #select second level of columns
    sub_df = df.xs(column_second_level, axis=1, level=1)
    sub_df_applied = sub_df.apply(function)
    #create MultiIndex in columns 
    sub_df_applied.columns = pd.MultiIndex.from_product([sub_df_applied.columns, [new_column_name]])
    #join to original
    return pd.concat([df, sub_df_applied], axis=1).sort_index(axis=1)


def aplicar_bbl_y_bbh(data):
    bbl = lambda close: ta.volatility.bollinger_lband(close, 20, 2.2, False)
    data_con_bbl = apply_function_to_all_columns_in_second_level(data, 'Close', bbl, 'bbl_20_22')
    bbh = lambda close: ta.volatility.bollinger_hband(close, 50, 3.0, False)
    data_con_bbl_y_bbh = apply_function_to_all_columns_in_second_level(data_con_bbl, 'Close', bbh,'bbh_50_3')
    return data_con_bbl_y_bbh

def ZScore():
    '''
    >>> Descarga datos de tickers en lista
    '''
    with open("D:\\xDocumentos\Python Trading\Robot\Data\sp500.txt", "rb") as fp:   # Unpickling
        lista = pickle.load(fp)

    data = download(tickers=lista, period='3mo', interval = '1d', threads= True, group_by='Tickers')

    '''
    >>> Acomoda el df con todos los tickers y agrega indicadores Bollinger Bands
    '''

    # TODO arreglar renombre
    df_temp = data.stack(0).reset_index()
    df = df_temp.rename(columns={'level_1': 'Ticker'})


    data_con_bbl_y_bbh = aplicar_bbl_y_bbh(data)

    # data_con_bbl_y_bbh
    # print(data_con_bbl_y_bbh)

    '''
    >>> Prepara los df con la info para mostrar
    '''

    df_high1 = data_con_bbl_y_bbh.loc[:, (slice(None), ('level_1','bbh_50_3','High','Close'))].iloc[-1:]
    df_high2 = df_high1.stack(0).reset_index()
    df_high3 = df_high2.rename(columns={'level_1': 'Ticker'})
    df_bb_high  = df_high3[df_high3['High'] >df_high3['bbh_50_3']]
    show_high = df_bb_high[['Ticker','bbh_50_3','High','Close']]

    df_low1  = data_con_bbl_y_bbh.loc[:, (slice(None), ('level_1','bbl_20_22','Low','Close'))].iloc[-1:]
    df_low2  = df_low1.stack(0).reset_index()
    df_low3 = df_low2.rename(columns={'level_1': 'Ticker'})
    df_bb_low   = df_low3[df_low3['Low'] < df_low3['bbl_20_22']]
    show_low = df_bb_low[['Ticker','bbl_20_22','Low','Close']]

    return show_high.round(2), show_low.round(2)

    '''
    >>> Da estilo al df y colvierte a png para enviar como imagen x telegram
    '''
    # show_high_styled = show_high.style.background_gradient()
    # show_low_styled = show_low.style.background_gradient()

    # dfi.export(show_high_styled,"bb_high.png")
    # dfi.export(show_low_styled,"bb_low.png")

    # photo_bb_high = open(r'D:\xDocumentos\Python Trading\bb_high.png','rb')
    # photo_bb_low = open(r'D:\xDocumentos\Python Trading\bb_low.png','rb')


if __name__ == '__main__':
    ZScore()