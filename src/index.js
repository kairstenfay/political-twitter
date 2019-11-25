import React, { useState, useEffect, useRef } from "react"
import ReactDOM from "react-dom"
import styled from "styled-components"
import './main.css';

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
  max-width: 15vw;
  margin: 5px;
`

const ToolTip = styled.p`
  background-color: lightgrey;
  padding: 3vw;
  max-width: 30vw;
  border-radius: 5px;
`

const candidateMap = {
    'Elizabeth Warren': { name: 'Elizabeth Warren', photo: Warren },
    'Bernie Sanders': { name: 'Bernie Sanders', photo: Sanders },
    'Joe Biden': { name: 'Joe Biden', photo: Biden },
    'Andrew Yang': { name: 'Andrew Yang', photo: Yang },
    'Pete Buttigieg': { name: 'Pete Buttigieg', photo: Buttigieg },
    'Tulsi Gabbard': { name: 'Tulsi Gabbard', photo: Gabbard },
    'Kamala Harris': { name: 'Kamala Harris', photo: Harris },
    'Amy Klobuchar': { name: 'Amy Klobuchar', photo: Klobuchar },
    'Cory Booker': { name: 'Cory Booker', photo: Booker },
}

const Candidate = (props) => (
    <Img src={props.candidate.photo}
        ref={props.node}
        onMouseEnter={props.handleHover}
        onMouseOut={props.handleHover}
        onClick={props.handleClick}
        />
    )

const CandidatePreview = (props) => {
    return (
        <ToolTip id="tooltip">
            { props.children }
        </ToolTip>
    )
}


const App = () => {
    const [ toolTipVisibility, setToolTipVisibility ] = useState(false)
    const [ currentCandidate, setCurrentCandidate ] = useState(null)
    const [ hoverTarget, setHoverTarget ] = useState(null)
    const node = useRef();


    const handleClick = e => {
        if (node.current.contains(e.target)) {
          // inside click
          return;
        }  // outside click
        setCurrentCandidate(null)
      };

    useEffect(() => {
        // add when mounted
        document.addEventListener("mousedown", handleClick);

        // return function to be called when unmounted
        return () => {
          document.removeEventListener("mousedown", handleClick);
        };
      }, []);

    const toggleToolTipVisibility = (candidate) => {  // useEffect?
        setToolTipVisibility(!toolTipVisibility)
        setHoverTarget(candidate)
    }

    const toggleCurrentCandidate = () => {
    }

    // useEffect(() => {
    //     if (toolTipVisibility) {
    //         setCurrentCandidate('testing')
    //     }
    // }, [ toolTipVisibility ]) // TODO

    return (
        <div>
            <h1>U.S. Democratic Presidential Candidates</h1>
            <h2>A Tweet analysis</h2>
            { Object.values(candidateMap).map((c, i) => (
                <Candidate
                    node={node}
                    key={i}
                    candidate={c}
                    handleHover={c => toggleToolTipVisibility(c.name)}
                    handleClick={() => setCurrentCandidate(c.name)}
                    />
            )) }
            <p>image credit: Politico</p>
            { toolTipVisibility? (
                <CandidatePreview>
                    Click to see stats on {hoverTarget}
                </CandidatePreview>
            ) : (
                <CandidatePreview>
                    Click on a candidate to see their stats.
                </CandidatePreview>
            )}
            { !!currentCandidate && (
                <ToolTip>
                    Some facts about {currentCandidate}:
                    * loves cheese
                    * has a Twitter account
                </ToolTip>
            )}
        </div>
    )
}


const domElement = document.getElementById("root")
ReactDOM.render(<App />, domElement)
