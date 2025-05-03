export default function initPayment(STRIPE_PUBLIC_KEY) {
    const stripe = Stripe(STRIPE_PUBLIC_KEY);
    const elements = stripe.elements();
    const cardElement = elements.create('card');
    cardElement.mount('#card-element');

    const form = document.getElementById('payment-form');
    const button = document.getElementById('submit-button');
    const paymentStatus = document.getElementById('payment-status');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        paymentStatus.textContent = 'Procesando...';
        paymentStatus.style.color = 'black';
        button.disabled = true;

        try {
            const amount = Math.round(document.getElementById('amount').value * 100);
            if (amount < 100) throw new Error('El monto debe ser al menos $1');

            const { paymentMethod, error } = await stripe.createPaymentMethod({
                type: 'card',
                card: cardElement,
            });
            if (error) {
                paymentStatus.textContent = error.message;
                return;
            }

            const response = await fetch('/create-payment-intent', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount })
            });

            const { clientSecret } = await response.json();
            const { paymentIntent, error: confirmError } = await stripe.confirmCardPayment(
                clientSecret,
                { payment_method: paymentMethod.id }
            );

            if (confirmError) {
                paymentStatus.textContent = confirmError.message;
                paymentStatus.style.color = 'red';
            } else if (paymentIntent.status === 'succeeded') {
                paymentStatus.textContent = 'Pago exitoso!';
                paymentStatus.style.color = 'green';
                alert('Pago exitoso!');
            }
        } catch (err) {
            paymentStatus.textContent = err.message;
            paymentStatus.style.color = 'red';
        } finally {
            button.disabled = false;
        }
    });
}
