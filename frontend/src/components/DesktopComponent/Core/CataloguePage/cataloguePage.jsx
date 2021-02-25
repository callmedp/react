import React, { useEffect,useState } from 'react';
import Header from '../../Common/Header/header';
import CatalogBanner from './Banner/banner';
import CoursesTray from './CoursesTray/coursesTray';
import AllCategories from './AllCategories/allCategories';
import ServicesForYou from './ServicesForYou/servicesForYou';
import RecentCourses from './RecentCourses/recentCourses';
import OurVendors from './OurVendors/ourVendors';
import Footer from 'components/DesktopComponent/Common/Footer/footer';
import './cataloguePage.scss';
import { CountryCode2 } from 'utils/storage.js';
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
import Loader from '../../Common/Loader/loader';

const CatalogPage = (props) => {
  const dispatch = useDispatch();
  const meta_tags = useSelector((store) =>
    store.allCategories.meta ? store.allCategories.meta : ""
  );
  let [loader,setLoader] = useState(false)


  const handleEffects = async () => {
    Aos.init({
      duration: 2000,
      once: true,
      offset: 10,
      anchorPlacement: "bottom-bottom",
    });

    if (!(window && window.config && window.config.isServerRendered)) {
      setLoader(true)
          new Promise((resolve, reject) =>
            dispatch(
              fetchRecentlyAddedCourses({
                payload: { code2: CountryCode2() },
                resolve,
                reject,
              })
            )
          );
          new Promise((resolve, reject) =>
            dispatch(
              fetchPopularServices({
                payload: { code2: CountryCode2() },
                resolve,
                reject,
              })
            )
          );
          new Promise((resolve, reject) =>
            dispatch(
              fetchTrendingCategories({
                payload: { code2: CountryCode2(), medium: 0 },
                resolve,
                reject,
              })
            )
          );
          new Promise((resolve, reject) =>
            dispatch(
              fetchAllCategoriesAndVendors({
                payload: { code2: CountryCode2(), medium: 0, num: 8 },
                resolve,
                reject,
              })
            )
          );
          setLoader(false)
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
    {loader?<Loader/>:''}
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
