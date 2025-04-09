-- WHERE condition

-- SELECT * FROM public.customer WHERE first_name = 'ADOM';

-- SELECT * FROM public.customer WHERE first_name = 'John' AND last_name = 'Doe';

/* Challenges:

How many payment were made by the customer with customer_id=100?

What is the last name of our customer with first name 'ERICA'

*/

-- SELECT COUNT(*) FROM public.payment WHERE customer_id = 100;

-- SELECT last_name FROM public.customer WHERE first_name = 'ERICA';

/* Challenges:

The inventory manager asks you how rentals have not been returned yet (return_date is null)

The sales manager asks you how for a list of all the payment_ids with an amount less than or equal to $2.
Include payment_id and the amount

*/

-- SELECT COUNT(*) FROM public.rental WHERE return_date IS NULL;

-- SELECT payment_id, amount FROM public.payment WHERE amount <= 2;


/*

WHERE with AND/OR

*/

SELECT * FROM public.payment WHERE customer_id = 100 OR customer_id = 101;

SELECT * FROM public.payment WHERE customer_id = 100 AND amount > 2;
