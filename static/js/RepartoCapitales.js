const getOptionChart = async () => {
  try {
    const respuesta_grafico = await fetch(
      "https://actuarial.alephsub0.org/RepartoCapitalesGrafico"
    );
    console.log(respuesta_grafico);
    return await respuesta_grafico.json();
  } catch (ex) {
    alert(ex);
  }
};

const initChart = async () => {
  const myChart = echarts.init(
    document.getElementById("chart_repartocapitales")
  );

  myChart.setOption(await getOptionChart());

  myChart.resize();
};

window.addEventListener("load", async () => {
  await initChart();
});
