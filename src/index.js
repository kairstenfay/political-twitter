import React, { useState, useEffect, useRef } from "react"
import ReactDOM from "react-dom"
import styled from "styled-components"
import './main.css';

import candidateMap from "./candidateMap.js"

const data = require("./data/emojis.json")


const Header = styled.header`
  background-color: white;
  padding: 30vw;
  border: 1px solid lightgrey;
  border-radius: 2px;
  margin: 1vw;
`

const Img = styled.img`
  border-radius: 50%;
  width: 20vw;
  max-width: 150px;
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
  text-align: center;
`

const Emoji = styled.span`
  display: flex;
`

const CandidateStats = (props) => {
    if (!props.candidate) {
        return (<ToolTip id="tooltip">Click a candidate to see their stats.</ToolTip>)
    }

    const screenName = candidateMap[props.candidate].screenName;
    return (
        <ToolTip id="tooltip" className="CandidateStats">
            Some facts about {props.candidate}'s Twitter
            account <a href={`http://twitter.com/${screenName}`}>@{screenName}</a>
            <ul className="CandidateStats">
                <li>
                    {JSON.stringify(data[screenName].most_common)}
                </li>
                {data[screenName].most_common.map(x => (
                    <Emojis key={x} emoji={x} />
                ))}
            </ul>
            { props.children }
        </ToolTip>
    )
}

const Emojis = (props) => {
    const emoji = props.emoji[0]
    const count = props.emoji[1]

    return (
        <li>
            <Emoji>
                {`${emoji} `.repeat(count / 2)}
            </Emoji>
            {count}
            <Emoji>
                {`${emoji} `.repeat(count / 2)}
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

        if (t.localName === 'a' ||
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
            <Header>
                <h1>U.S. Presidential Candidates, 2020</h1>
                <h2>A Tweet analysis</h2>
            </Header>
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
