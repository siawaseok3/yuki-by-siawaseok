// app.js
const express = require('express');
const cookieParser = require('cookie-parser');
const axios = require('axios');
const path = require('path');
const app = express();

const PORT = 3000;
const maxApiWaitTime = 8000;
const maxTime = 12000;
let apis = [];

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'templates'));

app.use(cookieParser());
app.use('/css', express.static('./css'));
app.use('/word', express.static('./blog'));
app.use(express.urlencoded({ extended: true }));

// API一覧取得
axios.get('https://raw.githubusercontent.com/siawaseok3/yuki-by-siawaseok/refs/heads/main/api_list.txt')
  .then(response => {
    apis = eval(response.data);
    console.log('API list loaded');
  })
  .catch(err => console.error('Failed to load API list', err));

function isJson(str) {
  try {
    JSON.parse(str);
    return true;
  } catch {
    return false;
  }
}

function checkCookie(cookieVal) {
  return cookieVal === 'True';
}

app.get('/', (req, res) => {
  const yuki = req.cookies.yuki;
  if (checkCookie(yuki)) {
    res.cookie('yuki', 'True', { maxAge: 7 * 24 * 60 * 60 * 1000 });
    res.render('home', { request: req });
  } else {
    res.redirect('/word');
  }
});

// 他のルートも順次追加していく

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
