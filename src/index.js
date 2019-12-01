import React, { useState, useEffect, useRef } from "react"
import ReactDOM from "react-dom"
import styled from "styled-components"
import './main.css';

import candidateMap from "./candidateMap.js"

const data = require("./data/emojis.json")

const Img = styled.img`
  border-radius: 50%;
  width: 20vw;
  max-width: 125px;
  margin: 5px 5px 0 5px;
`

const CandidatePortraits = styled.div`
  background-color: #1da1f2;
  border: 1px solid lightgrey;
  border-radius: 2px;
  text-align: center;
  color: white;
`

const Emoji = styled.span`
  width: 80vw;
  font-size: 8px;
  border-left: 1px solid black;
  margin: 1vh;
  overflow-wrap: break-word;
  display: flex;
  flex-direction: column;
`

const Tooltip = styled.div`
  width: 350px;
`

const CandidateStats = (props) => {
    if (!props.candidate) {
        return (<div id="tooltip">Click a candidate to see their stats.</div>)
    }

    const screenName = candidateMap[props.candidate].screenName;
    return (
        <Tooltip id="tooltip" className="CandidateStats">
            <legend>
                Top emojis in Tweets sent to {props.candidate}'s Twitter
                account <a href={`http://twitter.com/${screenName}`}>@{screenName}</a>
            </legend>
            <ul className="CandidateStats">
                {data[screenName].most_common.map(x => (
                    <Emojis key={x} emoji={x} />
                ))}
            </ul>
            { props.children }
        </Tooltip>
    )
}

const Emojis = (props) => {
    const emoji = props.emoji[0]
    const count = props.emoji[1]

    return (
        <li>
            {emoji}
            <Emoji>
                {`${emoji}`.repeat(count)}
                {<span style={{ fontSize: '16px'}}>×{count}</span>}
            </Emoji>
        </li>

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
    // const node = useRef()

    /**
     * Reset the clickedCandidate to `null` on click-away events.
     * @param {*} e
     */
    const handleClick = e => {
        const t = e.target
        // if (node && node.current.contains(e.target)) {
        //     console.log('target is node')
        //     return;
        // }
        console.log(t);
        console.log(t.type)
        if (t.localName == 'html') {
            setClickedCandidate(null)
            return
        }

        if (t.localName === 'a' || t.localName === 'span' ||
            t.id === 'tooltip' ||
            (t.parentElement & t.parentElement.id === 'tooltip') ||
            (t.parentElement.parentElement && t.parentElement.parentElement.id === 'tooltip') ||
            Object.keys(candidateMap).includes(t.id)) {
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
            <header>
                <h1>U.S. Presidential Candidates, 2020</h1>
                <h2>A Tweet analysis</h2>
            </header>
            <CandidatePortraits>
                { Object.values(candidateMap).map((c, i) => (
                    <CandidateImage key={i}
                        candidate={c}
                        handleClick={() => {
                            if (c.name !== clickedCandidate) { setClickedCandidate(c.name) }
                        }}
                        handleMouseOver={() => setHoverCandidate(c.name)}
                        handleMouseEnter={() => setHoverCandidate(c.name)}
                        handleMouseOut={() => setHoverCandidate(null)}
                        handleMouseLeave={() => setHoverCandidate(null)}
                        />
                )) }
                <p>image credits: Politico</p>
            </CandidatePortraits>

            {( hoverCandidate && hoverCandidate !== clickedCandidate )
                ? <div>Click to see stats about {hoverCandidate}.</div>
                : <CandidateStats candidate={clickedCandidate} />
            }
        </div>
    )
}


const domElement = document.getElementById("root")
ReactDOM.render(<App />, domElement)
