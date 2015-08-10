width = 1200
height = 900
radius = 6

fill = d3.scale.category20()

force = d3.layout.force()
          .gravity(.02)
          .charge(-400)
          .linkDistance(60)
          .size [width, height]

svg = d3.select(".main").append('svg')
        .attr "width", width
        .attr "height", height


d3.json('graph.json', (error, graph)->
  if (error)
    throw error

  console.dir(graph)

  link = svg.selectAll('line')
            .data(graph.links)
            .enter()
            .append('line')
            .style("stroke-width", (d)-> d.value)

  node = svg.selectAll('.node')
            .data graph.nodes
            .enter()
            .append('g')
            .attr "class", "node"
            .call(force.drag)

  node.append("circle")
      .attr 'r', (d) -> d.value
      .style 'fill', (d) -> fill(d.group)
      .style 'stroke', (d)-> d3.rgb(fill(d.group)).darker()

  node.append("text")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text((d)-> d.name )

  tick = ()->
    node.attr("transform", (d)-> "translate(" + d.x + "," + d.y + ")")

    link.attr "x1", (d)-> d.source.x
        .attr "y1", (d)-> d.source.y
        .attr "x2", (d)-> d.target.x
        .attr "y2", (d)-> d.target.y

  force.nodes(graph.nodes)
       .links(graph.links)
       .on("tick", tick)
       .start()
)
