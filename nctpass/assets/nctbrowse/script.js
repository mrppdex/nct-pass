/*
var data = [
  { name: "Steering And Suspension", value: 29653 },
  { name: "Wheels And Tyres", value: 28395 },
  { name: "Side Slip Test", value: 24212 },
  { name: "Brake Test", value: 19832 }
];
*/

var margin = { top: 20, right: 30, bottom: 50, left: 40 },
  width = 600 - margin.left - margin.right,
  height = 70 * (data.length + 1) - margin.top - margin.bottom;

var binHeight = height / data.length;

var x = d3
  .scaleLinear()
  .domain([
    0,
    d3.max(data, d => {
      return d.value;
    })
  ])
  .range([0, width]);

var y = d3
  .scaleOrdinal()
  .domain(
    data.map(d => {
      return d.name;
    })
  )
  .range([0, height]);

var chart = d3
  .select("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

var xAxis = d3
  .axisBottom(x)
  .ticks(data.length)
  .tickValues(
    data.map(d => {
      return d.value;
    })
  );

var svg = chart
  .selectAll("g")
  .data(data)
  .enter()
  .append("g")
  .attr("fill", "steelblue")
  .attr("transform", function(d, i) {
    return "translate(0, " + i * binHeight + ")";
  });

var bar = svg
  .append("rect")
  .transition()
  .duration(2000)
  .ease(d3.easeBounceOut)
  .delay(function(d, i) {
    return i * 100;
  })
  .attr("width", d => {
    return x(d.value);
  })
  .attr("height", binHeight - 5)

svg
  .append("text")
  .attr("font-size", Math.round(binHeight * 0.3) + "px")
  .attr("x", d => {
    return x(d.value) - 8;
  })
  .attr("y", binHeight / 2)
  .attr("dy", "1em")
  .style("text-anchor", "end")
  .text(d => {
    return d.name;
  });

chart
  .append("g")
  .attr("class", "axis")
  .attr("transform", `translate(0, ${height})`)
  .attr("fill", "black")
  .call(xAxis)
  .selectAll("text")
  .attr("transform", "rotate(-45)")
  .style("text-anchor", "end");

svg
  .append("line")
  .attr("x1", d => {
    return x(d.value);
  })
  .attr("x2", d => {
    return x(d.value);
  })
  .attr("y1", (d, i) => {
    return binHeight;
  })
  .attr("y2", (d, i) => {
    return height - i * binHeight;
  })
  .style("stroke-width", 1)
  .style("stroke", "lightgray")
  .style("fill", "none");
