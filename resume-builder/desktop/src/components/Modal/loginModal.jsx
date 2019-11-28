import React from 'react';
import Modal from 'react-modal';
import './loginModal.scss'


if (typeof document !== 'undefined') {
    Modal.setAppElement(document.getElementById('react-app'));
}


export default class LoginModal extends React.Component {

    constructor(props) {
        super(props);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/';
        this.closeModal = this.closeModal.bind(this);
        this.handleEmailInput = this.handleEmailInput.bind(this);
        this.handlePasswordInput = this.handlePasswordInput.bind(this);
        this.handleLogin = this.handleLogin.bind(this);
        this.state = {
            email: "",
            password: "",
            error: false,
            errorMessage: ""
        }
    }

    handleEmailInput(event) {
        this.setState({
            "email": event.target.value
        })
    }

    handlePasswordInput(event) {
        this.setState({
            "password": event.target.value
        })
    }

    async handleLogin(event) {
        event.preventDefault();
        const { history } = this.props, templateId = localStorage.getItem('selected_template') || ''
        this.setState({
            "error": false,
            "errorMessage": ''
        })
        if (!this.state.email || !this.state.password) {
            let errorMessage = "";
            if (!this.state.email && !this.state.password) {
                errorMessage = "Email and Password is required."
            }
            else if (!this.state.email) {
                errorMessage = "Email is required."
            }
            else {
                errorMessage = "Password is required"
            }
            this.setState({
                'error': true,
                "errorMessage": errorMessage
            })
            return;
        }
        try {
            const result = await this.props.loginCandidate({ email: this.state.email, password: this.state.password }, history, true)
            if (templateId) {
                localStorage.setItem('selected_template', templateId);
            }
            this.closeModal();
            this.props.handleLoginSuccess()
        }
        catch (e) {
            this.setState({
                error: true,
                errorMessage: e.message
            })

        }
    }
    closeModal() {
        this.props.hideLoginModal();
        this.setState({
            "email": "",
            "password": "",
            "error": false,
            "errorMessage": ""
        })
    }

    render() {
        const { ui: { loginModal }, handleLoginSuccess } = this.props
        return (
            <div className="pr">
                <Modal
                    isOpen={loginModal}
                    onRequestClose={this.closeModal}
                    contentLabel="Help Modal"
                    className="login-modal"
                >
                    <form>
                        <div className="mt-10">
                            <React.Fragment>

                                <i onClick={this.closeModal}
                                    className='login-modal--close'>
                                </i>

                                <h2 className="mt-30">Login to build your resume</h2>

                                <p className="login-modal--error text-center">
                                        {
                                        this.state.error &&
                                        <span className='pr'>{this.state.errorMessage}</span>

                                    }
                                </p>
                                <ul className="login-modal__lists">
                                    <li className="login-modal__lists--item">
                                        <input className="login-modal__input" placeholder="Email" onChange={this.handleEmailInput} />
                                    </li>
                                    <li className="login-modal__lists--item">
                                        <input className="login-modal__input" placeholder="Password" type='password' onChange={this.handlePasswordInput} />
                                    </li>

                                    {/* <li className="login-modal__lists--item text-right">
                                        <a href="#">Forget Password</a>
                                    </li> */}
                                    

                                    <li className="login-modal__lists--item">
                                        <button className="orange-button w-100"
                                            type={'submit'} onClick={this.handleLogin}>Login
                                    </button>
                                    </li>
                                </ul>

                                <p className="mt-30 mb-30 text-center">Don’t have an account yet? <a href="/register/">Register Now</a></p>




                            </React.Fragment>
                        </div>
                    </form>
                </Modal>
            </div>
        );
    }


}