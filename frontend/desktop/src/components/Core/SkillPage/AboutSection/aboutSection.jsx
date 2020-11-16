import React from 'react';
import './aboutSection.scss';
import Accordion from 'react-bootstrap/Accordion'
import { useSelector } from 'react-redux'

const AboutSection = (props) => {

    const { name, description  } = useSelector( store => store.skillBanner)

    return (
        <section className="container mt-0">
            <div id="module" className="row about-course">
    <h2 className="heading2">About {name}</h2>
                {/* <p className="about-course__txt collapse" id="expand-content" aria-expanded="false">Shine Learning offers online digital marketing courses which comprehensively cover the entire scope of the field. The top domains which are covered under the courses are social media optimization, search engine optimization, pay per click, email marketing, social media advertising.</p> */}
                <div dangerouslySetInnerHTML={{ __html: description }} >
                </div>
                <a role="button" className="collapsed" data-toggle="collapse" href="#expand-content" aria-expanded="false" aria-controls="expand-content"></a>
            </div>
        </section>
    )
}


export default AboutSection;