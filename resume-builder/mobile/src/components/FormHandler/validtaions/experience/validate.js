const validate = values => {
    const errors = {};
    if (!values.list || !values.list.length) {
        errors.list = {_error: 'Atleast One Education should be entered.'}
        return errors;
    }
    else{
        const listErrors = []
        values.list.forEach((obj, objIndex) => {
            const objErrors = {}
            objErrors.job_profile = !obj || !obj.job_profile ? 'Required' : undefined;
            objErrors.company_name = !obj || !obj.company_name ? 'Required' : undefined;
            objErrors.start_date = !obj || !obj.start_date ? 'Required' : undefined;
            objErrors.end_date = !obj || !obj.end_date ? 'Required' : undefined;
            listErrors[objIndex] = objErrors
        });
        if (listErrors.length) {
            errors.list = listErrors;
            console.log(errors)
            return errors;
        }
    }
    
};


export default validate;