const express = require("express");
const app = express();

app.get("/products", (req, res) => {
  const products = [
    { id: 101, name: "Notebook", price: 3.5 },
    { id: 102, name: "Pencil", price: 1.2 },
    { id: 103, name: "Backpack", price: 25.0 }
  ];
  res.json(products);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Product service running on port ${PORT}`);
});
