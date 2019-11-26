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

const Candidate = (props) => (
    <Img src={props.candidate.photo}
        id={props.name}
        ref={props.node}
        onMouseEnter={props.handleHover}
        onMouseOut={props.handleHover}
        onClick={props.handleClick}
        />
    )

const CandidateStats = (props) => {
    return (
        <ToolTip id="tooltip">
            Some facts about {props.candidate}:
            <ul>
                <li>loves cheese</li>
                <li>has a Twitter account</li>
            </ul>
            { props.children }
        </ToolTip>
    )
}

const App = () => {
    const [ clickedCandidate, setClickedCandidate ] = useState(null)
    const [ hoverCandidate, setHoverCandidate ] = useState(null)
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

    const handleHover = (candidate) => {  // useEffect?
        hoverCandidate ? setHoverCandidate(null) : setHoverCandidate(candidate)
    }

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
            { Object.values(candidateMap).map((c, i) => (
                <Candidate
                    node={node}
                    key={i}
                    candidate={c}
                    handleHover={() => handleHover(c.name)}
                    handleClick={() => setClickedCandidate(c.name)}
                    />
            )) }
            <p>image credit: Politico</p>

            { hoverCandidate
                ? <CandidateStats candidate={hoverCandidate} />
                : clickedCandidate
                    ? <CandidateStats candidate={clickedCandidate} />
                    : (
                        <ToolTip>
                            Click on a candidate to see their stats.
                        </ToolTip>
                    )
            }
        </div>
    )
}


const domElement = document.getElementById("root")
ReactDOM.render(<App />, domElement)
