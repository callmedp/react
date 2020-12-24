import React from 'react';
import { siteDomain } from 'utils/domains';

const PopoverDetail = (props) => {
    const noOfWords = 220
    const { popoverData : { 
                            about, highlights, 
                            jobsAvailable,  skillList,
                            url, type,
                            level, u_courses_benefits }
                        } = props
    
    const OpenProductPage = () =>{
        window.location.replace(`${siteDomain}${url}`)
    }

    return (
        <>
            <p className="type">Type: <strong>{type}</strong>  |   <strong>Course level:</strong> {level}
    <br /><strong>{jobsAvailable}</strong> Jobs available
        </p>
            <p>
                <strong>About</strong>
                <div dangerouslySetInnerHTML={{__html: (about?.slice(noOfWords)?.length ? (about?.slice(0,noOfWords)+'...') : about?.slice(0,noOfWords))}}></div>
            </p>
            <p>
                <strong>Skills you gain</strong>
                {
                    skillList?.slice(0, 10)?.map((skill, index) =>{
                        return ( 
                            <React.Fragment key={index}>
                                {skill}
                                {index === skillList?.slice(0, 10).length-1 ? ' ' : '  |  '}
                                {(skillList?.slice(0, 10)?.pop() == skill && skillList?.slice(10)?.length) ? '& Many More..' : ''}
                            </React.Fragment>
                            )
                    })
                }
        </p>
            {highlights && <p>
                <strong>Highlights</strong>
                {/* <p dangerouslySetInnerHtml={{__html : highlights}}></p> */}
                {highlights?.replace(/<[^>]*>/g, '')?.slice(80)?.length ? (highlights?.replace(/<[^>]*>/g, '')?.slice(0,80)+'...') : highlights?.replace(/<[^>]*>/g, '')?.slice(0,80)}
            </p>}
            {u_courses_benefits && <p className="skill-ht">
                <strong>Highlights</strong>
                <ul>
                    {
                        u_courses_benefits?.slice(0, 2)?.map((value, index) =>{
                            return (
                                <li key={index}>{value}</li>
                            )
                        })
                    }
                </ul>
            </p>}
            <button onClick={OpenProductPage} type="submit" className="btn btn-inline btn-secondary mx-auto" role="button">Enroll now</button>
        </>
    )
}

export default PopoverDetail;