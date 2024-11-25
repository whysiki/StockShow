import json
from typing import Dict, Tuple, Literal, Union, List
from curl_cffi import requests
import pandas as pd
from datetime import datetime

# from rich import print
from pathlib import Path
import time

# import pytz
import math
import functools
import yaml

# 获取上海时区
shanghai_tz = None  # pytz.timezone('Asia/Shanghai')
script_dir = Path(__file__).parent


def save_decorator(
    file_format: Union[
        List[Literal["json", "csv", "yaml"]], Literal["json", "csv", "yaml"]
    ]
):

    def save_decorator_inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kargs):
            raw_json_df_tuple = func(*args, **kargs)
            if (
                isinstance(raw_json_df_tuple, tuple)
                and len(raw_json_df_tuple) == 2
                and isinstance(raw_json_df_tuple[0], dict)
                and isinstance(raw_json_df_tuple[1], pd.DataFrame)
                and (code := kargs.get("code", None))
                and (minute_frequency := kargs.get("minute_frequency", None))
            ):
                count = kargs.get("count", 0)
                raw_json: Dict = raw_json_df_tuple[0]
                df: pd.DataFrame = raw_json_df_tuple[1]
                time_stamp = math.floor(time.time())
                prefix = f"{code}_m{minute_frequency}_count{count}_{datetime.strftime(datetime.now(shanghai_tz),r'%Y_%m_%d')}"
                raw_json_path, csv_path, yaml_path = (
                    script_dir / "data" / f"{prefix}_{time_stamp}.{ext}"
                    for ext in ("json", "csv", "yaml")
                )
                # makedirs

                for path in (csv_path, raw_json_path, yaml_path):
                    path.parent.mkdir(parents=True, exist_ok=True)

                # save
                save_fun_dict = {
                    "json": lambda: raw_json_path.write_text(
                        json.dumps(raw_json, indent=4, ensure_ascii=False),
                        encoding="UTF-8",
                    ),
                    "csv": lambda: df.to_csv(
                        csv_path,
                        mode="w",
                    ),
                    "yaml": lambda: yaml.dump(
                        raw_json,
                        yaml_path.open(mode="w", encoding="UTF-8"),
                        allow_unicode=True,
                        default_flow_style=False,
                    ),
                }
                (
                    save_fun_dict[file_format]()
                    if isinstance(file_format, str)
                    else [save_fun_dict[ext]() for ext in file_format]
                )
            return raw_json_df_tuple

        return wrapper

    return save_decorator_inner


# 腾讯分钟线
# @save_decorator(file_format=["yaml", "csv"])
def get_price_min_tx(
    *, code: str, minute_frequency: int, count: int
) -> Tuple[Dict, pd.DataFrame]:
    URL = (
        f"http://ifzq.gtimg.cn/appstock/app/kline/mkline?param={code},m{minute_frequency}"
        + (f",,{count}" if count > 0 else "")
    )
    raw_json: Dict = requests.get(URL).json()
    buf = raw_json["data"][code]["m" + str(minute_frequency)]
    df = pd.DataFrame(
        buf, columns=["time", "open", "close", "high", "low", "volume", "n1", "n2"]
    )
    df = df[["time", "open", "close", "high", "low", "volume"]]
    df[["open", "close", "high", "low", "volume"]] = df[
        ["open", "close", "high", "low", "volume"]
    ].astype("float")
    df.time = pd.to_datetime(df.time)
    df.set_index(["time"], inplace=True)
    df.index.name = ""  # 处理索引
    df.loc[df.index[-1], "close"] = float(
        raw_json["data"][code]["qt"][code][3]
    )  # 最新基金数据是3位的
    return raw_json, df


# if __name__ == "__main__":

#     # 中国中免 sh601888

#     # 南京商旅 sh600250

#     df1 = get_price_min_tx(**{"code": "sh601888", "minute_frequency": "1", "count": 0})[
#         1
#     ]

#     print(df1)
