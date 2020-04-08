import React,{useState}from 'react';
import './innerBanner.scss';
import { Link as LinkScroll} from 'react-scroll';
import { Link , Route } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux';
import * as Actions from '../../../../store/LandingPage/actions/index';
import  Loader  from '../../../Loader/loader';
import Swal from 'sweetalert2'

export default function InnerBanner(){
 
    const score = useSelector(state => state.home.score )
    const section_score = useSelector( state => state.home.section_score)
    const [flag, setFlag] = useState(false);
    const [localScore, setLocalScore] =useState(JSON.parse(localStorage.getItem('resume_score')).score)
    const dispatch = useDispatch()
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-right',
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true,
        onOpen: (toast) => {
          toast.addEventListener('mouseenter', Swal.stopTimer)
          toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
      })
       
    const fileUpload = async event => {
        let file1 = await event.target.files[0];
        if((file1.name.slice(-4)=='.pdf' || file1.name.slice(-4)=='.doc' || file1.name.slice(-5)=='.docx') ){
            try{
            setFlag(true)
            let url = await new Promise((resolve, reject) => {
                dispatch(Actions.uploadFileUrl({file1, resolve, reject}));
            })
            localStorage.removeItem('resume_score')
            localStorage.setItem('resume_score',JSON.stringify({score,section_score}))
            setLocalScore(score)
            setFlag(false)
            }catch(err){
                setFlag(false)
                Toast.fire({
                    icon: 'error',
                    html : '<h3>Something went wrong! Try again.<h3>'
                  })
            }
        }
        else{
             
            Toast.fire({
                icon: 'warning',
                html: '<h3>Please select the file in the format PDF,DOC,DOCX only<h3>',
            })
        }
    }


    return (
<div>        
<section className="banner">
    <div className="container h-100">
        <div className="row h-100">
            <div className="col-md-6">
                <div className="banner-score">
                    <nav aria-label="breadcrumb">
                        <ol className="breadcrumb">
                          <li className="breadcrumb-item"><Link to='/'>Home</Link></li>
                          <li className="breadcrumb-item active" aria-current="page">Resume Review</li>
                        </ol>
                    </nav>
                    <div className="banner-score__resume-scoreWrap"> 
                      <div className="banner-score__progressBar">

                        <div className="ko-progress-circle" data-progress="70">
                          <div className="ko-progress-circle__text">
    <strong>{localScore}</strong>
                            <p className="fs-12">Resume score</p>
                            
                          </div>
                          <div className="ko-circle">
                              <div className="full ko-progress-circle__slice">
                                  <div className="ko-progress-circle__fill"></div>
                              </div>
                              <div className="ko-progress-circle__slice">
                                  <div className="ko-progress-circle__fill"></div>
                                  <div className="ko-progress-circle__fill ko-progress-circle__bar"></div>
                              </div>
                          </div>
                          <div className="ko-progress-circle__overlay"></div>
                        </div>

                      </div>
                      
                      {/* <div className="banner-score__myresume">
                        <a href="#">
                          <i className="sprite clip"></i>
                          Myresume.doc
                        </a>

                        <a href="#" className="btn btn-outline-primary btn-round-40 fs-12 py-1">Download</a>
                      </div> */}
                    </div>

                </div>
            </div>
            <div className="col-md-6 h-100 d-flex align-items-self-start justify-content-center flex-column">
                <h1 className="fs-30">
                    <span>Hello Sachin,<br/>Your resume Scored {score} out of 100</span>
                </h1>
                <p className="text-white-50">Good Job! You are just few steps away for perfecting your resume. Check out the detailed reviews to improve the score. Score more to get perfect job match your profile</p>

                <div className="d-flex mt-5">
                    <LinkScroll 
                        to='getexpert' 
                        className="btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                        Get expert help
                    </LinkScroll>
                    <div className="file-upload btn btn-outline-light btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                        <i className="sprite export mr-3"></i> 
                            Upload Resume            
                        <input className="file-upload__input" type="file"  onChange={fileUpload} name="resume"/>
                    </div>
                    { flag && <Loader></Loader> }

                    
                </div>

            </div>
            
        </div>
    </div>
</section>
<section className="howItWork" style={{height: '60px'}}></section>
</div>
    );
}