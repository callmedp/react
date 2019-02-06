import React from "react";

import {BrowserRouter as Router, Route, Link} from "react-router-dom";

import HomeContainer from '../containers/Home/home';

const Index = () => <h1> Home </h1>;
const About = () => <h1> About</h1>;
const User = () => <h1> User</h1>;

const AppRouter = () => (
    <Router>
        <div>
            <Route path="/resume-builder/" exact component={HomeContainer}/>
            <Route path="/resume-builder/about" component={About}/>
            <Route path="/resume-builder/users" component={User}/>
        </div>
    </Router>
);

export default AppRouter;