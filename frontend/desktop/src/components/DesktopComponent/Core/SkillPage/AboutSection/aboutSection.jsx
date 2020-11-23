import React from 'react';
import './aboutSection.scss';
import { useSelector } from 'react-redux'

const AboutSection = (props) => {
    
    const { name, description  } = useSelector( store => store.skillBanner)
    
    return (
        <section className="container mt-0 pl-0" id="aboutSect">
            <div id="module" className="about-course">
            <h2 className="heading2">About {name}</h2>
            {description.length > 255 ? (<input type="checkbox" className="read-more-state" id="post-1" />)
            : ("")}
                <p className="read-more-wrap">
                    {!description ? null : description.slice(0, 255)}
                    <span className="read-more-target">{description.slice(255)}</span>
                </p>
                <label htmlFor="post-1" className="read-more-trigger"></label>
            </div>
        </section>
        )
    }
    
    
    export default AboutSection;