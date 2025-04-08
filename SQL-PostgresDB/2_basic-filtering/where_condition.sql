-- WHERE condition

-- SELECT * FROM public.customer WHERE first_name = 'ADOM';

-- SELECT * FROM public.customer WHERE first_name = 'John' AND last_name = 'Doe';

/* Challenges:

How many payment were made by the customer with customer_id=100?

What is the last name of our customer with first name 'ERICA'

*/

SELECT COUNT(*) FROM public.payment WHERE customer_id = 100;

SELECT last_name FROM public.customer WHERE first_name = 'ERICA';






