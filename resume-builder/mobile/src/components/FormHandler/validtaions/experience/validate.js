const validate = values => {
    const errors = {}, listErrors = [], valuesLength = 4;
    values = (values && values.list) || [];

    values.forEach((obj, objIndex) => {
        const objErrors = {}
        objErrors.job_profile = !obj || !obj.job_profile || !obj.job_profile.label ? 'Required' : undefined;
        objErrors.company_name = !obj || !obj.company_name ? 'Required' : undefined;
        objErrors.start_date = !obj || !obj.start_date ? 'Required' : undefined;
        objErrors.end_date = !obj || (!obj.end_date && !obj.is_working) ? 'Required' : undefined;
        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        const errorElementsCount = Object.values(listErrors[0]).filter(el => el != undefined).length;
        if (listErrors.length <= 1 && errorElementsCount === valuesLength) {
            return errors;
        }
        errors.list = listErrors;
        return errors;
    }
    return errors;
};


export default validate;