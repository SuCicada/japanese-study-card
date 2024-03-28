import ReactFullpage from "@fullpage/react-fullpage"

export const Test = () => {
    const fullpageOptions = {
        // fullpage.js 配置选项
        anchors: ['section1', 'section2', 'section3'], // 页面锚点
        sectionsColor: ['#f2f2f2', '#4BBFC3', '#7BAABE'], // 每个页面的背景颜色
        navigation: true, // 是否显示导航条
    };
    return (
        <ReactFullpage
            // animateAnchor={true}
            // autoScrolling={true}
            //fullpage options
            controlArrows={true}
            keyboardScrolling={true}
            scrollHorizontally={true}
            licenseKey={'YOUR_KEY_HERE'}
            // sectionsColor={["#ff5f45", "#0798ec", "#fc6c7c", "#435b71"]}
            scrollingSpeed={1000} /* Options here */
            render={({state, fullpageApi}) => {
                return (
                    <ReactFullpage.Wrapper>
                        <div className="section">
                            <div className="slide"> Slide 1 </div>
                            <div className="slide"> Slide 2 </div>
                            <div className="slide"> Slide 3 </div>
                            <div className="slide"> Slide 4 </div>
                        </div>
                    </ReactFullpage.Wrapper>
                );
            }}
            credits={
                {}
            }/>
    )
}
