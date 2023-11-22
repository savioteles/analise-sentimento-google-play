import React from 'react';
import {useState, useEffect} from 'react';
import './App.css';
import Positiveimg from './images/emoji_1.gif';
import Negativeimg from './images/sad_emoji.gif';
import Neutralimg from './images/no_express.gif';
import Sentiment from 'sentiment';
const sentiment = new Sentiment();


function App(){

  const [phrase, setphrase] = useState('')
  const [score, setscore] = useState(null)




  useEffect(() => {
    setscore(sentiment.analyze(phrase));
  }, [phrase])
  return(
      <div className='main'>
       
        <div className='main-container'>
            <h3 className='heading'>Sentiment Analysis</h3>
            <input value={phrase}  className='inputbox' onChange={(e)=> setphrase(e.target.value)}
            />
            <div className='scorecard'>
            {
                score !==null? 
            <p>Sentiment Score: {score.score}</p>
                :""
            }
            </div>
            <div className='img-container'>
            {
              score ? 
                  score.score===0? <img src={Neutralimg} className='image' alt='neutral'></img> :
                     score.score >0? <img src={Positiveimg} className='image' alt='positive'></img> :
                     <img src={Negativeimg} className='image' alt='negative'></img>
              :""
            }
            </div>
            </div>
      </div>
  )
}


export default App;