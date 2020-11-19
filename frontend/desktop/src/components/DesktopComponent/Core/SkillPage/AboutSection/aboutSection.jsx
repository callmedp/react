import React from 'react';
import './aboutSection.scss';
import { useSelector } from 'react-redux'

const AboutSection = (props) => {

    const { name, description } = useSelector(store => store.skillBanner)

    return (
        <section className="container mt-0" id="home">
            <div id="module" className="row about-course">
                <h2 className="heading2">About {name}</h2>
                <div dangerouslySetInnerHTML={{ __html: description }} >
                </div>
                <a role="button" className="collapsed" data-toggle="collapse" href="#expand-content" aria-expanded="false" aria-controls="expand-content"></a>
            </div>
        </section>
    )
}


export default AboutSection;