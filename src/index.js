import React from "react"
import ReactDOM from "react-dom"
import styled from "styled-components"
import Yang from "./img/AndrewYang.png"

const Img = styled.img`
  border-radius: 50%;
  max-width: 100px;
  border: 1px solid black;
`


const Candidate = () => (<Img src={Yang} />)

const App = () => {
    return (
        <div>
            <Candidate />
        </div>
    )
}

const domElement = document.getElementById("root")

// and away we go!
ReactDOM.render(<App />, domElement)
