import React, {useRef, useState, useEffect} from 'react';
import Toast from 'react-bootstrap/Toast';
import Modal from 'react-bootstrap/Modal';
import './offerEnds.scss';
import OfferModal from 'components/DesktopComponent/Common/Modals/offerModal';

const OfferEnds = (props) => {
    const { navOffer } = props;
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const [timerDays, setTimerDays] = useState("00");
    const [timerHours, setTimerHours] = useState("00");
    const [timerMinutes, setTimerMinutes] = useState("00");
    const [timerSeconds, setTimerSeconds] = useState("00");
    let interval = useRef();


    const startTimer = (countdownDate) => {
      const now = new Date().getTime();
      const distance = countdownDate - now;
  
      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor(
        (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
      );
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);
  
      if (distance < 0) {
        clearInterval(interval.current);
      } else {
        setTimerDays(days);
        setTimerHours(hours);
        setTimerMinutes(minutes);
        setTimerSeconds(seconds);
      }
    };

    const saveInLocalStorage = (time) => {
      localStorage.setItem("timer", time);
    }
  
    const getTimeFromLocalStorage = () => {
      return localStorage.getItem("timer");
    }

    useEffect(() => {
      const localTimer = getTimeFromLocalStorage();

      if (localTimer) {
        interval.current = setInterval(() => {
          startTimer(+localTimer);
        }, 1000);
      }
      else {
        const countdownDate = new Date(navOffer[0]);
        saveInLocalStorage(countdownDate);
        interval.current = setInterval(() => {
          startTimer(+countdownDate);
        }, 1000);
      }

      return () => clearInterval(interval.current);
    }, []);
    
    return(
        <div>
          <Toast className="offer-ends">
            <Toast.Header>
              <p className="flex-1">
                limited time offer by&nbsp;<strong>{navOffer[1]}&nbsp;</strong>   |  {navOffer[3]} OFF  |  Offer ends in
                <span className="time">
                  <strong>{timerDays}</strong> 
                  <em>D</em>
                </span>
                <span className="time">
                  <strong>{timerHours}</strong> 
                  <em>H</em>
                </span>
                <span className="time">
                  <strong>{timerMinutes}</strong> 
                  <em>M</em> 
                </span>
                <span className="time">
                  <strong>{timerSeconds}</strong> 
                  <em>S</em> 
                </span>
                <em onClick={handleShow} className="btn btn-inline btn-outline-primary">Avail offer</em>
              </p>
            </Toast.Header>
          </Toast>

          <OfferModal show={show} handleClose={handleClose} timerDays={timerDays} timerHours={timerHours} timerMinutes={timerMinutes} timerSeconds={timerSeconds} navOffer={navOffer}/>
          {/* <Modal 
            show={show} 
            onHide={handleClose}
            {...props}
            // size="md"
            dialogClassName="offer-end-box"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            
            <Modal.Header closeButton>
            </Modal.Header>
            <Modal.Body>
                  <form className="w-50">
                    <h2 className="heading2 mb-20">Avail offer</h2>
                    <div className="form-group error">
                        <input type="text" className="form-control" id="name" name="name" placeholder=" "
                            value="" aria-required="true" aria-invalid="true" />
                        <label for="">Name</label>
                        <span class="error-msg">Required</span>
                    </div>
                    <div className="form-group">
                        <input type="text" className="form-control" id="email" name="email" placeholder=" "
                            value="" aria-required="true" aria-invalid="true" />
                        <label for="">Email</label>
                    </div>
                    <div className="d-flex">
                        <div className="custom-select-box">
                            <select className="select" className="custom-select">
                                <option selected>+91</option>
                                <option value="+91">+91</option>
                                <option value="+92">+92</option>
                                <option value="+93">+93</option>
                            </select>
                        </div>
                        <div className="form-group flex-1">
                            <input type="text" className="form-control" id="mobile" name="mobile"
                                placeholder=" " value="" aria-required="true" aria-invalid="true" />
                            <label for="">Mobile</label>
                        </div>
                    </div>
                    <button type="submit" className="btn btn-block btn-primary submit-btn mt-10 mb-20" role="button">Avail offer now!</button>

                    <div className="brand-partner">
                      <strong><span>Course offered by</span></strong>
                      <figure>
                        <img src={`${imageUrl}desktop/cambridge-logo.png`} alt="Cambridge Assessment English" />
                      </figure>
                      <span>*T&C applied, valid only on select courses</span>
                    </div>
                  </form>
                  <div className="offer-box">
                    <div className="offer-txt">
                      <span className="offer-heading">Limited time offer -<strong> upto 20% off</strong></span>
                      Offer ends in  
                      <p className="mt-10">
                        <span className="time">
                          <strong>00</strong>
                          <em>Days</em>
                        </span>
                        <span className="time">
                          <strong>22</strong> 
                          <em>Hours</em>
                        </span>
                        <span className="time">
                          <strong>44</strong> 
                          <em>Min.</em> 
                        </span>
                        <span className="time">
                          <strong>24</strong> 
                          <em>Sec.</em> 
                        </span>
                      </p>
                    </div>
                  </div>
            </Modal.Body>
        </Modal>
        
         */}
        {/* <Modal 
            show={show} 
            onHide={handleClose}
            {...props}
            // size="md"
            dialogClassName="offer-end-box offer-thanks"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            
            <Modal.Header closeButton>
            </Modal.Header>
            <Modal.Body>
              <figure>
                  <img src="media/images/thankyou-offer.png" alt="Thank you" />
              </figure>
              <h2 className="heading2 mb-20 mt-20">Our expert will get in touch with you.</h2>
            </Modal.Body>
        </Modal> */}
      </div>
    )
}

export default OfferEnds;