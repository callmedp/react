const validate = values => {
    const errors = {}, listErrors = [], valuesLength = 2;
    values = (values && values.list) || [];
    values.forEach((obj, objIndex) => {
        const objErrors = {}
        objErrors.name_of_certification = !obj || !obj.name_of_certification ? 'Required' : undefined;
        objErrors.year_of_certification = !obj || !obj.year_of_certification ? 'Required' : undefined;
        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        const errorElementsCount = Object.values(listErrors[0]).filter(el =>el != undefined).length;
        if(listErrors.length <= 1 && errorElementsCount === valuesLength){
        return errors;
        }
        errors.list = listErrors;
        return errors;
    }
    return errors;

};


export default validate;