import React from 'react';
import Modal from 'react-modal';
import './helpModal.scss'


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
                    className="help-modal1"
                >
                    <form>
                        <div className="pr help-modal">
                            <React.Fragment>
                                <i onClick={this.closeModal}
                                    className='icon-close icon-close--position1' />
                                <h2>Login</h2>

                                <input className="mb-20" placeholder="Email" onChange={this.handleEmailInput} />

                                <input placeholder="Password" onChange={this.handlePasswordInput} />

                                {
                                    this.state.error &&
                                    <span className='pr'>{this.state.errorMessage}</span>

                                }
                                <button className="orange-button"
                                    type={'submit'} onClick={this.handleLogin}>Login
                            </button>
                            </React.Fragment>
                        </div>
                    </form>
                </Modal>
            </div>
        );
    }


}