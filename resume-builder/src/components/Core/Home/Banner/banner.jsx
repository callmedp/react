import React, {Component} from 'react';
import './banner.scss'
import { Events, animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'

export default class Banner extends Component {


    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
    }

    scrollTo(elem) {
        scroller.scrollTo(elem, {
          duration: 800,
          delay: 0,
          smooth: 'easeInOutQuad',
          offset:-63
        })
    }
    componentDidMount() {
        Events.scrollEvent.register('begin', function () {
          console.log("begin", arguments);
        });
    
        Events.scrollEvent.register('end', function () {
          console.log("end", arguments);
        });
    
    }

    componentWillUnmount() {
        Events.scrollEvent.remove('begin');
        Events.scrollEvent.remove('end');
    }
    

    render() {
        return (
            <div className="banner-bg">
               <div className="banner-content">
                   <h1>Quickest Resume Builder</h1>
                   <p className="banner-content--txt">
                       <strong>Amit,</strong> secure the job you want with our resume builder
                   </p>
                   <ul>
                        <li><strong>10 years</strong> of expertise in resume building</li>
                        <li>Build your resume in a minute by importing your <strong>Shine profile</strong></li>
                        <li><strong>Download</strong> your customised resume anytime</li>
                        <li><strong>Highly customizable</strong> resume</li>
                        <li>Power to get you <strong>hired 33% faster</strong></li>
                   </ul>
                   <button className="orange-button banner-content--button" onClick={() => this.scrollTo('templates')}>Build your resume</button>
               </div>
               <div className="banner-slider">
                    <img alt={"Banner"} src="/media/static/react/assets/images/home-banner-slider.png" className="img-responsive" />
               </div>
            </div>
        )
    }

}
