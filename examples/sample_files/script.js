/**
 * A simple JavaScript file for testing file type detection
 */

const greeting = "Hello, World!";

function greet(name = "World") {
    console.log(`Hello, ${name}!`);
}

// Arrow function example
const multiply = (a, b) => a * b;

// Object example
const person = {
    name: "John",
    age: 30,
    greet: function() {
        console.log(`Hi, I'm ${this.name}`);
    }
};

// Array operations
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);

// Main execution
if (typeof window === 'undefined') {
    // Node.js environment
    greet("Node.js");
    console.log("Doubled:", doubled);
    person.greet();
} else {
    // Browser environment
    greet("Browser");
}
