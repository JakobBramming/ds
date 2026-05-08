const year = document.querySelector("#year");

if (year) {
  year.textContent = new Date().getFullYear();
}

const thesisData = [
  { window: 15, internal: 54, rideTime: 4.0, distance: 109 },
  { window: 30, internal: 65, rideTime: 6.0, distance: 106 },
  { window: 45, internal: 74, rideTime: 9.0, distance: 103 },
  { window: 60, internal: 80, rideTime: 12.4, distance: 100 },
  { window: 75, internal: 85, rideTime: 16.0, distance: 98 },
  { window: 90, internal: 88, rideTime: 20.0, distance: 96 },
  { window: 105, internal: 90, rideTime: 25.0, distance: 95 },
  { window: 120, internal: 91, rideTime: 30.0, distance: 94 },
];

const objectiveData = {
  15: [
    { label: "Min. distance", internal: 51, rideTime: 3.6, className: "distance" },
    { label: "Min. time", internal: 53, rideTime: 3.9, className: "time" },
    { label: "Max. slack", internal: 54, rideTime: 4.0, className: "slack" },
  ],
  30: [
    { label: "Min. distance", internal: 61, rideTime: 5.2, className: "distance" },
    { label: "Min. time", internal: 63, rideTime: 5.6, className: "time" },
    { label: "Max. slack", internal: 65, rideTime: 6.0, className: "slack" },
  ],
  45: [
    { label: "Min. distance", internal: 70, rideTime: 8.1, className: "distance" },
    { label: "Min. time", internal: 72, rideTime: 8.4, className: "time" },
    { label: "Max. slack", internal: 74, rideTime: 9.0, className: "slack" },
  ],
  60: [
    { label: "Min. distance", internal: 76, rideTime: 10.2, className: "distance" },
    { label: "Min. time", internal: 78, rideTime: 11.0, className: "time" },
    { label: "Max. slack", internal: 80, rideTime: 12.4, className: "slack" },
  ],
  75: [
    { label: "Min. distance", internal: 81, rideTime: 13.5, className: "distance" },
    { label: "Min. time", internal: 83, rideTime: 14.6, className: "time" },
    { label: "Max. slack", internal: 85, rideTime: 16.0, className: "slack" },
  ],
  90: [
    { label: "Min. distance", internal: 84, rideTime: 17.0, className: "distance" },
    { label: "Min. time", internal: 86, rideTime: 18.4, className: "time" },
    { label: "Max. slack", internal: 88, rideTime: 20.0, className: "slack" },
  ],
  105: [
    { label: "Min. distance", internal: 86, rideTime: 21.0, className: "distance" },
    { label: "Min. time", internal: 88, rideTime: 23.0, className: "time" },
    { label: "Max. slack", internal: 90, rideTime: 25.0, className: "slack" },
  ],
  120: [
    { label: "Min. distance", internal: 87, rideTime: 25.0, className: "distance" },
    { label: "Min. time", internal: 89, rideTime: 27.0, className: "time" },
    { label: "Max. slack", internal: 91, rideTime: 30.0, className: "slack" },
  ],
};

const svgNamespace = "http://www.w3.org/2000/svg";
const windowSlider = document.querySelector("#time-window");
const windowValue = document.querySelector("#window-value");
const currentWindow = document.querySelector("#current-window");
const sensitivityChart = document.querySelector("#sensitivity-chart");
const tradeoffChart = document.querySelector("#tradeoff-chart");
const objectiveChart = document.querySelector("#objective-chart");
const internalValue = document.querySelector("#internal-value");
const outsourcedValue = document.querySelector("#outsourced-value");
const rideTimeValue = document.querySelector("#ride-time-value");
const distanceValue = document.querySelector("#distance-value");

function createSvgElement(name, attributes = {}) {
  const element = document.createElementNS(svgNamespace, name);

  Object.entries(attributes).forEach(([key, value]) => {
    element.setAttribute(key, value);
  });

  return element;
}

function scale(value, inputMin, inputMax, outputMin, outputMax) {
  const progress = (value - inputMin) / (inputMax - inputMin);
  return outputMin + progress * (outputMax - outputMin);
}

function clearSvg(svg) {
  if (svg) {
    svg.replaceChildren();
  }
}

function addText(svg, text, x, y, className, anchor = "middle") {
  const label = createSvgElement("text", {
    x,
    y,
    class: className,
    "text-anchor": anchor,
  });
  label.textContent = text;
  svg.append(label);
}

function drawAxes(svg, bounds, leftTicks, rightTicks) {
  leftTicks.forEach((tick) => {
    const y = scale(tick, 40, 100, bounds.bottom, bounds.top);
    svg.append(createSvgElement("line", {
      x1: bounds.left,
      x2: bounds.right,
      y1: y,
      y2: y,
      class: "chart-grid",
    }));
    addText(svg, `${tick}%`, bounds.left - 14, y + 5, "axis-label green", "end");
  });

  rightTicks.forEach((tick) => {
    const y = scale(tick, 0, 35, bounds.bottom, bounds.top);
    addText(svg, `${tick}m`, bounds.right + 16, y + 5, "axis-label gold", "start");
  });

  svg.append(createSvgElement("line", {
    x1: bounds.left,
    x2: bounds.left,
    y1: bounds.top,
    y2: bounds.bottom,
    class: "axis-line",
  }));
  svg.append(createSvgElement("line", {
    x1: bounds.left,
    x2: bounds.right,
    y1: bounds.bottom,
    y2: bounds.bottom,
    class: "axis-line",
  }));
}

function drawSensitivityChart(selectedWindow) {
  clearSvg(sensitivityChart);

  if (!sensitivityChart) {
    return;
  }

  const bounds = { left: 78, right: 830, top: 26, bottom: 292 };
  const step = (bounds.right - bounds.left) / thesisData.length;
  const barWidth = step * 0.7;
  const points = [];

  drawAxes(sensitivityChart, bounds, [40, 50, 60, 70, 80, 90, 100], [0, 5, 10, 15, 20, 25, 30, 35]);

  thesisData.forEach((item, index) => {
    const centerX = bounds.left + step * index + step / 2;
    const barHeight = scale(item.internal, 40, 100, 0, bounds.bottom - bounds.top);
    const y = bounds.bottom - barHeight;
    const rideY = scale(item.rideTime, 0, 35, bounds.bottom, bounds.top);

    sensitivityChart.append(createSvgElement("rect", {
      x: centerX - barWidth / 2,
      y,
      width: barWidth,
      height: barHeight,
      rx: 5,
      class: item.window === selectedWindow ? "completion-bar selected" : "completion-bar",
    }));

    addText(sensitivityChart, `${item.window}m`, centerX, bounds.bottom + 28, "axis-label");
    points.push(`${centerX},${rideY}`);
  });

  sensitivityChart.append(createSvgElement("polyline", {
    points: points.join(" "),
    class: "ride-line",
  }));

  thesisData.forEach((item, index) => {
    const centerX = bounds.left + step * index + step / 2;
    const rideY = scale(item.rideTime, 0, 35, bounds.bottom, bounds.top);

    sensitivityChart.append(createSvgElement("circle", {
      cx: centerX,
      cy: rideY,
      r: item.window === selectedWindow ? 7 : 5,
      class: "ride-point",
    }));
  });
}

function drawTradeoffChart() {
  clearSvg(tradeoffChart);

  if (!tradeoffChart) {
    return;
  }

  const bounds = { left: 62, right: 420, top: 22, bottom: 250 };
  const completionPoints = [];
  const ridePoints = [];

  drawAxes(tradeoffChart, bounds, [40, 50, 60, 70, 80, 90, 100], [0, 5, 10, 15, 20, 25, 30, 35]);

  thesisData.forEach((item, index) => {
    const x = scale(index, 0, thesisData.length - 1, bounds.left, bounds.right);
    completionPoints.push(`${x},${scale(item.internal, 40, 100, bounds.bottom, bounds.top)}`);
    ridePoints.push(`${x},${scale(item.rideTime, 0, 35, bounds.bottom, bounds.top)}`);
    addText(tradeoffChart, `${item.window}m`, x, bounds.bottom + 26, "axis-label");
  });

  tradeoffChart.append(createSvgElement("polyline", {
    points: completionPoints.join(" "),
    fill: "none",
    stroke: "#0f766e",
    "stroke-width": 3,
  }));
  tradeoffChart.append(createSvgElement("polyline", {
    points: ridePoints.join(" "),
    fill: "none",
    stroke: "#d85d45",
    "stroke-width": 3,
  }));
}

function drawObjectiveChart(selectedWindow) {
  clearSvg(objectiveChart);

  if (!objectiveChart) {
    return;
  }

  const data = objectiveData[selectedWindow];
  const bounds = { left: 60, right: 430, top: 24, bottom: 242 };
  const colors = {
    distance: { fill: "rgba(59, 130, 214, 0.28)", stroke: "#3b82d6" },
    time: { fill: "rgba(15, 118, 110, 0.25)", stroke: "#0f766e" },
    slack: { fill: "rgba(197, 144, 45, 0.28)", stroke: "#c5902d" },
  };

  [0, 20, 40, 60, 80, 100].forEach((tick) => {
    const y = scale(tick, 0, 100, bounds.bottom, bounds.top);
    objectiveChart.append(createSvgElement("line", {
      x1: bounds.left,
      x2: bounds.right,
      y1: y,
      y2: y,
      class: "chart-grid",
    }));
    addText(objectiveChart, `${tick}`, bounds.left - 12, y + 5, "axis-label", "end");
  });

  objectiveChart.append(createSvgElement("line", {
    x1: bounds.left,
    x2: bounds.right,
    y1: bounds.bottom,
    y2: bounds.bottom,
    class: "axis-line",
  }));

  const groups = [
    { label: "Internal completion", key: "internal", x: 118, scaleMax: 100 },
    { label: "Excess ride time", key: "rideTime", x: 305, scaleMax: 35 },
  ];

  groups.forEach((group) => {
    data.forEach((item, index) => {
      const color = colors[item.className];
      const value = item[group.key];
      const height = scale(value, 0, group.scaleMax, 0, bounds.bottom - bounds.top);
      const x = group.x + index * 36;

      objectiveChart.append(createSvgElement("rect", {
        x,
        y: bounds.bottom - height,
        width: 30,
        height,
        rx: 4,
        fill: color.fill,
        stroke: color.stroke,
        "stroke-width": 2,
      }));
    });

    addText(objectiveChart, group.label, group.x + 52, bounds.bottom + 28, "axis-label");
  });
}

function updateDashboard(selectedWindow) {
  const selected = thesisData.find((item) => item.window === selectedWindow);

  if (!selected) {
    return;
  }

  const distanceDelta = selected.distance - 100;
  const distanceLabel = distanceDelta === 0
    ? "Baseline"
    : `${distanceDelta > 0 ? "+" : ""}${distanceDelta}%`;

  windowValue.textContent = `${selected.window} min`;
  currentWindow.textContent = `current = ${selected.window} min`;
  internalValue.textContent = `${selected.internal}%`;
  outsourcedValue.textContent = `${100 - selected.internal}%`;
  rideTimeValue.textContent = `${selected.rideTime.toFixed(1)} min`;
  distanceValue.textContent = distanceLabel;

  drawSensitivityChart(selected.window);
  drawObjectiveChart(selected.window);
}

if (windowSlider) {
  drawTradeoffChart();
  updateDashboard(Number(windowSlider.value));
  windowSlider.addEventListener("input", () => updateDashboard(Number(windowSlider.value)));
}
