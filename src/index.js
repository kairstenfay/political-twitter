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
  background-color: white;
  padding: 3vw;
  border: 1px solid lightgrey;
  border-radius: 2px;
  margin: 1vw;
`

const CandidatePortraits = styled.div`
  background-color: white;
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 5vw;
  margin: 1vw;
`

const CandidateStats = (props) => {
    if (!props.candidate) {
        return (<ToolTip>Click a candidate to see their stats.</ToolTip>)
    }
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
        onMouseEnter={props.handleMouseEnter}
        onMouseLeave={props.handleMouseLeave}
        onMouseOver={props.handleMouseOver}
        onMouseOut={props.handleMouseOut}
        />
    )

const App = () => {
    const [ clickedCandidate, setClickedCandidate ] = useState(null)
    const [ hoverCandidate, setHoverCandidate ] = useState(null)
    const node = useRef()

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
                    <CandidateImage key={i}
                        candidate={c}
                        node={node}
                        handleClick={() => setClickedCandidate(c.name)}
                        handleMouseOver={() => setHoverCandidate(c.name)}
                        handleMouseEnter={() => setHoverCandidate(c.name)}
                        handleMouseOut={() => setHoverCandidate(null)}
                        handleMouseLeave={() => setHoverCandidate(null)}
                        />
                )) }
                <p>image credit: Politico</p>
            </CandidatePortraits>

            {( hoverCandidate && hoverCandidate !== clickedCandidate )
                ? <ToolTip>Click to see stats about {hoverCandidate}.</ToolTip>
                : <CandidateStats candidate={clickedCandidate} />
            }
        </div>
    )
}


const domElement = document.getElementById("root")
ReactDOM.render(<App />, domElement)
