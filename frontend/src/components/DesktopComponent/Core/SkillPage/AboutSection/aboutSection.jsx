import React, { useRef, useEffect } from 'react';
import './aboutSection.scss';
import { useSelector } from 'react-redux'

const AboutSection = (props) => {
    const { pageId } = props
    const { name, about } = useSelector(store => store.skillBanner);
    const reqLength = 365
    const regex = /<(.|\n)*?>/g
    const inputCheckbox = useRef(null)
    useEffect(() => {
        inputCheckbox.current && (inputCheckbox.current.checked = false)
    }, [pageId])

    return (
        <section className="container mt-0 " id="about" itemScope itemType="https://schema.org/AboutPage" >
            { about ? <div id="module" className="row about-course">
                <h2 className="heading2" itemProp="headline" >About {name}</h2>
                {about?.replace(regex, '')?.length > reqLength ? (
                    <input type="checkbox" className="read-more-state" id="post-10" ref={inputCheckbox} itemProp="about" />
                    ) : (
                        ""
                        )}
                        
                <p className="read-more-wrap">
                    <span dangerouslySetInnerHTML={{__html:about.replace(regex, '').slice(0, reqLength)}} />
                    <span className="read-more-target" dangerouslySetInnerHTML={{__html: about.replace(regex, '').slice(reqLength)}} />
                </p>
                <label htmlFor="post-10" className="read-more-trigger"></label>
            </div> : "" }
        </section>
        )
    }
    
    
    export default AboutSection;