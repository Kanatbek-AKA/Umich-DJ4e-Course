// // On login.html  or here after successfully initiation login logout
// <script type="text/javascript">
//     var domain = 'https://apps.facebook.com/',
//         redirectURI = domain + {{ FACEBOOK_APP_NAMESPACE }} + '/';

//     window.top.location = 'https://www.facebook.com/dialog/oauth/' +
//                                 '?client_id={{ FACEBOOK_KEY }}' +
//                                 '&redirect_uri=' + encodeURIComponent(redirectURI) +
//                                 '&scope={{ FACEBOOK_EXTENDED_PERMISSIONS }}';
// </script>




// // Google +
// <script src="https://apis.google.com/js/api:client.js"></script>

// <script type="text/javascript">
//   gapi.load('auth2', function () {
//     var auth2;

//     auth2 = gapi.auth2.init({
//       client_id: "<PUT SOCIAL_AUTH_GOOGLE_PLUS_KEY HERE>",
//       scope: "<PUT BACKEND SCOPE HERE>"
//     });

//     auth2.then(function () {
//       var button = document.getElementById("google-plus-button");
//       console.log("User is signed-in in Google+ platform?", auth2.isSignedIn.get() ? "Yes" : "No");

//       auth2.attachClickHandler(button, {}, function (googleUser) {
//         // Send access-token to backend to finish the authenticate
//         // with your application

//         var authResponse = googleUser.getAuthResponse();
//         var $form;
//         var $input;

//         $form = $("<form>");
//         $form.attr("action", "/complete/google-plus");
//         $form.attr("method", "post");
//         $input = $("<input>");
//         $input.attr("name", "id_token");
//         $input.attr("value", authResponse.id_token);
//         $form.append($input);
//         // Add csrf-token if needed
//         $(document.body).append($form);
//         $form.submit();
//       });
//     });
//   });
// </script>