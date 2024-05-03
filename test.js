const express = require("express");
const path = require("path");
const mongoose = require("mongoose");

// Initialize Express app
const app = express();

// Connect to MongoDB
mongoose
  .connect("mongodb://0.0.0.0:27017/discountmate")
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("Error connecting to MongoDB:", err));

// Set up view engine and static files
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");
app.use(express.static("public"));

// Middleware for parsing request body
app.use(express.urlencoded({ extended: true }));

// Routes
const router = require("./routes/router");
app.use("/", router);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send("Something broke!");
});

// Start server
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Server started at port ${PORT}.`);
});
