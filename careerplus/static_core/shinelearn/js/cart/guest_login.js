var login_button = document.getElementById("login_guests")

if(login_button != null){
login_button.addEventListener("click", guest_login);
}



function guest_login(){

              (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
              (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
              m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
              })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
              ga('create', 'UA-3537905-41', 'auto', {'name': 'a'});
              ga('a.send', 'pageview');
              ga('create', 'UA-3537905-41', 'auto');
              ga('send', 'pageview');
         function hitGA(){
            ga('send', 'event', 'Button Clicked', 'Buy Flow', 'Contimue as Guest');
          }



        var form=document.getElementById('login_form');
         hitGA();
        email= $("input[name=email]").val();
        if(email){

        var input = document.createElement("input");
        input.setAttribute("type", "hidden");
        input.setAttribute("name", "login_with");
        input.setAttribute("value", "login_guest")
        form.appendChild(input);
        form.submit();

        }

   }