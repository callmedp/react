import React,{useEffect,useState } from 'react';
import './parameters.scss'
import { useDispatch } from 'react-redux';
import { eventClicked } from '../../../../store/googleAnalytics/actions/index'
import { Link } from 'react-router-dom';
import { Link as LinkScroll } from 'react-scroll';

const Parameters=props=> {

    const [flag, setFlag] =useState(false)
    const staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    const dispatch = useDispatch()

    useEffect(()=>{
        if(!JSON.parse(localStorage.getItem('resume_score'))){
            setFlag(false)
        }
        else{
            setFlag(true)
        }
    },[])

    const handleCheckScore = () => {
        dispatch(eventClicked({
            'action': 'CheckScore',
            'label': 'Params'
        }))

    }

    return (

        <section className="parameters">
            <div className="container">
                <div className="d-flex justify-content-center">
                    <h2><span>Resume checker Parameters</span></h2>
                </div>

                <div className="media align-items-center">
                    <div className="media-body">
                        <ul className="parameters__lists mt-5">
                            <li className="parameters__item">
                                <p className="parameters__head">Format /Style</p>
                                <p>It checks font size, font family, resume structure flow, sections and length of the resume.</p>
                            </li>

                            <li className="parameters__item">
                                <p className="parameters__head">Education Details</p>
                                <p>It evaluates all the required educational details such as your latest qualifications, year of graduation, overall marks scored etc.</p>
                            </li>

                            <li className="parameters__item">
                                <p className="parameters__head">Summary & Objective</p>
                                <p>This resume section communicates your overall work experience and expectations to the recruiters at one go.</p>
                            </li>

                            <li className="parameters__item">
                                <p className="parameters__head">Skills & Work Experience</p>
                                <p>It makes sure you have skills and work experience in your resume based on job opportunities you’re looking for.</p>
                            </li>

                            <li className="parameters__item">
                                <p className="parameters__head">Contact Details</p>
                                <p>It checks the presence of name, email-id, address and mobile number, LinkedIn profile in resume. </p>
                            </li>
                            <li className="parameters__item">
                                <p className="parameters__head">Resume action verbs</p>
                                <p>Resume checker validates and makes sure you’ve used strong action verbs as well as other index of a strong impact- oriented resume.</p>
                            </li>
                        </ul>
                    </div>
                    <img className="ml-5 img-fluid parameters__image" alt="parameters" src={`${staticUrl}score-checker/images/parameters-image.png`} />
                </div>

                <div className="text-center mt-5">
                    {flag ? <Link to='/resume-score-checker/score-checker' className="btn btn-primary btn-round-40 px-5 py-4 mr-5" onClick={handleCheckScore}>Check the score now</Link> :
                        <LinkScroll to='banner' className="btn btn-primary btn-round-40 px-5 py-4 mr-5" onClick={handleCheckScore}>Check the score now</LinkScroll> }
                </div>

            </div>
        </section>
    );
}

export default Parameters;