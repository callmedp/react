import React,{useState}from 'react';
import './innerBanner.scss';
import { Link as LinkScroll} from 'react-scroll';
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux';
import * as Actions from '../../../../store/LandingPage/actions/index';

export default function InnerBanner(){
    const [flag, setFlag] = useState(true);
    const [filename, setFileName] = useState('Upload Resume');
    const dispatch = useDispatch()
    const score = useSelector(state => state.home.score )
    const fileUpload = async event => {
        let file1 = event.target.files[0];
        if((file1.name.slice(-4)=='.pdf' || file1.name.slice(-4)=='.doc' || file1.name.slice(-5)=='.docx') && (file1.size/(1024*1024)<=5)){
            setFileName('File Uploading...')
            let url = await new Promise((resolve, reject) => {
                dispatch(Actions.uploadFileUrl({file1, resolve, reject}));
            })
            console.log("This is the url")
            console.log(url)
            setFlag(false)
            setFileName('Check Score')
            }
        else{
            console.log("file is unsafe")
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
    <strong>{score}</strong>
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
                    { flag && 
                            <div className="file-upload btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                                <i className="sprite upload mr-3"></i> 
                                { filename }               
                                <input className="file-upload__input" type="file"  onChange={fileUpload} name="resume"/>
                            </div>
                            
                         ||
                         <Link to = "/score-checker" className="file-upload btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">            
                            <i ></i>  Check Score
                        </Link>
                        }

                    <LinkScroll to='getexpert' className="btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                        Get expert help
                    </LinkScroll>
                </div>
            </div>
            
        </div>
    </div>
</section>
<section className="howItWork" style={{height: '60px'}}></section>
</div>
    );
}