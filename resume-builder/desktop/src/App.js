import React, {Component} from 'react';
import AppRouter from './routes/index';
import  { Link } from 'react-router-dom'

class App extends Component {
    render() {
        return (

            // < AppRouter />
            // null
            // <Redirect to='https://resumestage.shine.com/resume-builder'  />
            <Link to={{ pathname: "https://resumestage.shine.com/resume-builder" }} />
    )
        ;
    }
}

export default App;
