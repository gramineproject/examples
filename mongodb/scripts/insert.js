// Copyright (C) 2024 Gramine contributors
// SPDX-License-Identifier: BSD-3-Clause

const db = connect("mongodb://localhost:27017/mydatabase");

const products = db.products;

products.drop()

products.insertMany([
  { item: "card", quantity: 25 },
  { item: "pen", quantity: 30 },
  { item: "lamp", quantity: 20 },
]);
