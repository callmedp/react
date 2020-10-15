import React, {Component} from 'react';
import './App.css';
import AppRouter from './routes/index';

class App extends Component {

    render() {
        return ( 
        // < AppRouter / >
        <Link to={{ pathname: "https://resumestage.shine.com/resume-builder" }} />
    )
        ;
    }
}

export default App;
