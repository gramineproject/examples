// Copyright (C) 2024 Gramine contributors
// SPDX-License-Identifier: BSD-3-Clause

const db = connect("mongodb://localhost:27017/mydatabase");

const products = db.products;

const cursor = products.find();
while (cursor.hasNext()) {
  const doc = cursor.next();
  printjson(doc);
}
