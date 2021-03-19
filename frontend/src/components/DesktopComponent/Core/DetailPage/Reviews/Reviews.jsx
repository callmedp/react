import React, {useState, useEffect} from 'react';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
import './Reviews.scss';
import Modal from 'react-bootstrap/Modal';
// import Button from 'react-bootstrap/Button';
import { useSelector, useDispatch } from 'react-redux';
import { fetchReviews } from 'store/DetailPage/actions';
// import Slider from "react-slick";

const LearnersStories = (props) => {
    const {id} = props;

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const { prd_reviews : { prd_review_list, prd_rv_current_page, prd_rv_has_next, prd_rv_has_prev } } = useSelector( store => store.reviews )

    const dispatch = useDispatch();
    let currentPage = 1;

    useEffect( () => {
        handleEffects(currentPage);
    }, [id])

    const handleEffects = async (page) => {
        currentPage = page;
        try {
            await new Promise((resolve, reject) => dispatch(fetchReviews({ payload: { prdId: id, page: page }, resolve, reject })));
        }
        catch (error) {
            if (error?.status == 404) {
                // history.push('/404');
            }
        }
    };

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> :
                star === '+' ? <em className="micon-halfstar" key={index}></em> :
                    <em className="micon-blankstar" key={index}></em>
        )
    }

    const handleSelect = (selectedIndex, e) => {
        //   console.log(currentPage)
          if(e.target.className === 'carousel-control-next-icon' && prd_rv_has_next) handleEffects(prd_rv_current_page+1);
          if(e.target.className === 'carousel-control-prev-icon' && prd_rv_has_prev) handleEffects(prd_rv_current_page-1);
    }

    return (
        <section id="reviews" className="container" data-aos="fade-up">
            <div className="grid">
                <h2 className="heading2 m-auto pb-20">Reviews</h2>

                <Carousel className="reviews" onSelect={handleSelect}>
                    <Carousel.Item interval={10000000000}>
                        <div className="d-flex col">
                            {
                                prd_review_list?.map((review, idx) => {
                                    return (
                                        <div className="col-sm-4" key={idx}>
                                            <div className="card">
                                                <span className="rating">
                                                    {
                                                        review?.rating?.map((star, index) => starRatings(star, index))
                                                    }
                                                </span>
                                                <strong className="card__name">{review?.title}</strong>
                                                <p className="card__txt">{review?.content}</p>
                                                <strong>{ review?.user_name ? review?.user_name : review?.user_email }</strong>
                                                <span className="card__location">{review?.created}</span>
                                            </div>
                                        </div>
                                    )
                                })
                            }
                        </div>
                    </Carousel.Item>
                </Carousel>

                <div className="d-flex mx-auto mt-20">
                    <Link to={"#"} onClick={handleShow} className="btn btn-outline-primary btn-custom">Write a review</Link>
                </div>
                <Modal show={show} 
                    onHide={handleClose}
                    {...props}
                    // size="md"
                    dialogClassName="write-reviews-box"
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                >
                    
                    <Modal.Header closeButton>
                    </Modal.Header>
                    <Modal.Body>
                        <h2 className="mb-20">Write a Review</h2>
                        <span className="rating">
                            <em className="icon-fullstar-big"></em>
                            <em className="icon-fullstar-big"></em>
                            <em className="icon-fullstar-big"></em>
                            <em className="icon-fullstar-big"></em>
                            <em className="icon-blankstar-big"></em>
                            <span>Click on rate to scale of 1-5</span>
                        </span>
                        <form className="mt-30">
                            <div className="form-group error">
                                <input type="text" className="form-control" id="name" name="name" placeholder=" "
                                    value="" aria-required="true" aria-invalid="true" />
                                <label for="">Title</label>
                                <span class="error-msg">Required</span>
                            </div>
                            <div className="form-group">
                                <textarea className="form-control" rows="3" id="mesage" name="mesage" placeholder=" "
                                    value="" aria-required="true" aria-invalid="true" />
                                <label for="">Review</label>
                            </div>
                            <button type="submit" className="btn btn-inline btn-primary submit-btn mx-auto" role="button">Submit</button>
                        </form>
                    </Modal.Body>
                </Modal>
            </div>
        </section>
    )
}

export default LearnersStories;