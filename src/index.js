import React, { useState, useEffect, useRef } from "react"
import ReactDOM from "react-dom"
import styled from "styled-components"
import './main.css';

import candidateMap from "./candidateMap.js"

const data = require("./data/emojis.json")


const Img = styled.img`
  border-radius: 50%;
  max-width: 15vw;
  margin: 5px;
`

const ToolTip = styled.div`
  background-color: lightgrey;
  padding: 3vw;
  max-width: 30vw;
  border-radius: 5px;
`

const CandidatePortraits = styled.div`
  background-color: white;
`

const CandidateStats = (props) => {
    return (
        <ToolTip id="tooltip">
            Some facts about {props.candidate}:
            <ul>
                <li>loves cheese</li>
                <li>has a Twitter account @{data[props.candidate]}</li>
            </ul>
            { props.children }
        </ToolTip>
    )
}

const CandidateImage = (props) => (
    <Img src={props.candidate.photo}
        alt={`${props.candidate.name}`}
        id={props.candidate.name}
        ref={props.node}
        onClick={props.handleClick}
        />
    )

const TextBox = (props) => {
    console.log(props.hoverCandidate)
    // if (props.hoverCandidate) {
    //     return (
    //         <ToolTip>
    //             Click to see more about {props.hoverCandidate}.
    //         </ToolTip>
    //     )
    // }
    if (props.candidate) {
        return (
            <CandidateStats candidate={props.candidate} />
        )
    }
    else {
        return (
            <ToolTip>
                Click to see more about a candidate.
            </ToolTip>
        )
    }
}

const App = () => {
    const [ clickedCandidate, setClickedCandidate ] = useState(null)
    // const [ hoverCandidate, setHoverCandidate ] = useState(null)

    const node = useRef();

    /**
     * Reset the clickedCandidate to `null` on click-away events.
     * @param {*} e
     */
    const handleClick = e => {
        if (node.current.contains(e.target)) {
          return;
        }  // outside click
        setClickedCandidate(null)
      };


    /**
     * Handle click and click-away effects.
     */
    useEffect(() => {
        // add when mounted
        document.addEventListener("mousedown", handleClick);

        return () => { // return function to be called when unmounted
          document.removeEventListener("mousedown", handleClick);
        };
      }, []);


    return (
        <div>
            <h1>U.S. Democratic Presidential Candidates</h1>
            <h2>A Tweet analysis</h2>
            <CandidatePortraits>
                { Object.values(candidateMap).map((c, i) => (
                    <CandidateImage
                        node={node}
                        key={i}
                        candidate={c}
                        handleClick={() => setClickedCandidate(c.name)}
                        />
                )) }
                <p>image credit: Politico</p>
            </CandidatePortraits>
            <TextBox candidate={clickedCandidate} />
        </div>
    )
}


const domElement = document.getElementById("root")
ReactDOM.render(<App />, domElement)
