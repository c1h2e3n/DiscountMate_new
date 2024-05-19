const express = require("express");
const router = express.Router();
const puppeteer = require("puppeteer");
const Product = require("../models/Product");
const scrapeData = require("../utils/scrapeData");
const passport = require("passport");
const User = require("../models/usermodel");

// Function to ensure the user is authenticated
function isAuthenticatedUser(req, res, next) {
  if (req.isAuthenticated()) {
    return next();
  }
  req.flash("error_msg", "Please Login first to access this page.");
  res.redirect("/login");
}

// Existing routes and functionality
router.get("/scrape", (req, res) => {
  res.render("scrape");
});

router.get("/index", (req, res) => {
  res.render("index");
});

router.get("/scrapeResults", async function (req, res) {
  let url = req.query.search;
  let browser;

  try {
    browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    let data = await scrapeData(url, page);

    // Check if a product with the same title already exists in the database
    const existingProduct = await Product.findOne({ title: data.title });

    if (existingProduct) {
      console.log("Product with the same title already exists, skipping save.");
      res.render("scrapeResults", { product: existingProduct });
    } else {
      // Save the scraped product into the database
      const product = new Product({
        title: data.title,
        price: data.price,
        discount: data.discount,
        productDetails: data.productDetails,
        imgUrl: data.imgUrl,
      });
      await product.save();

      res.render("scrapeResults", { product: product });
    }
  } catch (error) {
    console.log(error);
    res.status(500).send("Error scraping data");
  } finally {
    if (browser) {
      await browser.close();
    }
  }
});

router.get("/resultsproducts", async (req, res) => {
  try {
    const searchTitle = req.query.title;
    let sortCriteria = {};

    // Check if sorting by price
    if (req.query.sort === "price") {
      sortCriteria.price = 1; // Ascending order
    }

    // Check if sorting by discount
    if (req.query.sort === "discount") {
      sortCriteria.discount = -1; // Descending order
    }

    // Search for products with matching title and apply sorting
    const products = await Product.find({
      title: { $regex: searchTitle, $options: "i" },
    }).sort(sortCriteria);

    // Pass searchTitle and sort parameters to the view
    res.render("resultsproducts", {
      products: products,
      searchTitle: searchTitle,
      sort: req.query.sort,
    });
  } catch (error) {
    console.log(error);
    res.status(500).send("Error searching and sorting products");
  }
});

router.get("/shoppingList", async (req, res) => {
  try {
    // Fetch the products from the database
    const products = await Product.find();

    // Calculate the total cost by summing up the prices of all products
    let totalCost = 0;
    products.forEach((product) => {
      totalCost += product.price;
    });

    // Render the shoppingList view and pass products and totalCost to it
    res.render("shoppingList", { products: products, totalCost: totalCost });
  } catch (error) {
    console.error("Error fetching products:", error);
    res.status(500).send("Error fetching products");
  }
});

router.post("/shoppingList", async (req, res) => {
  try {
    const selectedProductIds = req.body.selectedProducts;

    // If no products were selected, handle accordingly
    if (!selectedProductIds) {
      req.flash("error_msg", "No products were selected");
      return res.redirect("back");
    }

    // Store the selected product IDs in session
    req.session.shoppingList = selectedProductIds;

    // Find the selected products in the database
    const selectedProducts = await Product.find({
      _id: { $in: selectedProductIds },
    });

    // Calculate the total cost
    let totalCost = 0;
    selectedProducts.forEach((product) => {
      const priceString = product.price;
      const priceNumber = parseFloat(priceString.replace("$", ""));

      if (isNaN(priceNumber)) {
        console.error("Invalid price for product:", product);
      } else {
        totalCost += priceNumber;
      }
    });

    // Render the shopping list page with the selected products and total cost
    res.render("shoppingList", {
      products: selectedProducts,
      totalCost: totalCost.toFixed(2),
    });
  } catch (error) {
    console.log(error);
    res.status(500).send("Error generating shopping list");
  }
});

// Login and signup routes
router.get("/login", (req, res) => {
  res.render("login");
});

router.get("/signup", (req, res) => {
  res.render("signup");
});

router.post(
  "/login",
  passport.authenticate("local", {
    successRedirect: "/index",
    failureRedirect: "/login",
    failureFlash: "Invalid email or password. Try Again!!!",
  })
);

router.post("/signup", (req, res) => {
  let { name, email, password } = req.body;

  let userData = {
    name: name,
    email: email,
  };

  User.register(userData, password, (err, user) => {
    if (err) {
      req.flash("error_msg", "ERROR: " + err);
      res.redirect("/signup");
    }
    passport.authenticate("local")(req, res, () => {
      req.flash("success_msg", "Account created successfully");
      res.redirect("/login");
    });
  });
});

module.exports = router;

// previous code without shopping list (just sorting and searching)

// // router.js
// const express = require("express");
// const router = express.Router();
// const passport = require("passport");
// const crypto = require("crypto");
// const async = require("async");
// const nodemailer = require("nodemailer");
// const puppeteer = require("puppeteer");
// const Product = require("../models/Product");
// const User = require("../models/usermodel");
// const scrapeData = require("../utils/scrapeData");

// router.get("/scrape", (req, res) => {
//   res.render("scrape");
// });

// router.get("/index", (req, res) => {
//   res.render("index");
// });

// router.get("/scrapeResults", async function (req, res) {
//   let url = req.query.search;
//   let browser;

//   try {
//     browser = await puppeteer.launch({ headless: true });
//     const page = await browser.newPage();

//     let data = await scrapeData(url, page);

//     const existingProduct = await Product.findOne({ title: data.title });

//     if (existingProduct) {
//       console.log("Product with the same title already exists, skipping save.");
//       res.render("scrapeResults", { product: existingProduct });
//     } else {
//       const product = new Product({
//         title: data.title,
//         price: data.price,
//         discount: data.discount,
//         productDetails: data.productDetails,
//         imgUrl: data.imgUrl,
//       });

//       console.log(product);

//       await product.save();

//       res.render("scrapeResults", { product: product });
//     }
//   } catch (error) {
//     console.log(error);
//     res.status(500).send("Error scraping data");
//   } finally {
//     if (browser) {
//       await browser.close();
//     }
//   }
// });

// router.get("/resultsproducts", async (req, res) => {
//   try {
//     const searchTitle = req.query.title;
//     let sortCriteria = {};

//     // Check if sorting by price
//     if (req.query.sort === "price") {
//       sortCriteria.price = 1; // Ascending order
//     }

//     // Check if sorting by discount
//     if (req.query.sort === "discount") {
//       sortCriteria.discount = -1; // Descending order
//     }

//     // Search for products with matching title and apply sorting
//     const products = await Product.find({ title: { $regex: searchTitle, $options: "i" } }).sort(sortCriteria);

//     // Pass searchTitle and sort parameters to the view
//     res.render("resultsproducts", { products: products, searchTitle: searchTitle, sort: req.query.sort });
//   } catch (error) {
//     console.log(error);
//     res.status(500).send("Error searching and sorting products");
//   }
// });

// router.get("/login", (req, res) => {
//   res.render("login");
// });

// router.get("/signup", (req, res) => {
//   res.render("signup");
// });

// router.post("/login", passport.authenticate("local", {
//   successRedirect: "/index",
//   failureRedirect: "/login",
//   failureFlash: "Invalid email or password. Try Again!!!",
// }));

// router.post("/signup", (req, res) => {
//   let { name, email, password } = req.body;

//   let userData = {
//     name: name,
//     email: email,
//   };

//   User.register(userData, password, (err, user) => {
//     if (err) {
//       req.flash("error_msg", "ERROR: " + err);
//       res.redirect("/signup");
//     }
//     passport.authenticate("local")(req, res, () => {
//       req.flash("success_msg", "Account created successfully");
//       res.redirect("/login");
//     });
//   });
// });

// module.exports = router;
