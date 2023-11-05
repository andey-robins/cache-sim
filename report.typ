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

= Replacement Policy Study

= Inclusion Property Study