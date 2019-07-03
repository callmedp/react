import Swal from "sweetalert2";

export const LandingPageToast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
  heightAuto: false,
  padding: 20
});
