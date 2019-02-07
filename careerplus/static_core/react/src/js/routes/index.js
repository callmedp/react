import React from "react";
import {BrowserRouter as Router, Route, Link, Switch} from "react-router-dom";
import RegisterContainer from '../components/UserInfo/Register/register.jsx';
import DetailContainer from '../components/UserInfo/Detail/detail.jsx';
import Main from '../components/Main/main.jsx';

const AppRouter = () => (
    <Router>
        <Switch>
            <Route path='/resume-builder' exact component={Main}/>
            <Route path="/resume-builder/register" component={RegisterContainer}/>
            <Route path="/resume-builder/detail" component={DetailContainer}/>
        </Switch>

    </Router>
);

export default AppRouter;