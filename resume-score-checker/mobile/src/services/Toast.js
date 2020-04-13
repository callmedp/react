import Swal from 'sweetalert2';

export const Toast = (type, message) => Swal.fire({
    icon : type,
    title : message
})
