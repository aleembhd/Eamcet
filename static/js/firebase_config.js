// Firebase configuration - Replace with your actual Firebase credentials
const firebaseConfig = {
    apiKey: "AIzaSyBUErVnCXAnMistt8iS0y7cgy9jNOIqd1I",
    authDomain: "eamcet-47898.firebaseapp.com",
    projectId: "eamcet-47898",
    storageBucket: "eamcet-47898.firebasestorage.app",
    messagingSenderId: "44535893771",
    appId: "1:44535893771:web:ac938f0bbb83d48ae65c0e",
    measurementId: "G-KPC366GQ6R"
  };
  

// Initialize Firebase
function initializeFirebase() {
  if (typeof firebase !== 'undefined') {
    firebase.initializeApp(firebaseConfig);
  } else {
    console.error('Firebase SDK not loaded');
  }
}

// Google Sign In function using popup only
function signInWithGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  
  // Add scopes to request
  provider.addScope('https://www.googleapis.com/auth/userinfo.email');
  provider.addScope('https://www.googleapis.com/auth/userinfo.profile');
  
  // Set custom parameters to force account selection dialog
  provider.setCustomParameters({
    prompt: 'select_account',
    select_account: 'true'
  });
  
  // Clear any existing cookie issues by first signing out
  // firebase.auth().signOut(); // Commented out this line
  
  // Use popup for authentication
  return firebase.auth()
    .signInWithPopup(provider)
    .then((result) => {
      const credential = result.credential;
      const token = credential.idToken;
      const user = result.user;
      
      return sendTokenToBackend(user.email, token, user.displayName);
    })
    .catch((error) => {
      console.error("Error during popup auth:", error);
      
      // Better handling for popup closed errors
      if (error.code === 'auth/popup-closed-by-user') {
        throw new Error('The authentication popup was closed. Please try again and ensure you complete the Google sign-in process before closing the popup.');
      }
      
      if (error.code === 'auth/popup-blocked') {
        throw new Error('The authentication popup was blocked by your browser. Please allow popups for this site and try again.');
      }
      
      return Promise.reject(error);
    });
}

// Send token to backend for verification and session creation
function sendTokenToBackend(email, token, displayName) {
  return fetch('/auth/callback/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email,
      token: token,
      name: displayName,
      action: 'google_login'
    }),
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      window.location.href = '/';
    } else {
      throw new Error(data.error || 'Authentication failed');
    }
  });
}

// Email/Password Sign In function
function signInWithEmailPassword(email, password) {
  return firebase.auth()
    .signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      return user.getIdToken().then(token => {
        return sendEmailPasswordTokenToBackend(user.email, token, user.displayName, 'login');
      });
    })
    .catch((error) => {
      console.error("Error during email/password auth:", error);
      
      if (error.code === 'auth/user-not-found') {
        throw new Error('No account found with this email. Please check your email or sign up.');
      }
      
      if (error.code === 'auth/wrong-password') {
        throw new Error('Incorrect password. Please try again.');
      }
      
      if (error.code === 'auth/invalid-email') {
        throw new Error('Invalid email format. Please enter a valid email address.');
      }
      
      if (error.code === 'auth/too-many-requests') {
        throw new Error('Too many failed login attempts. Please try again later or reset your password.');
      }
      
      return Promise.reject(error);
    });
}

// Email/Password Sign Up function
function createUserWithEmailPassword(email, password, name) {
  return firebase.auth()
    .createUserWithEmailAndPassword(email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      
      // Update the user profile with the provided name
      return user.updateProfile({
        displayName: name
      }).then(() => {
        return user.getIdToken().then(token => {
          return sendEmailPasswordTokenToBackend(user.email, token, name, 'signup');
        });
      });
    })
    .catch((error) => {
      console.error("Error during email/password signup:", error);
      
      if (error.code === 'auth/email-already-in-use') {
        throw new Error('An account with this email already exists. Please log in or use a different email.');
      }
      
      if (error.code === 'auth/invalid-email') {
        throw new Error('Invalid email format. Please enter a valid email address.');
      }
      
      if (error.code === 'auth/weak-password') {
        throw new Error('Password is too weak. Please use a stronger password.');
      }
      
      return Promise.reject(error);
    });
}

// Send email/password token to backend
function sendEmailPasswordTokenToBackend(email, token, displayName, action) {
  return fetch('/auth/callback/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email,
      token: token,
      name: displayName,
      action: 'firebase_email_auth',
      auth_type: action
    }),
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      window.location.href = '/';
    } else {
      throw new Error(data.error || 'Authentication failed');
    }
  });
}

// Password Reset function
function resetPassword(email) {
  return firebase.auth()
    .sendPasswordResetEmail(email)
    .then(() => {
      return Promise.resolve('Password reset email sent. Please check your inbox.');
    })
    .catch((error) => {
      console.error("Error sending reset email:", error);
      
      if (error.code === 'auth/user-not-found') {
        throw new Error('No account found with this email.');
      }
      
      if (error.code === 'auth/invalid-email') {
        throw new Error('Invalid email format. Please enter a valid email address.');
      }
      
      return Promise.reject(error);
    });
} 