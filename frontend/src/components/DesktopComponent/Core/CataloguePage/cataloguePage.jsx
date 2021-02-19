import React, { useEffect } from 'react';
import Header from '../../Common/Header/header';
import CatalogBanner from './Banner/banner';
import CoursesTray from './CoursesTray/coursesTray';
import AllCategories from './AllCategories/allCategories';
import ServicesForYou from './ServicesForYou/servicesForYou';
import RecentCourses from './RecentCourses/recentCourses';
import OurVendors from './OurVendors/ourVendors';
import Footer from 'components/DesktopComponent/Common/Footer/footer';
import './cataloguePage.scss';
import Aos from "aos";
// import "aos/dist/aos.css";
import { useDispatch, useSelector } from "react-redux";
import MetaContent from "../../Common/MetaContent/metaContent";
import {
  fetchRecentlyAddedCourses,
  fetchPopularServices,
  fetchAllCategoriesAndVendors,
  fetchTrendingCategories,
} from "store/CataloguePage/actions/index";
import { fetchAlreadyLoggedInUser } from "store/Authentication/actions/index";

const CatalogPage = (props) => {
  const dispatch = useDispatch();
  const meta_tags = useSelector((store) =>
    store.allCategories.meta ? store.allCategories.meta : ""
  );
  let cookies = "";
  try {
    cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, "_em_".length + 1) === "_em_=") {
        cookies = cookie.substring("_em_".length + 1);
        break;
      }
    }
  } catch (err) {
    cookies = "";
  }

  const handleEffects = async () => {
    Aos.init({
      duration: 2000,
      once: true,
      offset: 10,
      anchorPlacement: "bottom-bottom",
    });

    if (!(window && window.config && window.config.isServerRendered)) {
      let code2 = "IN";
      const result = await new Promise((resolve, reject) => {
        dispatch(
          fetchAlreadyLoggedInUser({
            resolve,
            reject,
            payload: { em: cookies },
          })
        );
      })
        .then((json) => {
          code2 = json["code2"];
        })
        .catch((err) => {
          code2 = "IN";
        })
        .finally(() => {
          new Promise((resolve, reject) =>
            dispatch(
              fetchRecentlyAddedCourses({
                payload: { code2: code2 },
                resolve,
                reject,
              })
            )
          );
          new Promise((resolve, reject) =>
            dispatch(
              fetchPopularServices({
                payload: { code2: code2 },
                resolve,
                reject,
              })
            )
          );
          new Promise((resolve, reject) =>
            dispatch(
              fetchTrendingCategories({
                payload: { code2: code2, medium: 0 },
                resolve,
                reject,
              })
            )
          );
          new Promise((resolve, reject) =>
            dispatch(
              fetchAllCategoriesAndVendors({
                payload: { code2: code2, medium: 0, num: 8 },
                resolve,
                reject,
              })
            )
          );
        });
    } else {
      // isServerRendered is needed to be deleted because when routing is done through react and not on the node,
      // above actions need to be dispatched.
      delete window.config?.isServerRendered;
    }
  };

  useEffect(() => {
    handleEffects();
  }, []);

  return (
    <>
      {meta_tags && <MetaContent meta_tags={meta_tags} />}
      <div>
        <Header placeHolder="Search course, assessment..." />
        <main>
          <CatalogBanner />
          <CoursesTray />
          <AllCategories />
          <ServicesForYou />
          <RecentCourses />
          <OurVendors />
        </main>
        <Footer />
      </div>
    </>
  );
};

export default CatalogPage;
