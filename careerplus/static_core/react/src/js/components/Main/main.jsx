import React from "react";
import {Link} from 'react-router-dom';
import {Header} from '../Core/Header/header.jsx';
import {Footer} from '../Core/Footer/footer.jsx';


class Main extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <div className={'Main-page'}>
                    <Link to="/resume-builder/register">Create Your Resume</Link>
                </div>
            </div>
        );
    }
}

export default Main;