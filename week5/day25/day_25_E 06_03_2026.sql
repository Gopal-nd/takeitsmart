create table students(
id int not null,
name varchar(50) not null,
age int
);

insert into students values(101,'Arpita',29);
insert into students values(null,'priya',32);


create table user1
(
user_id int,
email_id varchar(20) unique
);

insert into user1 values(101,'abc@gmail.com'),
(102,'xyz@gmail.com');

insert into user1 values(103,'abc@gmail.com');




create table employee(
emp_id int primary key,
name varchar(20),
address varchar(10),
salary int
);

insert into employee values (1001,'Amit','Hyderabad',55000),
(1002,'shreya','Hyderabad',65000),
(1001,'jhoshna','Hyderabad',72000);

create table departments(
dept_id int primary key,
dept_name varchar(20)
);


create table employee(
emp_id int primary key,
name varchar(20),
dept_id int,
salary int,
location varchar(20),
foreign key(dept_id) references departments(dept_id)


insert into departments values(101,'IT'),
(102,'Hr');

insert into employee values(1,'rajini',101,35000,'hyderabad'),
(2,'shaziya',105,43000,'chennai');

create table students(
id int,
name varchar(20),
age int check (age>=18)
);

insert into students values(101,'shreya',15)


create table orders(
order_id int,
product_name varchar(20),
product_category varchar(20) default 'clothing'
);

insert into orders(order_id,product_name) values(101,'kurti');







