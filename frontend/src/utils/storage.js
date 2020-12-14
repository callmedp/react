export const getLearningToken = () => {
    if (localStorage.getItem('learning_token')) return localStorage.getItem('learning_token');
    if (sessionStorage.getItem('learning_token')) return sessionStorage.getItem('learning_token');
    return '';
}


export const getAccessKey = () => {
    if (localStorage.getItem('access_key')) return localStorage.getItem('access_key');
    if (sessionStorage.getItem('access_key')) return sessionStorage.getItem('access_key');
    return '';
}