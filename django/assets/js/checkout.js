// This test secret API key is a placeholder. Don't include personal details in requests with this key.
// To see your test secret API key embedded in code samples, sign in to your Stripe account.
// You can also find your test secret API key at https://dashboard.stripe.com/test/apikeys.
// const stripe = Stripe("pk_test_51QUBXO03yFraxdaZ7VMAIyrZGUBQdyMQP49vvT5k07aCSfrBNZIemMPg50IDEodHmWb72TyHJKZeL4hP6Y9RLnBK00ulfKG1EC");

// initialize();

// // Create a Checkout Session
// async function initialize() {
//   const fetchClientSecret = async () => {
//     const response = await fetch("/checkout", {
//       method: "POST",
//       'X-CSRFToken':'P1sHKqEtzxz5lrnuQYNBQsFUCkARiVfh'
//     });
//     const { clientSecret } = await response.json();
//     return clientSecret;
//   };

//   const checkout = await stripe.initEmbeddedCheckout({
//     fetchClientSecret,
//   });

//   // Mount Checkout
//   checkout.mount('#checkout');
// }



const stripe = Stripe("pk_test_51QUBXO03yFraxdaZ7VMAIyrZGUBQdyMQP49vvT5k07aCSfrBNZIemMPg50IDEodHmWb72TyHJKZeL4hP6Y9RLnBK00ulfKG1EC");

// Initialize the Checkout Session
async function initialize() {
  // Get the CSRF token dynamically from the page
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  const fetchClientSecret = async () => {
    const response = await fetch("/checkout", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,  // Include CSRF token in headers
      },
    });

    // Check for successful response and parse the client secret
    const { clientSecret } = await response.json();
    return clientSecret;
  };

  const clientSecret = await fetchClientSecret();

  const checkout = await stripe.redirectToCheckout({
    sessionId: clientSecret,
  });

  checkout.then(function(result) {
    if (result.error) {
      alert(result.error.message);
    }
  });
}

// Start the checkout process
initialize();
