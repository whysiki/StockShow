let intradayChartInstance = null;
let dailyChartInstance = null;
let volumeChartInstance = null;

document.getElementById("queryButton").addEventListener("click", async () => {
  const stockCode = document.getElementById("stockCode").value;
  if (!stockCode) {
    alert("Please enter a stock code");
    return;
  }

  try {
    const response = await fetch(
      `http://localhost:5000/stock?code=${stockCode}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();

    console.log("API response data:", data);

    if (data.error) {
      alert(data.error);
      return;
    }

    if (!data.m1_entries || !Array.isArray(data.m1_entries)) {
      throw new Error(
        "Invalid data format: m1_entries is missing or not an array"
      );
    }

    drawIntradayChart(data.m1_entries);
    drawVolumeChart(data.m1_entries);
    drawDailyChart(data.m1_entries);
    displayStockDetails(data.stock_details);
    displayMarketStatus(data.market_status);
  } catch (error) {
    console.error("Error fetching data:", error);
    alert("Failed to fetch data");
  }
});

function drawIntradayChart(data) {
  const chartDom = document.getElementById("intradayChart");
  const myChart = echarts.init(chartDom);
  const chartData = data.map((entry) => ({
    timestamp: entry["时间戳"],
    values: [
      parseFloat(entry["开盘价"]),
      parseFloat(entry["收盘价"]),
      parseFloat(entry["最高价"]),
      parseFloat(entry["最低价"]),
    ],
  }));

  const timestamps = chartData.map((item) => item.timestamp);
  const values = chartData.map((item) => item.values);

  const option = {
    title: {
      text: "Intraday Chart",
      left: "center",
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
      },
    },
    xAxis: {
      type: "category",
      data: timestamps,
      axisLabel: {
        formatter: (value) => `${value.slice(8, 10)}:${value.slice(10, 12)}`,
      },
    },
    yAxis: {
      type: "value",
      scale: true,
    },
    series: [
      {
        name: "K线",
        type: "candlestick",
        data: values,
        itemStyle: {
          color: "#ff4d4f",
          color0: "#2ecc71",
          borderColor: "#ff4d4f",
          borderColor0: "#2ecc71",
        },
      },
    ],
  };

  myChart.setOption(option);
  myChart.on("click", () => {
    myChart.dispatchAction({
      type: "dataZoom",
      start: 0,
      end: 100,
    });
  });
}

function drawVolumeChart(data) {
  const chartDom = document.getElementById("volumeChart");
  const myChart = echarts.init(chartDom);
  const chartData = data.map((entry) => ({
    timestamp: entry["时间戳"],
    volume: parseFloat(entry["成交量"]),
  }));

  const timestamps = chartData.map((item) => item.timestamp);
  const volumes = chartData.map((item) => item.volume);

  const option = {
    title: {
      text: "Volume Chart",
      left: "center",
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
      },
    },
    xAxis: {
      type: "category",
      data: timestamps,
      axisLabel: {
        formatter: (value) => `${value.slice(8, 10)}:${value.slice(10, 12)}`,
      },
    },
    yAxis: {
      type: "value",
      scale: true,
    },
    series: [
      {
        name: "Volume",
        type: "bar",
        data: volumes,
        itemStyle: {
          color: "#007bff",
        },
      },
    ],
  };

  myChart.setOption(option);
  myChart.on("click", () => {
    myChart.dispatchAction({
      type: "dataZoom",
      start: 0,
      end: 100,
    });
  });
}

function drawDailyChart(data) {
  const chartDom = document.getElementById("dailyChart");
  const myChart = echarts.init(chartDom);
  const chartData = data.map((entry) => ({
    timestamp: entry["时间戳"].slice(0, 8),
    values: [
      parseFloat(entry["开盘价"]),
      parseFloat(entry["收盘价"]),
      parseFloat(entry["最高价"]),
      parseFloat(entry["最低价"]),
    ],
  }));

  const timestamps = chartData.map((item) => item.timestamp);
  const values = chartData.map((item) => item.values);

  const option = {
    title: {
      text: "Daily Chart",
      left: "center",
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
      },
    },
    xAxis: {
      type: "category",
      data: timestamps,
      axisLabel: {
        formatter: (value) =>
          `${value.slice(0, 4)}-${value.slice(4, 6)}-${value.slice(6, 8)}`,
      },
    },
    yAxis: {
      type: "value",
      scale: true,
    },
    series: [
      {
        name: "K线",
        type: "candlestick",
        data: values,
        itemStyle: {
          color: "#ff4d4f",
          color0: "#2ecc71",
          borderColor: "#ff4d4f",
          borderColor0: "#2ecc71",
        },
      },
    ],
  };

  myChart.setOption(option);
  myChart.on("click", () => {
    myChart.dispatchAction({
      type: "dataZoom",
      start: 0,
      end: 100,
    });
  });
}

function displayStockDetails(details) {
  const detailsContainer = document.getElementById("stockDetails");
  detailsContainer.innerHTML = `
    <tr>
      <td>${details["股票名称"]}</td>
      <td>${details["股票代码"]}</td>
      <td>${details["最新价"]}</td>
      <td>${details["昨收"]}</td>
      <td>${details["开盘价"]}</td>
      <td>${details["成交量"]}</td>
      <td>${details["市净率"]}</td>
      <td>${details["涨停"]}</td>
      <td>${details["涨跌"]}</td>
      <td>${details["量比"]}</td>
      <td>${details["均价"]}</td>
      <td>${details["市盈率(动)"]}</td>
      <td>${details["市盈率(静)"]}</td>
    </tr>
  `;

  const detailsContainer2 = document.getElementById("stockDetails2");
  detailsContainer2.innerHTML = `
    <tr>
      <td>${details["买入量"]}</td>
      <td>${details["卖出量"]}</td>
      <td>${details["涨跌额"]}</td>
      <td>${details["涨跌幅"]}</td>
      <td>${details["最高价"]}</td>
      <td>${details["最低价"]}</td>
    </tr>
  `;

  const detailsContainer3 = document.getElementById("stockDetails3");
  detailsContainer3.innerHTML = `
    <tr>
      <td>${details["价格/成交量/成交额(元)"]}</td>
      <td>${details["成交量(手)"]}</td>
      <td>${details["成交笔数"]}</td>
      <td>${details["换手率"]}</td>
      <td>${details["市盈率(TTM)"]}</td>
      <td>${details["振幅"]}</td>
    </tr>
  `;

  const detailsContainer4 = document.getElementById("stockDetails4");
  detailsContainer4.innerHTML = `
    <tr>
      <td>${details["总股本"]}</td>
      <td>${details["流通股本"]}</td>
      <td>${details["总市值"]}</td>
      <td>${details["流通市值"]}</td>
    </tr>
  `;

  displayTopBuySell(details);
}

function displayTopBuySell(details) {
  const topBuySellContainer = document.getElementById("topBuySell");
  topBuySellContainer.innerHTML = `
    <div class="row">
      <div class="col s6">
        <h3>Buy</h3>
        <ul>
          <li>${details["买一价"]} (${details["买一量"]})</li>
          <li>${details["买二价"]} (${details["买二量"]})</li>
          <li>${details["买三价"]} (${details["买三量"]})</li>
          <li>${details["买四价"]} (${details["买四量"]})</li>
          <li>${details["买五价"]} (${details["买五量"]})</li>
        </ul>
      </div>
      <div class="col s6">
        <h3>Sell</h3>
        <ul>
          <li>${details["卖一价"]} (${details["卖一量"]})</li>
          <li>${details["卖二价"]} (${details["卖二量"]})</li>
          <li>${details["卖三价"]} (${details["卖三量"]})</li>
          <li>${details["卖四价"]} (${details["卖四量"]})</li>
          <li>${details["卖五价"]} (${details["卖五量"]})</li>
        </ul>
      </div>
    </div>
  `;
}

function displayMarketStatus(status) {
  const statusContainer = document.getElementById("marketStatus");
  statusContainer.innerHTML = `
    <ul>
      ${status.map((s) => `<li>${s}</li>`).join("")}
    </ul>
  `;
}

// 定时更新数据
setInterval(async () => {
  const stockCode = document.getElementById("stockCode").value;
  if (stockCode) {
    try {
      const response = await fetch(
        `http://localhost:5000/stock?code=${stockCode}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      console.log("API response data (interval):", data);

      if (data.error) {
        console.error(data.error);
        return;
      }

      if (!data.m1_entries || !Array.isArray(data.m1_entries)) {
        throw new Error(
          "Invalid data format: m1_entries is missing or not an array"
        );
      }

      drawIntradayChart(data.m1_entries);
      drawVolumeChart(data.m1_entries);
      drawDailyChart(data.m1_entries);
      displayStockDetails(data.stock_details);
      displayMarketStatus(data.market_status);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
}, 60000); // 每分钟更新一次
