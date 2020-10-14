window.Parsley.addValidator('filemimetypes', {
    requirementType: 'string',
    validateString: function (value, requirement, parsleyInstance) {
        var file = parsleyInstance.$element[0].files;

        if (file.length == 0) {
            return true;
        }

        console.log(file[0].type);

        var allowedMimeTypes = requirement.replace(/\s/g, "").split(',');
        return allowedMimeTypes.indexOf(file[0].type) !== -1;
    },
    messages: {
        en: 'Only .csv is allowed'
    }
});

