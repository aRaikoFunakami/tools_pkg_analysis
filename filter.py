import pandas as pd
import os
from config import config

def read_excel_files(file_paths, sheet_name, columns, headers):
    """指定されたファイルを読み込み、必要な列を選択してヘッダーを設定する。"""
    data_frames = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist.")
            continue
        
        # エクセルファイルを読み込む
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        
        # 必要な列を選択する
        selected_columns = [col for col in columns if col < df.shape[1]]
        df = df.iloc[:, selected_columns]

        # 新しいヘッダーを設定
        df.columns = headers[:df.shape[1]]
        data_frames.append(df)
    
    return data_frames

def apply_filters(data_frames, filter_condition):
    """フィルタ条件を適用してデータフレームをフィルタリングする。"""
    filtered_data = []
    for df in data_frames:
        for column, value in filter_condition.items():
            if isinstance(value, list):
                df = df[df.iloc[:, column].isin(value)]
            else:
                df = df[df.iloc[:, column] == value]
        filtered_data.append(df)
    return filtered_data

def add_region_column(data_frames, regions):
    """地域名の列を追加する。"""
    for i, df in enumerate(data_frames):
        region_column = [regions[i]] * len(df)
        df.insert(0, 'region', region_column)
    return data_frames

def add_currency_column(data_frames, currencies, manual_rates):
    """通貨の列とJPYに換算した列を追加する。"""
    for i, df in enumerate(data_frames):
        currency_column = [currencies[i]] * len(df)
        df['currency'] = currency_column
        
        # 手動設定されたレートを使用してJPYに換算
        rate = manual_rates[currencies[i]]
        
        # JPYに換算したtotalを計算して追加
        df['jpy_total'] = df['total'] * rate
    return data_frames

def save_to_csv(data_frames, output_file):
    """データフレームをCSVファイルに保存する。"""
    if data_frames:
        result_df = pd.concat(data_frames, ignore_index=True)
        result_df.to_csv(output_file, index=False)
        print(f"Filtered data has been written to {output_file}")
    else:
        print("No data matched the filter criteria.")

def main():
    # 設定を読み込む
    path = config['path']
    files = [os.path.join(path, file) for file in config['files']]
    sheet_name = config['sheet_name']
    output_file = config['output_file']
    filter_condition = config['filter_condition']
    columns = config['columns']
    regions = config['regions']
    headers = config['headers']
    currencies = config['currency']
    manual_rates = config['manual_rates']
    
    # ファイルを読み込む
    data_frames = read_excel_files(files, sheet_name, columns, headers)

    # フィルタを適用する
    filtered_data = apply_filters(data_frames, filter_condition)
    
    # 地域名の列を追加する
    filtered_data = add_region_column(filtered_data, regions)
    
    # 通貨の列とJPYに換算した列を追加する
    filtered_data = add_currency_column(filtered_data, currencies, manual_rates)
    
    # CSVファイルに保存する
    save_to_csv(filtered_data, output_file)

if __name__ == "__main__":
    main()
