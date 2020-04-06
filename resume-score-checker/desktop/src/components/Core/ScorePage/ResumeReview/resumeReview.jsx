import React,{useState, useEffect} from 'react';
import './resumeReview.scss';
import { useSelector } from 'react-redux';

export default function ResumeReview(){

    const section_score = useSelector(state =>  state.home.section_score)
    const score = useSelector(state=> state.home.score)
    const [secscore, setSecscore] =useState(section_score[0])
    const [toggle, setToggle] =useState(new Array(section_score.length).fill({'checked':false}))
    useEffect(()=>{
      setToggle([{'checked':true},...toggle])
      localStorage.setItem('resume_score',JSON.stringify({score,section_score}))
    },[])
    const activateLi = (score,id) => {
      const newToggle = toggle.map((flag,index)=>{
          if(id==index){
            return {'checked':true}
          }
          else{
            return {'checked':false}
          }
        })

        setToggle(newToggle)
        setSecscore(score)
      }
    
    return (
        <section>
    <div className="container">
        <div className="d-flex justify-content-center">
            <h2><span>Resume detailed review</span></h2>
        </div>
        
        <div className="resume-detail mt-5">
          <ul className="resume-detail__list" >
        { section_score.map((score,index)=>{
        return (

            <li key={index} onClick={ () => activateLi(score,index) } className={ toggle[index].checked && "active" }> 
              <div>
                {
                score.section_status==1 && <i className="sprite green-tick mr-4"></i> 
                || score.sction_status ==2 && <i className="sprite question-mark mr-4"></i>
                || <i className="sprite caution-mark mr-4"></i>
                }
              {score.section_name}</div>
              <span className="fs-12"><strong className="fs-16">{score.section_score}</strong>/{score.total_section_score}</span>
            </li>
        )})
            }
        </ul> 
        <div className="resume-detail__contentWrap">
        <div className="resume-detail__content">
          <div className="resume-detail__content--head">
            <h3>{secscore.section_name}</h3>
            <div className="resume-detail__content--progressBar">
              <div className="sm-progress-circle" data-progress={secscore.section_score}>
                <div className="sm-progress-circle__text">
                  <strong>{secscore.section_score}</strong>
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
      <p>{secscore.section_description}</p>

          <ul className="mt-5">
            <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
            <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
            <li>When an unknown printer took a galley of type and scrambled it to make a type.</li>
            <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
          </ul>
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