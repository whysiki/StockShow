# from pathlib import Path


def extract_data(data_dict: dict, stock_code: str):
    # 提取 m1 数据
    m1_data = data_dict["data"][stock_code]["m1"]

    # 提取 qt 数据
    qt_data = data_dict["data"][stock_code]["qt"]

    # 提取 m1 中的所有数据，并按时间倒序排序
    m1_entries = []
    for entry in m1_data:
        timestamp = entry[0]
        m1_entry = {
            "时间戳": timestamp,
            "开盘价": entry[1],
            "收盘价": entry[2],
            "最高价": entry[3],
            "最低价": entry[4],
            "成交量": entry[5],
        }
        m1_entries.append(m1_entry)
    m1_entries.sort(key=lambda x: x["时间戳"], reverse=False)

    # 提取 qt 中的市场状态
    market_status = qt_data["market"][0]

    # 提取 qt 中的股票详细信息
    stock_details = {
        "股票名称": qt_data[stock_code][1],
        "股票代码": qt_data[stock_code][2],
        "最新价": qt_data[stock_code][3],
        "昨收": qt_data[stock_code][4],
        "开盘价": qt_data[stock_code][5],
        "成交量": qt_data[stock_code][6],
        "买入量": qt_data[stock_code][7],
        "卖出量": qt_data[stock_code][8],
        "买一价": qt_data[stock_code][9],
        "买一量": qt_data[stock_code][10],
        "买二价": qt_data[stock_code][11],
        "买二量": qt_data[stock_code][12],
        "买三价": qt_data[stock_code][13],
        "买三量": qt_data[stock_code][14],
        "买四价": qt_data[stock_code][15],
        "买四量": qt_data[stock_code][16],
        "买五价": qt_data[stock_code][17],
        "买五量": qt_data[stock_code][18],
        "卖一价": qt_data[stock_code][19],
        "卖一量": qt_data[stock_code][20],
        "卖二价": qt_data[stock_code][21],
        "卖二量": qt_data[stock_code][22],
        "卖三价": qt_data[stock_code][23],
        "卖三量": qt_data[stock_code][24],
        "卖四价": qt_data[stock_code][25],
        "卖四量": qt_data[stock_code][26],
        "卖五价": qt_data[stock_code][27],
        "卖五量": qt_data[stock_code][28],
        "时间戳": qt_data[stock_code][30],
        "涨跌额": qt_data[stock_code][31],
        "涨跌幅": qt_data[stock_code][32],
        "最高价": qt_data[stock_code][33],
        "最低价": qt_data[stock_code][34],
        "价格/成交量/成交额(元)": qt_data[stock_code][35],
        "成交量(手)": qt_data[stock_code][36],
        "成交笔数": qt_data[stock_code][37],
        "换手率": qt_data[stock_code][38],
        "市盈率(TTM)": qt_data[stock_code][39],
        "振幅": qt_data[stock_code][43],
        "总股本": qt_data[stock_code][72],
        "流通股本": qt_data[stock_code][73],
        "流通市值": qt_data[stock_code][44],
        "总市值": qt_data[stock_code][45],
        "市净率": qt_data[stock_code][46],
        "涨停": qt_data[stock_code][47],
        "涨跌": qt_data[stock_code][48],
        "量比": qt_data[stock_code][49],
        "均价": qt_data[stock_code][51],
        "市盈率(动)": qt_data[stock_code][52],
        "市盈率(静)": qt_data[stock_code][53],
    }

    return dict(
        m1_entries=m1_entries,
        market_status=[i for i in market_status.split("|")[1:] if i.strip()],
        stock_details=stock_details,
    )


if __name__ == "__main__":

    from rich import print
    from pathlib import Path

    data_dict_path = (
        Path(__file__).parent / "data" / "sh601888_m1_count0_2024_11_26_1732558830.yaml"
    )

    import yaml

    data_dict = yaml.safe_load(data_dict_path.open("r", encoding="utf-8"))

    stock_code = "sh601888"
    d = extract_data(data_dict, stock_code)

    print(d)
