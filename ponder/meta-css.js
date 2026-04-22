//variables vs constant
const PI = 3.14;
let radius = 3; //you can also declare it, let radius;, then initialize it later, radius = 3;

let area = radius * radius * PI; //could be a const, the area equation will never change.
console.log(area);

radius = 20;
area = radius * radius * PI;
console.log(area)

radius = 50;
area = radius * radius * PI;
console.log(area)

//type coersion
const one = 1;
const two = '2';

let result = one * two;
console.log(result); //js recognizes '2' as a number

result = one + two; //concatenate takes place over math
console.log(result)

result = one + Number(two);
console.log(result)


let course = "CSE131"; //global scope
let student;
if (true) {
    student = "John"
    console.log(course);  //works just fine, course is global
    console.log(student); //works just fine, it's being accessed within the block
}
console.log(course); //works fine, course is global
console.log(student); //does not work, can't access a block variable outside the block
                    