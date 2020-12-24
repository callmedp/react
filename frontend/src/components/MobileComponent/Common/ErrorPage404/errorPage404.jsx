import React from "react";
import "./errorPage404.scss";
import { imageUrl, siteDomain } from "utils/domains";


const ErrorPage404 = () => {


  return (
    <main>
      <div className="container">
        <div className="row">
          <div className="col-sm-12 error-page mt-20">
            <figure>
                <img
                  height={265}
                  className="img-fluid"
                  src={`${imageUrl}mobile/error404.jpg`}
                  alt="404"
                />
          
            </figure>
            <strong className="mt-20">
              We could not find the page you are looking for
            </strong>
            <a href={siteDomain} className="btn-blue mt-20">
              Go to homepage
            </a>
          </div>
        </div>
      </div>
    </main>
  );
};

export default ErrorPage404;
