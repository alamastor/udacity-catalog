function onSignIn(googleUser) {
  var id_token = googleUser.getAuthResponse().id_token;
  var backendUrl = document.querySelector('meta[name=login-url]').content;
  var csrf_token = document.querySelector('meta[name=csrf-token]').content
  var xhr = new XMLHttpRequest();
  xhr.open('POST', backendUrl);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (xhr.status === 204) {
      window.location.reload();
    } else {
      signOut();
    }
  };
  xhr.send('idtoken=' + id_token + '&_csrf_token=' + csrf_token);
  console.log('signing in')
}

function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    var logoutUrl = document.querySelector('meta[name=logout-url]').content;
    var csrf_token = document.querySelector('meta[name=csrf-token]').content
    var xhr = new XMLHttpRequest();
    xhr.open('POST', logoutUrl);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
      window.location.reload();
    };
    xhr.send('_csrf_token=' + csrf_token);
    window.location.reload();
    console.log('User signed out.');
  });
}

function onLoad() {
  gapi.load('auth2', function() {
    gapi.auth2.init();
  });
  var logoutButton = document.querySelector('button[id=logout-button]');
  logoutButton.addEventListener('click', signOut, false);
}

window.onload = onLoad;