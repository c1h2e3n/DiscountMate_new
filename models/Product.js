const mongoose = require("mongoose");

const productSchema = new mongoose.Schema({
  title: String,
  price: String,
  discount: String,
  productDetails: String,
  imgUrl: String,
});

const Product = mongoose.model("Product", productSchema);

module.exports = Product;
