create table employees(
emp_id int,name varchar(20),department varchar(50),salary int,joining_date date);

insert into employees(emp_id,name,department,salary,joining_date) values
(101,'Rahul','IT',60000,'2023-01-10'),
(102,'Sneha','HR',45000,'2022-05-12'),
(103,'Arjun','IT',70000,'2021-07-15'),
(104,'Meghana','Finance',45000,'2023-02-20'),
(105,'Meena','Non IT',28000,'2023-03-17'),
(106,'Anushka','Finance',42000,'2022-01-23'),
(107,'Kiran','HR',37000,'2022-05-12');

select * from employees;

update employees
set salary=30000
where emp_id=105;

select * from employees where emp_id=106;

select name,department,salary from employees;

select * from employees where salary>=46000;


insert into employees values(108,'Shreya','Non IT',37000,'2022-04-10');

delete from employees where emp_id=108;

select * from employees

Alter table employees add email varchar(100);

update employees
set email='rahul@smart.com'
where emp_id=101;

update employees
set email='Sneha@smart.com'
where emp_id=102;

update employees
set email='Arjun@smart.com'
where emp_id=103;

update employees
set email='Meena@smart.com'
where emp_id=105;




update employees
set email='Anushka@smart.com'
where emp_id=106;

update employees
set email='Kiran@smart.com'
where emp_id=107;

update employees
set email='Meghana@smart.com'
where emp_id=104;

select * from employees;

select * from employees order by salary desc;

select * from employees where department='HR' and salary >=35000

select * from employees where department='HR' or salary = 55000


Alter table employees add bonus int;

update employees
set bonus=5000;

select bonus from employees

select * from employees
