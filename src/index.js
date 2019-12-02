import React, { useState, useEffect, useRef } from "react"
import ReactDOM from "react-dom"
import styled from "styled-components"
import './main.css';

import candidateMap from "./candidateMap.js"

const data = require("./data/emojis.json")
const twitter = require("./img/twitter.png")

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
  width: 70vw;
  font-size: 8px;
  border-left: 1px solid black;
  margin: 1vh;
  overflow-wrap: break-word;
  display: flex;
  flex-direction: column;
`

const Tooltip = styled.div`
  display: flex;
  flex-direction: column;
  margin-left: -5vw;
  padding: 15px;
`

const HelpText = styled.p`
  display: flex;
  flex-direction: row;
  justify-content: center;
  padding: 25px 15px;
  height: 5vh;
  background-color: grey;
  color: white;
`


const CandidateStats = (props) => {
    if (!props.candidate) {
        return null
    }

    const screenName = candidateMap[props.candidate].screenName;

    const politicalEmojis = {
        '🧢': 'https://www.urbandictionary.com/define.php?term=🧢',
        '🌹': 'https://mashable.com/2017/05/27/hidden-meaning-rose-emoji-dsa/',
    }

    return (
        <Tooltip ref={props.node} id="tooltip" className="CandidateStats">
            <h2>
                Top Emojis from Users Tweeting to {props.candidate}
            </h2>
            <legend>
                The 15 most common emojis from the names of Twitter users
                sending {data[screenName].tweets} Tweets
                to <a href={`http://twitter.com/${screenName}`}>@{screenName}.</a>
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
    const node = useRef()

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
                <h1><img id="twitterBird" src={twitter} />My Country Tis of Tweet:</h1>
                <h2>Who on Twitter talks to U.S. 2020 Presidential Candidates?</h2>
                <h3>A Tweet analysis by Kairsten Fay</h3>
            </header>
            { hoverCandidate
                ? (<HelpText>Click to see stats about {hoverCandidate}.</HelpText>)
                : (<HelpText>Click a candidate to see their stats.</HelpText>)
            }
            <CandidatePortraits>
                { Object.values(candidateMap).map((c, i) => (
                    <CandidateImage key={i}
                        candidate={c}
                        handleClick={() => { // todo refactor
                            if (c.name !== clickedCandidate) { setClickedCandidate(c.name) }
                            if (node.current){
                                    node.current.scrollIntoView({
                                       behavior: "smooth",
                                       block: "nearest"
                                    })
                                }
                            }
                        }
                        handleMouseOver={() => setHoverCandidate(c.name)}
                        handleMouseEnter={() => setHoverCandidate(c.name)}
                        handleMouseOut={() => setHoverCandidate(null)}
                        handleMouseLeave={() => setHoverCandidate(null)}
                        />
                )) }
                <p>image credits: Politico</p>
            </CandidatePortraits>

            {(clickedCandidate && (
                <CandidateStats node={node} candidate={clickedCandidate} />
            ))}
        </div>
    )
}


const domElement = document.getElementById("root")
ReactDOM.render(<App />, domElement)
