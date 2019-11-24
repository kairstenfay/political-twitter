import React from "react"
import ReactDOM from "react-dom"
import styled from "styled-components"

import Warren from "./img/ewarren.png"
import Sanders from "./img/BernieSanders.png"
import Biden from "./img/JoeBiden.png"
import Yang from "./img/AndrewYang.png"
import Buttigieg from "./img/PeteButtigieg.png"
import Booker from "./img/CoryBooker.png"
import Gabbard from "./img/TulsiGabbard.png"
import Harris from "./img/KamalaHarris.png"
import Klobuchar from "./img/AmyKlobuchar.png"
// import Steyer from "./img/TomSteyer.png"

const Img = styled.img`
  border-radius: 50%;
  max-width: 100px;
  border: 1px solid grey;
  margin: 5px;
`

const candidates = [
    Warren, Sanders, Biden, Yang, Buttigieg, Gabbard, Harris, Klobuchar, Booker
]

const Candidate = (props) => (<Img src={props.candidate} />)

const App = () => {
    return (
        <div>
            { candidates.map(c => (<Candidate candidate={c} />)) }
        </div>
    )
}


const domElement = document.getElementById("root")
ReactDOM.render(<App />, domElement)
