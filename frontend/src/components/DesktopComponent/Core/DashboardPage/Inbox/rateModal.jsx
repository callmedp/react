import React, {useState} from 'react';
import { Modal } from 'react-bootstrap';


const RateModal =(props) => {

    const { handleClose, show, name } = props;
    
    let [rating, setRating] = useState(-1);
    let [clicked, setClicked] = useState(false);

    const fillNewStar = (star) => {
        if (star <= rating) return "icon-fullstar";
        else return "icon-blankstar";
    };

    const mouseOver = (e) => {
        setStars(4);
        setStars(e, "fullstar");
    };

    const mouseOut = (e) => (!clicked ? setStars(e) : null);

    const onClickEvent = (e, val = 0) => {
        setRating(
            parseInt(e.target.getAttribute("value"))
                ? parseInt(e.target.getAttribute("value"))
                : val
        );
        setStars(e, "fullstar");
        setClicked(true);
    };

    const setStars = (e, className = "blankstar") => {
        let data = typeof e == "number" ? e : parseInt(e.target.getAttribute("value")) - 1;
        let children = document.getElementsByClassName("rating-review")[0].children;
        for (let i = 0; i <= data; i++) {
            children[i].setAttribute("className", `icon-${className}`);
        }
    };

    return (
        <Modal show={show} onHide={handleClose} className="db-modal">
        <Modal.Header closeButton>
        </Modal.Header>
        <Modal.Body>
            <div className="text-center db-rate-services need-help">
                <img src="/media/images/rate-services.png" className="img-fluid" alt=""/>
                <p className="db-rate-services--heading">Rate {name}</p>
                
                <span className="rating-review">
                    {[1, 2, 3, 4, 5].map((value,indx) => {
                        return (
                            <i
                            key={indx}
                            value={value}
                            className={fillNewStar(value)}
                            onMouseOver={(e) => mouseOver(e)}
                            onMouseOut={(e) => mouseOut(e)}
                            onClick={(e) => onClickEvent(e)}
                            ></i>
                        );
                    })}
                </span>
                <p className="db-rate-services--subheading">Click on rate to scale of 1-5</p>
                <form action="">
                    <div className="form-group">
                        <input type="email" className="form-control" id="email" name="email" placeholder=" "
                            value="" aria-required="true" aria-invalid="true" />
                        <label htmlFor="">Email</label>
                    </div>
                    
                    <div className="form-group">
                        <textarea  className="form-control" name="review" id="review" cols="30" rows="3" placeholder=" "></textarea>
                        <label htmlFor="">Review</label>
                    </div>

                    <button className="btn btn-primary px-5">Submit</button>
                </form>
            </div>
        </Modal.Body>
    </Modal>
    )
}

export default RateModal;