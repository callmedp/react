import React, { useState, useEffect } from "react";
import { Route } from "react-router-dom";
import { siteDomain } from "utils/domains";
import { useDispatch } from "react-redux";
import {
  sessionAvailability,
  getCandidateInfo,
} from "store/Header/actions/index";
import Loader from "components/DesktopComponent/Common/Loader/loader";
import { fetchAlreadyLoggedInUser } from "store/Authentication/actions";

const RouteWithSubRoutes = (route) => {
  const dispatch = useDispatch();
  const [loader, setLoader] = useState(true);
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

  const isSessionAvailable = async () => {
    localStorage.clear();
    try {
      const session = await new Promise((resolve, reject) =>
        dispatch(sessionAvailability({ resolve, reject }))
      );
      if (session["result"] === false) {
        setLoader(false);
        return;
      }
      const candidateId = session["candidate_id"];
      await new Promise((resolve, reject) =>
        dispatch(getCandidateInfo({ candidateId, resolve, reject }))
      );
      setLoader(false);
    } catch (e) {
      console.log("error occured in fetching user session");
      setLoader(false);
    }
  };

  const fetchLogin = async () => {
    try {
      let res = await new Promise((resolve, reject) =>
        dispatch(
          fetchAlreadyLoggedInUser({
            resolve,
            reject,
            payload: { em: cookies },
          })
        )
        
      );
    } catch (e) {
      //
    }
    if (!(localStorage.getItem('isAuthenticated') === "true")) {
      const session = isSessionAvailable();
    } else {
      setLoader(false);
    }
  };

  useEffect(() => {
    fetchLogin();
  }, []);

  const renderComponent = (props) => {
    if(props.match.path === "/course/:func/:skill/:id/") {
      if(typeof document && document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) document.getElementsByClassName('chat-bot')[0].style.display = 'block';
    }
    else {
      if(typeof document && document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) document.getElementsByClassName('chat-bot')[0].style.display = 'none';
    }

    if (!!route.private) {
      if (localStorage.getItem("isAuthenticated") === "true") {
        return <route.component {...props} routes={route.routes} />;
      } else {
        window.location.replace(`${siteDomain}/login?next=${props.match.url}`);
      }
    } else {
      return <route.component {...props} routes={route.routes} />;
    }
  };

  return (
    <>
      {!!loader && <Loader />}
      {!loader ? (
        <Route path={route.path} exact={route.exact} render={renderComponent} />
      ) : null}
    </>
  );
};

export default RouteWithSubRoutes;
