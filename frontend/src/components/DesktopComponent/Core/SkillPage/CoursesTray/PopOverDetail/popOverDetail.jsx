import React from 'react';
import { siteDomain } from 'utils/domains';

const PopoverDetail = (props) => {
    const noOfWords = 220
    const { popoverData : { 
                            about, highlights, 
                            jobsAvailable,  skillList,
                            url, type,
                            level, u_courses_benefits, u_desc }
                        } = props
    
    const OpenProductPage = () =>{
        window.location.replace(`${siteDomain}${url}`)
    }

    return (
        <>
            <p className="type">Type: <strong>{type}</strong>  |   Course level: <strong>{level}</strong>
    <br /><strong>{jobsAvailable}</strong> Jobs available
        </p>
            <p>
                <strong>About</strong>
                {
                    u_desc ? 
                    <div dangerouslySetInnerHTML={{__html: (u_desc?.replace(/<[^>]*>/g, '').slice(noOfWords)?.length ? (u_desc?.replace(/<[^>]*>/g, '').slice(0,noOfWords)+'...') : u_desc?.replace(/<[^>]*>/g, '').slice(0,noOfWords))}}></div> :
                    <div dangerouslySetInnerHTML={{__html: (about?.replace(/<[^>]*>/g, '').slice(noOfWords)?.length ? (about?.replace(/<[^>]*>/g, '').slice(0,noOfWords)+'...') : about?.replace(/<[^>]*>/g, '').slice(0,noOfWords))}}></div> 
                    
                }
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
            {
                highlights?.length ? 
                <>
                    <strong>Highlights</strong>
                    <ul>
                        {
                            highlights?.slice(0, 2)?.map((value, index) =>{
                                return (
                                    <li key={index}>{value}</li>
                                )
                            })
                        }
                    </ul>
                </> : ''
            }
            {   
                u_courses_benefits && 
                <p className="skill-ht">
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
                </p>
            }
            <button onClick={OpenProductPage} type="submit" className="btn btn-inline btn-secondary mx-auto" role="button">Enroll now</button>
        </>
    )
}

export default PopoverDetail;