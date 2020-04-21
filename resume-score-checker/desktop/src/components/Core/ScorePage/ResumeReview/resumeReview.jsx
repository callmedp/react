import React,{useState, useEffect} from 'react';
import './resumeReview.scss';

const Description = desc =>{
  return { __html : desc }
}

const ResumeReview=props=>{
    const section_score =JSON.parse(localStorage.getItem('resume_score'))?.section_score
    const [toggle, setToggle] =useState(new Array(section_score?.length).fill({'checked':false}))
    const [subSection,setSubSection] = useState(section_score?.length ? section_score[0] : '')
    useEffect(()=>{
      setToggle([{'checked':true},...toggle])
    },[])
    const activateLi = (score,id) => {
      const newToggle = toggle.map((flag,index)=>{
          if(id===index){
            return {'checked':true}
          }
          else{
            return {'checked':false}
          }
        })
        setSubSection(score)
        console.log("this is score")
        console.log(score)
        setToggle(newToggle)
      }
    
    return (
        <section>
    <div className="container">
        <div className="d-flex justify-content-center">
            <h2><span>Resume detailed review</span></h2>
        </div>
        
        <div className="resume-detail mt-5">
          <ul className="resume-detail__list" >
        { section_score?.map((score,index)=>{
        return (

            <li key={index} onClick={ () => activateLi(score,index) } className={ toggle[index]?.checked ? "active" : ""}> 
              <div>
                {
                ((score.section_status===2 && <i className="sprite green-tick mr-4"></i> )
                  || (score.section_status ===1 && <i className="sprite caution-mark mr-4"></i>)
                || (<i className="sprite question-mark mr-4"></i>))
    
                }
              {score.section_name}</div>
              <span className="fs-12"><strong className="fs-16">{score.section_score}</strong>/{score.section_total_score}</span>
            </li>
        )})
            }
        </ul> 
        <div className="resume-detail__contentWrap">
        <div className="resume-detail__content">
          <div className="resume-detail__content--head">
            <h3>{subSection?.section_name}</h3>
            <div className="resume-detail__content--progressBar">
              <div className="sm-progress-circle" data-progress={Math.round(subSection?.section_score*100/subSection?.section_total_score)}>
                <div className="sm-progress-circle__text">
                  <strong>{subSection?.section_score}</strong>
                </div>
                <div className="ko-circle">
                    <div className="full sm-progress-circle__slice">
                        <div className="sm-progress-circle__fill"></div>
                    </div>
                    <div className="sm-progress-circle__slice">
                        <div className="sm-progress-circle__fill"></div>
                        <div className="sm-progress-circle__fill sm-progress-circle__bar"></div>
                    </div>
                </div>
                <div className="sm-progress-circle__overlay"></div>
            </div>
            </div>
          </div>
          <p>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;</p>
          <div dangerouslySetInnerHTML={Description(subSection?.section_description)}></div>
        </div>
      </div>
        </div>
        <div className="mark-info">
          <span className="mr-5"><i className="sprite green-tick mr-3"></i>Available in resume</span>
          <span className="mr-5"><i className="sprite question-mark mr-3"></i>Missing in resume</span>
          <span><i className="sprite caution-mark mr-3"></i>Need major attention</span>
        </div>
    </div>
</section>    
    );
}

export default ResumeReview;