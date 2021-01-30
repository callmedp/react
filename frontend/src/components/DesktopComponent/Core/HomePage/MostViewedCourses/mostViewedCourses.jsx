import React, {useState} from 'react';
import './mostViewedCourses.scss';
import { Link } from 'react-router-dom';
import { Tabs, Tab } from 'react-bootstrap';
   
function MostViewedCourses() {
    const [key, setKey] = useState('categories1');

    return(
        <section className="container-fluid" data-aos="fade-up">
        <div className="row">
            <div className="container"> 
                <div className="recent-courses mt-10 mb-10">
                    <h2 className="heading2 text-center">Most viewed courses</h2>
                    <Tabs
                    id="controlled-tab-example"
                    activeKey={key}
                    onSelect={(k) => setKey(k)}
                    className="category"
                    >
                        <Tab eventKey="categories1" title={<span>All</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                        <Tab eventKey="categories2" title={<span>Banking & Finance</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>2 Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                        <Tab eventKey="categories3" title={<span>Sales & Marketing</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>3 Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                        <Tab eventKey="categories4" title={<span>HR</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>4 Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                        <Tab eventKey="categories5" title={<span>Operations</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>5 Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                        <Tab eventKey="categories6" title={<span>Personal Development</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>6 Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                        <Tab eventKey="categories7" title={<span>IT</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>7 Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                        <Tab eventKey="categories8" title={<span>Mass comm</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>8 Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                        <Tab eventKey="categories9" title={<span>Management</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>9 Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                        <Tab eventKey="categories10" title={<span>LAW</span>}>
                            <ul className="recent-courses__list">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>10 Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
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
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Tab>
                    </Tabs>
                </div>
            </div>
        </div>
    </section>
    )
}
   
export default MostViewedCourses;