import {useEffect, useState} from 'react'
import './App.css'
import {Card, getAudio, importFile, parseCards} from "./utils.ts";


function App() {
    const [cards, setCards] = useState<Card[]>([])
    const [currentCard, setCurrentCard] = useState<Card | null>(null)
    const [audioUrl, setAudioUrl] = useState<string>()
    useEffect(() => {
        (async () => {
            const _cards_4 = await parseCards('../data/４　補助記憶装置.txt')
            const _cards_5 = await parseCards('../data/５　入出力装置.txt')
            setCards(prevCards => [ ..._cards_4, ..._cards_5]);
        })()
    }, []);

    useEffect(() => {
        (async () => {
            await setRandomCard(cards)
        })()
            console.log(cards)
        // const timerId = setInterval(async () => {
        //     await setRandomCard(cards)
        // }, 3000);
        // 在组件卸载时清除定时任务，以防止内存泄漏
        // return () => {
        //     clearInterval(timerId);
        // };
    }, [cards])

    async function setRandomCard(cards: Card[]) {
        if(cards.length === 0) {
            return
        }
        // random card from cards
        const index = Math.floor(Math.random() * cards.length)
        const card = cards[index]
        setCurrentCard(card)
        console.log(`${index} ${card.Expression} ${card.Reading} ${card.Meaning} ${card.Tags}`)
        const _audio = await getAudio(`${card.Expression}, ${card.Reading}`)
        setAudioUrl(_audio)
    }

    return (
        <>
            <div
                className="card-container"
                style={{
                    display: "flex",
                }}>
                <div
                    className="card-container-item card-button"
                    style={{
                        // display: "flex",
                        flexGrow: 1,
                        // fontSize: "20px",
                    }}>
                    <button>👈️</button>
                </div>
                <div
                    className="card-container-item"
                    style={{
                        // display: "flex",
                        flexGrow: 3,
                    }}>
                    <div style={{
                        fontFamily: "Noto Sans JP",
                        fontSize: "68px",
                        fontWeight: "bold",
                    }}>
                        {currentCard?.Expression}
                    </div>
                    <div style={{
                        fontFamily: "Noto Sans JP",
                        fontSize: "55px",
                        fontWeight: "bold",
                    }}>
                        {currentCard?.Reading}
                    </div>
                    <div>{currentCard?.Meaning}</div>
                    <br/>
                    <div>{currentCard?.Tags.map((Tag,i) => (
                        <span key={i}>{Tag}</span>
                    ))}</div>
                    <div>
                        <audio
                            controls
                            src={audioUrl}
                            autoPlay={true}
                            style={{
                                // display: audioUrl ? "block" : "none"
                                width: "100%",
                            }}
                            onEnded={async () => {
                                await setRandomCard(cards)
                            }}
                        ></audio>
                    </div>
                </div>
                <div
                    className="card-container-item card-button"
                    style={{
                        // display: "flex",
                        flexGrow: 1,
                    }}>
                    <button onClick={()=>setRandomCard(cards)}>👉</button>
                </div>
                {/*<a href="https://react.dev" target="_blank">*/}
                {/*  <img src={reactLogo} className="logo react" alt="React logo" />*/}
                {/*</a>*/}
            </div>
        </>
    )
}

export default App
