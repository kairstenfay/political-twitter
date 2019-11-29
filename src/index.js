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

const data = require("./data/emojis.json")
// import Steyer from "./img/TomSteyer.png"


const candidateMap = {
    'ewarren': {
		name: 'Elizabeth Warren',
        photo: Warren,
	},
    'BernieSanders': {
		name: 'Bernie Sanders',
        photo: Sanders,
	},
    'JoeBiden': {
		name: 'Joe Biden',
        photo: Biden,
	},
    'AndrewYang': {
		name: 'Andrew Yang',
        photo: Yang,
	},
    'PeteButtigieg': {
		name: 'Pete Buttigieg',
        photo: Buttigieg,
	},
    'TulsiGabbard': {
		name: 'Tulsi Gabbard',
        photo: Gabbard,
	},
    'KamalaHarris': {
		name: 'Kamala Harris',
        photo: Harris,
	},
    'amyklobuchar': {
		name: 'Amy Klobuchar',
        photo: Klobuchar,
	},
    'CoryBooker': {
		name: 'Cory Booker',
        photo: Booker,
	},
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
        onMouseEnter={props.handleMouseEnter}
        onMouseLeave={props.handleMouseLeave}
        onClick={props.handleClick}
        />
    )

const TextBox = (props) => {
    if (props.hoverCandidate) {
        return (
            <ToolTip>
                Click to see more about {props.hoverCandidate}.
            </ToolTip>
        )
    }
    else if (props.candidate) {
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
    const helpText = 'Click on a candidate to see their stats.'
    // const [ textBoxText, setTextBoxText ] = useState(helpText)
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


    const handleMouseOver = e => {
        setHoverCandidate(e.target.name)
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


      
    useEffect(() => {
        console.log('effect')
        return () => {
        }
    }, [ hoverCandidate ])


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
                        handleMouseEnter={() => setHoverCandidate(c.name)}
                        handleMouseLeave={() => setHoverCandidate(null)}
                        handleClick={() => setClickedCandidate(c.name)}
                        />
                )) }
                <p>image credit: Politico</p>
            </CandidatePortraits>
            <TextBox candidate={clickedCandidate} hoverCandidate={hoverCandidate} />
        </div>
    )
}


const domElement = document.getElementById("root")
ReactDOM.render(<App />, domElement)
