import React, { useState, useEffect } from "react";
import { slide as Menu } from "react-burger-menu";
import { Link } from "react-router-dom";
import { siteDomain, resumeShineSiteDomain } from "utils/domains";
import MenuNavHeader from "../MenuNavHeader/menuNavHeader";
import "./defaultMenuNav.scss";
import { useSelector, useDispatch } from "react-redux";
import { cartCount, fetchNavOffersAndTags } from "store/Header/actions/index";
import { initLoggedInZendesk } from "utils/zendeskIniti";
// import { trackUser } from 'store/Tracking/actions/index.js';
import {
  removeTrackingInfo,
  getCandidateInformation,
  getCandidateId,
} from "utils/storage.js";
import { MyGA } from "utils/ga.tracking.js";
import useLearningTracking from 'services/learningTracking';

const DefaultMenuNav = (props) => {
  const { setType, setOpen, open } = props;
  const dispatch = useDispatch();

  const { navTags } = useSelector((store) => store.header);
  const [candidateInfo, setCandidateInfo] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const sendLearningTracking = useLearningTracking();

  const fetchUserInfo = async () => {
    try {
      dispatch(cartCount());
      // const isSessionAvailable = await new Promise((resolve, reject) => dispatch(sessionAvailability({ resolve, reject })));

      if (getCandidateId()) {
        try {
          setIsLoggedIn(true);
          // const candidateId = isSessionAvailable['candidate_id']
          // const candidateInformation = await new Promise((resolve, reject) => dispatch(getCandidateInfo({candidateId, resolve, reject })))
          const candidateInformation = getCandidateInformation();
          initLoggedInZendesk(candidateInformation, true);
          setCandidateInfo(candidateInformation);
        } catch (e) {
          setIsLoggedIn(false);
          console.log("ERROR OCCURED", e);
        }
      } else {
        setIsLoggedIn(false);
      }
    } catch (e) {
      setIsLoggedIn(false);
      console.log("ERROR OCCURED", e);
    }
  };

  const eventTracking = () => {
    MyGA.SendEvent(
      "logo_click",
      "ln_logo_click",
      "ln_logo_click",
      "homepage",
      "",
      false,
      true
    );
    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_menu_nav_header_homepage_redirection`,
      pageTitle: props.pageTitle,
      sectionPlacement: 'header',
      eventCategory: 'menu_nav_header',
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
    })
    let product_tracking_mapping_id = localStorage.getItem(
      "productTrackingMappingId"
    );
    if (product_tracking_mapping_id == "10") {
      removeTrackingInfo();
    }
  };

  useEffect(() => {
    fetchUserInfo();
    dispatch(fetchNavOffersAndTags());
  }, []);

  const handleHeaderTracking = (category, event) => {
    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_${category}_${event}`,
      pageTitle: props.pageTitle,
      sectionPlacement: 'header',
      eventCategory: `default_menu_nav_${category}`,
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
    })
  }
  const aboutContactTracking = (name) => {
    MyGA.SendEvent(
      "homepage_footer",
      "ln_homepage_footer",
      "ln_homepage_footer_clicked",
      name,
      "",
      false,
      true
    )

    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_default_menu_nav_${name}`,
      pageTitle: props.pageTitle,
      sectionPlacement: 'header',
      eventCategory: 'default_menu_nav',
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
    })

  }

  const blogTracking = () => {
    MyGA.SendEvent('homepage_navigation', 'ln_homepage_navigation', 'ln_blog', 'ln_blog', '', false, true)
    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_default_menu_nav_blog`,
      pageTitle: props.pageTitle,
      sectionPlacement: 'header',
      eventCategory: 'default_menu_nav',
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
    })
  }

  const userIntentTracking = () => {
    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_default_menu_nav_user_intent`,
      pageTitle: props.pageTitle,
      sectionPlacement: 'header',
      eventCategory: 'default_menu_nav',
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
    })
  }

  const jobAssistanceTracking = (e) => {
    e.preventDefault();
    setType("jobAssistanceServices");
    MyGA.SendEvent(
      "homepage_navigation",
      "ln_homepage_navigation",
      "ln_job_assisstance",
      "ln_job_assisstance",
      "",
      false,
      true
    );

    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_default_menu_nav_job_assistance_services`,
      pageTitle: props.pageTitle,
      sectionPlacement: 'header',
      eventCategory: 'default_menu_nav',
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
    })
  }

  const allCoursesTracking = (e) => {
    e.preventDefault();
    setType("allCourses");
    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_default_menu_nav_all_courses`,
      pageTitle: props.pageTitle,
      sectionPlacement: 'header',
      eventCategory: 'default_menu_nav',
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
    })

  }

  const linkedinProfileTracking = () => {
    MyGA.SendEvent(
      "homepage_navigation",
      "ln_homepage_navigation",
      "ln_linked_profile_writing",
      "ln_linked_profile_writing",
      "",
      false,
      true
    )

    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_default_menu_nav_linkedin_profile_writing`,
      pageTitle: props.pageTitle,
      sectionPlacement: 'header',
      eventCategory: 'default_menu_nav',
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
    })

  }

  const freeResourcesTracking = (e) => {
    e.preventDefault();
    setType("freeResources");
    MyGA.SendEvent(
      "homepage_navigation",
      "ln_homepage_navigation",
      "ln_free_resources",
      "ln_free_resources",
      "",
      false,
      true
    );

    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_default_menu_nav_free_resources`,
      pageTitle: props.pageTitle,
      sectionPlacement: 'header',
      eventCategory: 'default_menu_nav',
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
    })
  }

  const navTracking = (name, index) => {

    sendLearningTracking({
      productId: '',
      event: `${props.pageTitle}_default_menu_nav_${name}`,
      pageTitle: props.pageTitle,
      sectionPlacement:'header',
      eventCategory: 'default_menu_nav',
      eventLabel: '',
      eventAction: 'click',
      algo: '',
      rank: '',
  })
  }


  return (
    <Menu
      className="navigation"
      width={"300px"}
      isOpen={open}
      onStateChange={(state) => setOpen(state.isOpen)}
    >
      <MenuNavHeader 
        isLoggedIn={isLoggedIn} 
        candidateInfo={candidateInfo} 
        sendLearningTracking={sendLearningTracking}
        pageTitle = {props.pageTitle}
      />
      <div className="m-menu-links">
        <Link
          className="menu-item"
          to="/"
          onClick={() => {
            setOpen((state) => !state);
            eventTracking();
          }}
        >
          <figure className="micon-home" /> Home
        </Link>
        <a
          href="/"
          className="menu-item"
          onClick={allCoursesTracking}
        >
          <figure className="micon-courses-services" /> All Courses{" "}
          <figure className="micon-arrow-menusm ml-auto" />
        </a>
        <a
          href="/"
          className="menu-item"
          onClick={jobAssistanceTracking}
        >
          <figure className="micon-resume-service" /> Job Assistance Services{" "}
          <figure className="micon-arrow-menusm ml-auto" />
        </a>
        <a
          href={`${resumeShineSiteDomain}/product/linkedin-profile-writing/entry-level-2/1926/`}
          className="menu-item"
          onClick={linkedinProfileTracking}
        >
          <figure className="micon-linkedin-service" /> Linkedin Profile Writing
        </a>
        <a
          href="/"
          className="menu-item"
          onClick={freeResourcesTracking}
        >
          <figure className="micon-free-resources" /> Free Resources{" "}
          <figure className="micon-arrow-menusm ml-auto" />
        </a>
        <a
          className="menu-item"
          href={`${siteDomain}/talenteconomy/`}
          onClick={blogTracking}
        >
          <figure className="micon-blog-services" /> Blog
        </a>
        <Link
          className="menu-item"
          onClick={userIntentTracking}
          to={"/user-intent"}
        >
          <figure className="micon-ui-cg" /> Career Guidance <small className="m-config-tag">NEW</small>
        </Link>
        {navTags?.length
          ? navTags.map((tag, index) => {
            return (
              <a key={index} className="menu-item" onClick={() => navTracking(tag.display_name, index)} href={tag.skill_page_url}>
                {" "}
                {tag?.display_name}&emsp;
              </a>
            );
          })
          : null}
        {isLoggedIn && (
          <ul className="dashboard-menu">
            <li>
              <a
                onClick={() => handleHeaderTracking('login', 'my_courses')}
                className="dashboard-menu--item"
                href={`${siteDomain}/dashboard/`}
              >
                <figure className="icon-dashboard" /> Dashboard
              </a>
              <ul className="dashboard-menu__submmenu">
                <li>
                  <a onClick={() => handleHeaderTracking('login', 'my_courses')} href={`${siteDomain}/dashboard/`}>My Courses</a>
                </li>
                <li>
                  <a onClick={() => handleHeaderTracking('login', 'my_services')} href={`${siteDomain}/dashboard/myservices`}>My Services</a>
                </li>
                <li>
                  <a onClick={() => handleHeaderTracking('login', 'my_orders')} href={`${siteDomain}/dashboard/myorder/`}>My Orders</a>
                </li>
                <li>
                  <a onClick={() => handleHeaderTracking('login', 'my_wallet')} href={`${siteDomain}/dashboard/mywallet/`}>My Wallet</a>
                </li>
              </ul>
            </li>
          </ul>
        )}
        <a
          className="menu-item"
          href={`${siteDomain}/about-us`}
          onClick={() => aboutContactTracking('about_us')}
        >
          About us
        </a>
        <a
          className="menu-item"
          href={`${siteDomain}/contact-us`}
          onClick={() => aboutContactTracking("contact_us")}
        >
          Contact us
        </a>
      </div>
    </Menu>
  );
};

export default DefaultMenuNav;
