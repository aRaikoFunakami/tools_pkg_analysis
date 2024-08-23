import pandas as pd
import sys

def calculate_totals(df):
    # region ごとに total を計算（通貨付き）
    region_totals = df.groupby('region').agg({
        'total': 'sum',
        'currency': 'first',
        'jpy_total': 'sum'
    })

    # grand total を計算
    grand_total = df['jpy_total'].sum()
    
    return region_totals, grand_total

def print_totals(region_totals, grand_total, description):
    print(f"\n{description}")
    print("Region Totals:")
    for region, data in region_totals.iterrows():
        total = int(data['total'])
        jpy_total = int(data['jpy_total'])
        print(f"{region}: {total:,} {data['currency']} ({jpy_total:,} JPY)")
    
    print("\nGrand Total:")
    print(f"{int(grand_total):,} JPY")

def main():
    if len(sys.argv) != 2:
        print("Usage: python calculate_totals.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    df = pd.read_csv(csv_file)
    
    # 現在のもの
    region_totals, grand_total = calculate_totals(df)
    print_totals(region_totals, grand_total, "Current Totals")

    # product が T4C の場合に total = total * 0.0, jpy_total = jpy_total * 0.0
    df_zeroed = df.copy()
    df_zeroed.loc[df_zeroed['product'] == 'T4C', ['total', 'jpy_total']] = 0.0
    region_totals_zeroed, grand_total_zeroed = calculate_totals(df_zeroed)
    print_totals(region_totals_zeroed, grand_total_zeroed, "Totals with T4C set to 0")

    # product が T4C の場合に total = total * 0.3, jpy_total = jpy_total * 0.3
    df_reduced = df.copy()
    df_reduced.loc[df_reduced['product'] == 'T4C', ['total', 'jpy_total']] *= 0.3
    region_totals_reduced, grand_total_reduced = calculate_totals(df_reduced)
    print_totals(region_totals_reduced, grand_total_reduced, "Totals with T4C set to 30%")

if __name__ == "__main__":
    main()
