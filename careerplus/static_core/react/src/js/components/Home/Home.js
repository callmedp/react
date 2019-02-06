import React from 'react';
import PropTypes from 'prop-types';

class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'name': '',
            'email': '',
            'phone': ''
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleNameChange = this.handleNameChange.bind(this);
        this.handleEmailChange = this.handleEmailChange.bind(this);
        this.handleNumberChange = this.handleNumberChange.bind(this);
    }

    handleSubmit(e) {
        e.preventDefault();
        const userDetails = {
            name: this.state.name,
            email: this.state.email,
            number: this.state.number
        }
            this.props.onFetchHomeDetail();
        // return fetch('http://127.0.0.1:8000/resume/api/v1/users/', {
        //     headers: {
        //         "Content-Type": "application/json"
        //     },
        //     method: 'POST',
        //     body: JSON.stringify(userDetails)
        // })
        //     .then(response => console.log(response))
    }

    handleNameChange(e) {
        this.setState({
            name: e.target.value
        })
    }

    handleEmailChange(e) {
        this.setState({
            email: e.target.value
        })

    }

    handleNumberChange(e) {
        this.setState({
            number: e.target.value
        })
    }


    render() {
        return (
            <div className={'App-header'}>
                <form onSubmit={this.handleSubmit}>
                    <div className={'Text-spacing'}>
                        <label>
                            Name:
                            <input type="text" value={this.state.name} onChange={this.handleNameChange}/>
                        </label>
                    </div>
                    <div className={'Text-spacing'}>
                        <label>
                            Email:
                            <input type="text" value={this.state.email} onChange={this.handleEmailChange}/>
                        </label>
                    </div>
                    <div className={'Text-spacing'}>
                        <label>
                            Number:
                            <input type="text" value={this.state.number} onChange={this.handleNumberChange}/>
                        </label>
                    </div>

                    <input type="submit" value="Submit"/>
                </form>
            </div>
        );
    }
}

Home.propTypes = {
    pinCode: PropTypes.number
}

export default Home;