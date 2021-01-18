import React, { useRef } from 'react';
import './aboutSection.scss';
import { useSelector } from 'react-redux'

const AboutSection = (props) => {

    const { name, about } = useSelector(store => store.skillBanner);
    // const regex = /<[^>]*>/g
    const regex = /<(.|\n)*?>/g

    return (
        <section className="container mt-0 " id="about" itemScope itemType="https://schema.org/AboutPage" >
            { about ? <div id="module" className="row about-course">
                <h2 className="heading2" itemProp="headline" >About {name}</h2>
                {about?.replace(regex, '')?.length > 365 ? (
                    <input type="checkbox" className="read-more-state" id="post-10" itemProp="about" />
                    ) : (
                        ""
                        )}
                        
                <p className="read-more-wrap">
                    <span dangerouslySetInnerHTML={{__html:about.replace(regex, '').slice(0, 365)}} />
                    <span className="read-more-target" dangerouslySetInnerHTML={{__html: about.replace(regex, '').slice(365)}} />
                </p>
                <label htmlFor="post-10" className="read-more-trigger"></label>
            </div> : "" }
        </section>
        )
    }
    
    
    export default AboutSection;