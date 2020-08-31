export const getTitleCase = (firstName, lastName) => {
    const str = `${firstName} ${lastName}`;
    if (!str) return '';

    return str.replace(
        /\w\S*/g,
        function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}