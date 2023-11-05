#set text(
    size: 11pt,
    font: "New Computer Modern"
)

#set page(
    paper: "us-letter",
    margin: 1in,
    footer: [
        #set align(left)
        #smallcaps("Advanced Computer Architecture")
        #h(1fr)
        #counter(page).display(
            "1",
        )
    ]
)

#set heading(
    numbering: "1.a.",
)

#set terms(
    tight: false,
    separator: text[ -- ],
    indent: 1em,
    hanging-indent: 2em,

)

#set align(center)
#set heading(numbering: none)

#import "@preview/plotst:0.2.0": * 

== University of Central Florida
== Department of Computer Science
== CDA 5106: Fall 2023
== #datetime.today().display("[month repr:long] [day], [year]")
== Machine Problem 1: Cache Design, Memory Hierarchy Design

#v(50pt)

== by

#v(30pt)

== Andey Taylor Robins

#v(70pt)


#box(stroke: black, radius: 10pt, inset: 20pt)[#set align(left)
Honor Pledge: "I have neither given nor received unauthorized aid on this test or assignment."

Student's electronic signature: #underline[Andey Taylor Robins]]

#pagebreak()
#set heading(
    numbering: "1.a.",
)
#set align(left)

= L1 Cache Exploration: Size and Associativity

#let exp1a_plot() = {
  /* sizes: 1024, 2048, 4096, 8192, 16_384, 32_768, 65_536, 131_072, 262_144, 524_288, 1_048_576 */

  let assoc_1_data = ((10, 19.346), (11, 14.774), (12, 10.017), (13, 6.700), (14, 4.609), (15, 3.768), (16, 3.292), (17, 3.233), (18, 2.584), (19, 2.584), (20, 2.584))
  
  let assoc_2_data = ((10, 15.603), (11, 10.714), (12, 7.528), (13, 4.734), (14, 3.384), (15, 2.881), (16, 2.713), (17, 2.590), (18, 2.584), (19, 2.582), (20, 2.582))
  
  let assoc_4_data = ((10, 14.270), (11, 9.622), (12, 5.992), (13, 4.247), (14, 2.832), (15, 2.640), (16, 2.595), (17, 2.582), (18, 2.582), (19, 2.582), (20, 2.582))
  
  let assoc_8_data = ((10, 13.627), (11, 9.069), (12, 5.365), (13, 3.954), (14, 2.774), (15, 2.625), (16, 2.589), (17, 2.582), (18, 2.582), (19, 2.582), (20, 2.582))
  
  let assoc_full_data = ((10, 13.696), (11, 8.860), (12, 4.954), (13, 3.912), (14, 2.634), (15, 2.624), (16, 2.582), (17, 2.582), (18, 2.582), (19, 2.582), (20, 2.582))

  let x_axis = axis(min: 10, max: 20, step: 1, location: "bottom", title: [$log_2($L1 Cache Size$)$])
  let y_axis = axis(min: 0, max: 24, step: 4, location: "left", helper_lines: false, title: [Miss Rate (% Misses)])
  
  let p1 = plot(data: assoc_1_data, axes: (x_axis, y_axis))
  let p2 = plot(data: assoc_2_data, axes: (x_axis, y_axis))
  let p3 = plot(data: assoc_4_data, axes: (x_axis, y_axis))
  let p4 = plot(data: assoc_8_data, axes: (x_axis, y_axis))
  let p5 = plot(data: assoc_full_data, axes: (x_axis, y_axis))
  
  let g1 = graph_plot(p1, stroke: black, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and miss rate", markings: [#emoji.rocket])
  let g2 = graph_plot(p2, stroke: blue, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and miss rate", markings: [#emoji.rocket])
  let g3 = graph_plot(p3, stroke: red, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and miss rate", markings: [#emoji.rocket])
  let g4 = graph_plot(p4, stroke: purple, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and miss rate", markings: [#emoji.rocket])
  let g5 = graph_plot(p5, stroke: orange, (100%, 25%), rounding: 10%, caption: "Relation between cache size, associativity, and miss rate", markings: [#emoji.rocket])
  
  overlay((g1, g2, g3, g4, g5), (90%, 30%))
}

#let exp1b_plot() = {
  /* sizes: 1024, 2048, 4096, 8192, 16_384, 32_768, 65_536, 131_072, 262_144, 524_288, 1_048_576 */

  let ht_l1_1 = 0.114797
  let ht_l1_2 = 0.140329
  let ht_l1_4 = 0.14682
  let ht_l1_fa = 0.155484
  let miss_penalty = 100

  let assoc_1_data = ((10, ht_l1_1 + miss_penalty * 0.19346), (11, ht_l1_1 + miss_penalty * 0.14774), (12, ht_l1_1 + miss_penalty * 0.10017), (13, ht_l1_1 + miss_penalty * 0.06700), (14, ht_l1_1 + miss_penalty * 0.04609), (15, ht_l1_1 + miss_penalty * 0.03768), (16, ht_l1_1 + miss_penalty * 0.03292), (17, ht_l1_1 + miss_penalty * 0.03233), (18, ht_l1_1 + miss_penalty * 0.02584), (19, ht_l1_1 + miss_penalty * 0.02584), (20, ht_l1_1 + miss_penalty * 0.02584))
  
  let assoc_2_data = ((10, ht_l1_2 + miss_penalty * 0.15603), (11, ht_l1_2 + miss_penalty * 0.10714), (12, ht_l1_2 + miss_penalty * 0.07528), (13, ht_l1_2 + miss_penalty * 0.04734), (14, ht_l1_2 + miss_penalty * 0.03384), (15, ht_l1_2 + miss_penalty * 0.02881), (16, ht_l1_2 + miss_penalty * 0.02713), (17, ht_l1_2 + miss_penalty * 0.02590), (18, ht_l1_2 + miss_penalty * 0.02584), (19, ht_l1_2 + miss_penalty * 0.02582), (20, ht_l1_2 + miss_penalty * 0.02582))
  
  let assoc_4_data = ((10, ht_l1_4 + miss_penalty * 0.14270), (11, ht_l1_4 + miss_penalty * 0.09622), (12, ht_l1_4 + miss_penalty * 0.05992), (13, ht_l1_4 + miss_penalty * 0.04247), (14, ht_l1_4 + miss_penalty * 0.02832), (15, ht_l1_4 + miss_penalty * 0.02640), (16, ht_l1_4 + miss_penalty * 0.02595), (17, ht_l1_4 + miss_penalty * 0.02582), (18, ht_l1_4 + miss_penalty * 0.02582), (19, ht_l1_4 + miss_penalty * 0.02582), (20, ht_l1_4 + miss_penalty * 0.02582))
  
  let assoc_full_data = ((10, ht_l1_fa + miss_penalty * 0.13696), (11, ht_l1_fa + miss_penalty * 0.08860), (12, ht_l1_fa + miss_penalty * 0.04954), (13, ht_l1_fa + miss_penalty * 0.03912), (14, ht_l1_fa + miss_penalty * 0.02634), (15, ht_l1_fa + miss_penalty * 0.02582), (16, ht_l1_fa + miss_penalty * 0.02582), (17, ht_l1_fa + miss_penalty * 0.02582), (18, ht_l1_fa + miss_penalty * 0.02582), (19, ht_l1_fa + miss_penalty * 0.02582), (20, ht_l1_fa + miss_penalty * 0.02582))

  let x_axis = axis(min: 10, max: 20, step: 1, location: "bottom", title: [$log_2($L1 Cache Size$)$])
  let y_axis = axis(min: 0, max: 24, step: 4, location: "left", helper_lines: false, title: [Average Access Time (ns)])
  
  let p1 = plot(data: assoc_1_data, axes: (x_axis, y_axis))
  let p2 = plot(data: assoc_2_data, axes: (x_axis, y_axis))
  let p3 = plot(data: assoc_4_data, axes: (x_axis, y_axis))
  let p4 = plot(data: assoc_full_data, axes: (x_axis, y_axis))
  
  let g1 = graph_plot(p1, stroke: black, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and average access time", markings: [#emoji.rocket])
  let g2 = graph_plot(p2, stroke: blue, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and average access time", markings: [#emoji.rocket])
  let g3 = graph_plot(p3, stroke: red, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and average access time", markings: [#emoji.rocket])
  let g4 = graph_plot(p4, stroke: orange, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and average access time", markings: [#emoji.rocket])
  
  overlay((g1, g2, g3, g4), (90%, 30%))
}

#{
  v(20pt)
  exp1a_plot()
  exp1b_plot()
  v(20pt)
}

Associativity is color coded with an associativity of 1 being colored black, 2 being colored blue, 4 being colored red, 8 being colored purple, and fully-associative cache being colored orange.

As the associativity of the cache grows, the miss rate decreases. Similarly, as the size of the cache grows, the miss-rate decreases. Both have limited gains, and regardless of the associativity, the miss rate converges to 2.582% as the cache size reaches a size of $2^18$.

The compulsory cache miss rate appears to be 2.582% as that is the miss rate as the cache size grows. For each associativity, 1; 2; 4; 8; and full, the conflict miss rates appear to be 16.762%, 13.021%, 11.688%, 11.045%, and 11.114% respectively. For any given cache size, the best AAT will either be fully associative or tied with fully associative regardless of cache size.

= Replacement Policy Study

#let exp2_plot() = {
  /* sizes: 1024, 2048, 4096, 8192, 16_384, 32_768, 65_536, 131_072, 262_144*/

  let ht_l1_4 = 0.14682
  let miss_penalty = 100

  let rep_lru_data = ((10, ht_l1_4 + miss_penalty * 0.14270), (11, ht_l1_4 + miss_penalty * 0.09622), (12, ht_l1_4 + miss_penalty * 0.05992), (13, ht_l1_4 + miss_penalty * 0.04247), (14, ht_l1_4 + miss_penalty * 0.02832), (15, ht_l1_4 + miss_penalty * 0.02640), (16, ht_l1_4 + miss_penalty * 0.02595), (17, ht_l1_4 + miss_penalty * 0.02582), (18, ht_l1_4 + miss_penalty * 0.02582))
  
  let rep_fifo_data = ((10, ht_l1_4 + miss_penalty * 0.15415), (11, ht_l1_4 + miss_penalty * 0.10483), (12, ht_l1_4 + miss_penalty * 0.06727), (13, ht_l1_4 + miss_penalty * 0.04798), (14, ht_l1_4 + miss_penalty * 0.02977), (15, ht_l1_4 + miss_penalty * 0.02668), (16, ht_l1_4 + miss_penalty * 0.02603), (17, ht_l1_4 + miss_penalty * 0.02582), (18, ht_l1_4 + miss_penalty * 0.02582))

  let x_axis = axis(min: 10, max: 18, step: 1, location: "bottom", title: [$log_2($L1 Cache Size$)$])
  let y_axis = axis(min: 0, max: 20, step: 4, location: "left", helper_lines: false, title: [Average Access Time (ns)])
  let p1 = plot(data: rep_lru_data, axes: (x_axis, y_axis))
  let p2 = plot(data: rep_fifo_data, axes: (x_axis, y_axis))
  let g1 = graph_plot(p1, stroke: black, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and miss rate", markings: [#emoji.rocket])
  let g2 = graph_plot(p2, stroke: blue, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and miss rate", markings: [#emoji.rocket])
  overlay((g1, g2), (80%, 30%))
}

#{
  v(20pt)
  exp2_plot()
  v(20pt)
}

The line for cache with LRU replacement policy is colored black and the line for cache with FIFO replacement policy is colored blue.

Until both policies converge as the cache size reaches a large size, the LRU policy has a lower average access time. Therefore, LRU is the better policy.

#pagebreak()

= Inclusion Property Study

#let exp2_plot() = {
  /* sizes: 2048, 4096, 8192, 16_384, 32_768, 65_536*/

  // block size = 32 ; associativity = 8

  let l1_ht = 0.14682
  let l1_mr = 0.1427

  // rather than multiply by miss rate, we'll just manually shift the decimal on the MR by 100

  let inc_non_data = (
    (11, l1_ht + l1_mr * (0.180686 + 62.9713)),
    (12, l1_ht + l1_mr * (0.189065 + 37.6174)),
    (13, l1_ht + l1_mr * (0.211173 + 27.7715)), 
    (14, l1_ht + l1_mr * (0.233936 + 19.4114)), 
    (15, l1_ht + l1_mr * (0.288511 + 18.3952)), 
    (16, l1_ht + l1_mr * (0.341213 + 18.1430))
  )
  
  let inc_inc_data = (
    (11, l1_ht + 0.14523 * (0.180686 + 64.9108)), 
    (12, l1_ht + 0.14309 * (0.189065 + 37.7944)), 
    (13, l1_ht + 0.14277 * (0.211173 + 27.8000)), 
    (14, l1_ht + l1_mr * (0.233936 + 19.4114)), 
    (15, l1_ht + l1_mr * (0.288511 + 18.3952)), 
    (16, l1_ht + l1_mr * (0.341213 + 18.3952))
  )

  let x_axis = axis(min: 11, max: 16, step: 1, location: "bottom", title: [$log_2($L2 Cache Size$)$])
  let y_axis = axis(min: 0, max: 12, step: 4, location: "left", helper_lines: false, title: [Average Access Time (ns)])
  let p1 = plot(data: inc_non_data, axes: (x_axis, y_axis))
  let p2 = plot(data: inc_inc_data, axes: (x_axis, y_axis))
  let g1 = graph_plot(p1, stroke: black, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and miss rate", markings: [#emoji.rocket])
  let g2 = graph_plot(p2, stroke: blue, (100%, 30%), rounding: 10%, caption: "Relation between cache size, associativity, and miss rate", markings: [#emoji.rocket])
  overlay((g1, g2), (80%, 30%))
}

#{
  v(20pt)
  exp2_plot()
  v(20pt)
}

The line for cache with non-inclusive inclusion property is colored black and the line for cache with inclusive inclusion property is colored blue.

The non-inclusive inclusion property yields equivalent or better average access times by a minor margin which diminishes to near 0 as the size of the L2 cache grows.