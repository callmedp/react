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
          offset:-50
        })
    }
    componentDidMount() {
        
    
    }

    componentWillUnmount() {
        
    }
    

    render() {
        return (
            <section className="banner">
                <h1 className="mt-15">Quickest <br/>Resume Builder</h1>
                <p><strong>Amit</strong>, secure the job you want with our
                resume builder</p>

                <img src="/media/static/react/assets/images/mobile/resume-bundel.png" alt="" className="img-fluid"/>
                <p className="text-center mt-5">
                    <a className="btn pt-10 pb-10 btn__round btn__primary" onClick={() => this.scrollTo('templates')}>Build your resume</a>
                </p>
            </section>
        )
    }

}
