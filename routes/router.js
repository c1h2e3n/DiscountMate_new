// router.js
const express = require("express");
const router = express.Router();
const passport = require("passport");
const crypto = require("crypto");
const async = require("async");
const nodemailer = require("nodemailer");
const puppeteer = require("puppeteer");
const Product = require("../models/Product");
const User = require("../models/usermodel");
const scrapeData = require("../utils/scrapeData");

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

    const existingProduct = await Product.findOne({ title: data.title });

    if (existingProduct) {
      console.log("Product with the same title already exists, skipping save.");
      res.render("scrapeResults", { product: existingProduct });
    } else {
      const product = new Product({
        title: data.title,
        price: data.price,
        discount: data.discount,
        productDetails: data.productDetails,
        imgUrl: data.imgUrl,
      });

      console.log(product);

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
    const products = await Product.find({ title: { $regex: searchTitle, $options: "i" } }).sort(sortCriteria);

    // Pass searchTitle and sort parameters to the view
    res.render("resultsproducts", { products: products, searchTitle: searchTitle, sort: req.query.sort });
  } catch (error) {
    console.log(error);
    res.status(500).send("Error searching and sorting products");
  }
});


router.get("/login", (req, res) => {
  res.render("login");
});

router.get("/signup", (req, res) => {
  res.render("signup");
});

router.post("/login", passport.authenticate("local", {
  successRedirect: "/index",
  failureRedirect: "/login",
  failureFlash: "Invalid email or password. Try Again!!!",
}));

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

// function isAuthenticatedUser(req, res, next) {
//   if (req.isAuthenticated()) {
//     return next();
//   }
//   req.flash("error_msg", "Please Login first to access this page.");
//   res.redirect("/login");
// }

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

//     // Check if a product with the same title already exists in the database
//     const existingProduct = await Product.findOne({ title: data.title });

//     if (existingProduct) {
//       console.log("Product with the same title already exists, skipping save.");
//       res.render("scrapeResults", { product: existingProduct });
//     } else {
//       // Save the scraped product into the database
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

//     // Search for products with exact title match in the database
//     const products = await Product.find({ title: searchTitle });

//     res.render("resultsproducts", { products: products });
//   } catch (error) {
//     console.log(error);
//     res.status(500).send("Error searching products");
//   }
// });

// router.get("/login", (req, res) => {
//   res.render("login");
// });

// router.get("/signup", (req, res) => {
//   res.render("signup");
// });

// router.post(
//   "/login",
//   passport.authenticate("local", {
//     successRedirect: "/index",
//     failureRedirect: "/login",
//     failureFlash: "Invalid email or password. Try Again!!!",
//   })
// );

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


// router.get("/searchAndSort", async (req, res) => {
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

//     res.render("resultsproducts", { products: products, searchTitle: searchTitle });
//   } catch (error) {
//     console.log(error);
//     res.status(500).send("Error searching and sorting products");
//   }
// });



// module.exports = router;
