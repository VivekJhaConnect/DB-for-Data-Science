/*
    USed to order result based on a column
*/
SELECT first_name, last_name FROM public.actor ORDER BY first_name;

/* 
    If you want to order by descending order 
*/
SELECT first_name, last_name FROM public.actor ORDER BY first_name DESC;

/* 
    If you want to order by ascending order 
*/
SELECT first_name, last_name FROM public.actor ORDER BY first_name ASC;

/* 
    If you want to order by multiple columns 
*/
SELECT first_name, last_name FROM public.actor ORDER BY first_name ASC, last_name DESC;

/* 
    If you want to order by multiple columns 
*/
SELECT first_name, last_name FROM public.actor ORDER BY first_name ASC, last_name DESC;

/*
    Given the books table, write a SQL query to:

    Select all columns from the books table.

    Order the results by the price in descending order.
*/

SELECT * FROM public.payment ORDER BY price DESC;

/* Challenges:

1. Write a SQL query to select all columns from the books table and order the results by the price in descending order.

*/

SELECT * FROM public.books ORDER BY price DESC;

/* Challenges:

You need to help the Marketing team to work more easily.

The marketing Manager asks you to order the customer list by the last name.

The went to start from 'Z' and work toward 'A'.

In case of the same last name the order should be based on the first name - also from Z to A.

*/

SELECT first_name, last_name, email FROM public.customer ORDER BY last_name DESC, first_name DESC;
