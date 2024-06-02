const express = require('express');
const router = express.Router();
const User = require('../models/User');
const bcrypt = require('bcryptjs');

// Register Page
router.get('/register', (req, res) => {
    res.render('register');
});

// Register Handle
router.post('/register', async (req, res) => {
    const { username, password } = req.body;
    let errors = [];

    if (!username || !password) {
        errors.push({ msg: 'Please enter all fields' });
    }

    if (errors.length > 0) {
        res.render('register', { errors });
    } else {
        const user = await User.findOne({ username });
        if (user) {
            errors.push({ msg: 'User already exists' });
            res.render('register', { errors });
        } else {
            const newUser = new User({ username, password });
            await newUser.save();
            res.redirect('/login');
        }
    }
});

// Login Page
router.get('/login', (req, res) => {
    res.render('login');
});

// Login Handle
router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const user = await User.findOne({ username });

    if (user && await user.comparePassword(password)) {
        req.session.user = user;
        res.redirect('/');
    } else {
        res.render('login', { error: 'Invalid username or password' });
    }
});

// Logout Handle
router.get('/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/login');
});

module.exports = router;
