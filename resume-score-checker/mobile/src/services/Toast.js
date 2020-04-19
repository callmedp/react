import Swal from 'sweetalert2';

export const Toast = (type, message) => Swal.fire({
    icon : type,
    html : "<h3>" + message + '</h3>'
})
