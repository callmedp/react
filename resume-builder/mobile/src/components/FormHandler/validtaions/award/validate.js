const validate = values => {
    const errors = {};
    if (!values.list || !values.list.length) {
        errors.list = {_error: 'Atleast One Language should be entered.'}
        return errors;
    }
    else{
        const listErrors = []
        values.list.forEach((obj, objIndex) => {
            const objErrors = {}
            if (!obj || !obj.title ||obj.title.length === 0) {
                objErrors.title = 'Required';
                listErrors[objIndex] = objErrors;
            }
            if (!obj || !obj.date ||obj.date.length === 0) {
                objErrors.date = 'Required';
                listErrors[objIndex] = objErrors;
            }
        });
        if (listErrors.length) {
            errors.list = listErrors;
            console.log(errors);
            return errors;
        }
    }
    
};


export default validate;