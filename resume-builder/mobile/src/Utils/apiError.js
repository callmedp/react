import Swal from 'sweetalert2'

export const apiError = (isLogin) =>{
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000
      });
      
      Toast.fire({
        type: 'error',
        title: isLogin ? 'Redirecting to Login' : 'Something Went Wrong'
      })
}