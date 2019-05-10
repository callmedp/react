import React, {Component} from 'react';
import './resumeSlider.scss'
import Slider from "react-slick";

export default class ResumeSlider extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.selectTemplate = this.selectTemplate.bind(this);
    }

    selectTemplate(){
        // console.log("Selected Template",parseInt(document.getElementsByClassName('slick-current')[0].getAttribute('data-index')) + 1)
        localStorage.setItem('selected_template',(parseInt(document.getElementsByClassName('slick-current')[0].getAttribute('data-index')) + 1))
        window.location = '/resume-builder/edit/?type=profile'
    }

    render() {
        // const settings = {
        //     className: "center",
        //     centerMode: true,
        //     infinite: true,
        //     centerPadding: "60px",
        //     slidesToShow: 3,
        //     speed: 500
        // };

        const settings = {
            dots: false,
            className: "center",
            centerMode: true,
            infinite: true,
            centerPadding: "60px",
            slidesToShow: 3,
            speed: 500
        };

        return (
            <section id="templates" className="section-container">
                <h2>Proven resume templates</h2>
                <strong className="section-container--sub-head">Choose from a library of classic templates and land a
                    new job</strong>
                {/* <ul >
                    <li>
                        
                    </li>
                    <li>
                        <img src={`${this.staticUrl}react/assets/images/resume-2.jpg`}/>
                    </li>
                    <li>
                        <img src={`${this.staticUrl}react/assets/images/resume-3.jpg`}/>
                    </li>
                    <li>
                        <img src={`${this.staticUrl}react/assets/images/resume-4.jpg`}/>
                    </li>
                </ul> */}

                <Slider {...settings}>
                    {[1,2,3,4].map((item,key)=>{
                        return(
                            <div onClick={this.selectTemplate}>
                                <img src={`${this.staticUrl}react/assets/images/resume-${item}.jpg`}/>
                            </div>
                        )
                    })

                    }
                    
                
                </Slider>
                {/*<Slider {...settings}>*/}
                    {/*{*/}
                        {/*[1, 2, 3, 4, 5, 6, 7, 8].map((el, ind) => {*/}
                            {/*return (*/}
                                {/*<div  className={'resume-slider'}>*/}
                                    {/*<h3>{ind}</h3>*/}
                                {/*</div>)*/}
                        {/*})*/}
                    {/*}*/}
                {/*</Slider>*/}
                {/* <ul className="slider">
                <li><img onClick={() => this.props.history.push('/resume-builder/edit/')} alt={'Slider'}
                src={`${this.staticUrl}react/assets/images/slider.jpg`}
                className="img-responsive"/></li> */}
                {/* </ul> */}
                {/*<button className="orange-button orange-button--custom" onClick={() => this.scrollTo('templates')}>Customise*/}
                {/*</button>*/}
            </section>
        )
    }

}
