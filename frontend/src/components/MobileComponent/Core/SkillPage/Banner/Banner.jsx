import React, { useState } from 'react';
import './Banner.scss';
import { useSelector } from 'react-redux';

const noOfWords = 230

const SkillBanner = (props) => {
    const { name, about } = useSelector( store => store.skillBanner )
    const [showAll, setShowAll] = useState(false)
    
    const controlContent = (content, state) =>{
        return (
            <span onClick={()=>setShowAll(state)}>
                <strong>{content}</strong>
            </span>
        )
    }

    return (
        <div className="m-container mt-0 mb-0 m-skill-banner-bg m-skill-header">
            <h1 className="m-heading1">{name} Courses & Certifications</h1>
                <p>
                    {
                        about?.replace(/<[^>]*>/g, '').slice(0, noOfWords)
                    }
                    { 
                        (!showAll && about?.length > noOfWords) ? 
                            controlContent(" ...Read More", true) : ("") 
                    }
                    {
                        showAll ?
                           <>{ about?.replace(/<[^>]*>/g, '').slice(noOfWords)} <p>{controlContent("Show less", false)}</p> </>: null
                    }
                </p>
        </div>
    )
}

export default SkillBanner;