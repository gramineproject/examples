const db = connect("mongodb://localhost:27017/mydatabase");

const products = db.products;

products.drop()

products.insertMany([
  { item: "card", quantity: 25 },
  { item: "pen", quantity: 30 },
  { item: "lamp", quantity: 20 },
]);
