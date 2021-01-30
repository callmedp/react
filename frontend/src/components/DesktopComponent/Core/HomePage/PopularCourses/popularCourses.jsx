import React, {useState} from 'react';
import '../../SkillPage/CoursesTray/coursesTray.scss';
import './popularCourses.scss'
import { Tabs, Tab, CarouselItem } from 'react-bootstrap';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
   
function PopularCourses() {
  const [key, setKey] = useState('categories1');

  return (
    <section className="container mt-30 mb-0">
        <div className="row"> 
            <div className="col courses-tray popular-course-demand">
                <h2 className="heading2 text-center mb-20">Popular courses in demand</h2>
                <Tabs
                id="controlled-tab-example"
                activeKey={key}
                onSelect={(k) => setKey(k)}
                className="category"
                >
        
                <Tab eventKey="categories1" title={<h2>Master’s</h2>}>
                    <Carousel className="" fade={true}>
                        <Carousel.Item interval={10000000000}>
                            <ul className="courses-tray__list">
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg1">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg2">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg3">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg4">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Carousel.Item>
                        <Carousel.Item interval={10000000000}>
                            <ul className="courses-tray__list">
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg1">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg2">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg3">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg4">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Carousel.Item>
                        <Carousel.Item interval={10000000000}>
                            <ul className="courses-tray__list">
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg1">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg2">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg3">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg4">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Carousel.Item>
                    </Carousel>
                </Tab>
                <Tab eventKey="categories2" title={<h2>Certifications</h2>}>
                <Carousel className="">
                <Carousel.Item interval={10000000000}>
                            <ul className="courses-tray__list">
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg1">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg2">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg3">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg4">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Carousel.Item>
                        <Carousel.Item interval={10000000000}>
                            <ul className="courses-tray__list">
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg1">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg2">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg3">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg4">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Carousel.Item>
                        <Carousel.Item interval={10000000000}>
                            <ul className="courses-tray__list">
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg1">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg2">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg3">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                                <li className="col-sm-3">
                                    <div className="card">
                                        <div className="card__heading colbg4">
                                            <span className="flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating mt-5">
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="mode">Online</span>
                                            </div>
                                            <div className="card__duration-mode mt-10">
                                                Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                            </div>
                                            <Link className="view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Carousel.Item>
                    </Carousel>
                </Tab>
                
                </Tabs>
                <span className="pink-circle1" data-aos="fade-right"></span>
            </div>
        </div>
    </section>
  );
}
   
export default PopularCourses;