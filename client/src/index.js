// index.js

import React, {useState} from 'react';
import ReactDOM from 'react-dom/client';
import {
  BrowserRouter, Routes, Route
} from 'react-router-dom';
import { AppProvider } from './context.';
import './index.css';

import App from './components/App'

// import Home from './pages/Home/Home';
// import About from './pages/About/About';
// import ShowAll from './pages/ShowAll/ShowAll';
// import Login from './pages/Login/Login';
// import Signup from './pages/Signup/Signup';
// import SignUpForm from './components/SignUpForm/SignUpForm';
// import BookList from "./components/BookList/BookList";
// import BookDetails from "./components/BookDetails/BookDetails";
// import BookListAll from "./components/BookListAll/BookListAll";
// import MyLibrary from ".components/MyLibrary/MyLibrary";
// import Profile from ".components/Profile/Profile"
// import Login from ".components/Login/Login"
// import CreateAccount from ".components/CreateAccount/CreateAccount"
// import ErrorPage from ".components"
// const [user, setUser] = useState(null);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <AppProvider>
    <BrowserRouter>
    <App/>
      {/* <Routes>
        <Route path = "/" element = {<Home />}>
          <Route path = "about" element = {<About />} />
          <Route path = "login" element = {<Login onLogin={setUser} />} />
          <Route path = "book" element = {<BookList />} />
          <Route path = "/book/:id" element = {<BookDetails />} /> 
          <Route path = "showall" element = {<BookListAll />} />
          <Route path = "signup" element = {<SignUpForm />} />
        </Route>
      </Routes> */}
    </BrowserRouter>
  </AppProvider>
);

// moved all imports into routes.js 
// Then rewrote all the routes through here.

// import Home from "./pages/Home";
// import About from "./pages/About";
// import Login from "./pages/Login";
// import UserProfile from "./pages/UserProfile";
// import ErrorPage from "./pages/ErrorPage";
// import Search from "./pages/Search";
// import CreateAccount from "./pages/CreateAccount";
// import MyLibrary from "./pages/MyLibrary";
// import Friends from "./pages/Friends";
// import BookList from "./components/BookList/BookList";
// import BookDetails from "./components/BookDetails/BookDetails";

// This sequence used to work:
// const router = createBrowserRouter(routes);
// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
//   <AppProvider>
//     <RouterProvider router={router}/>
//   </AppProvider>
//   );

// THis used to work too:
// const container = document.getElementById("root");
// const root = createRoot(container);

// This never worked:
//root.render(
//     <Router>
//         <App />
//     </Router>
// );

// This, also never worked:
// ReactDOM.render(
//     <Router>
//         <App />
//     </Router>
//     /* document.getElementById('root') */
// );\

// Original Way:
// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
//     <BrowserRouter>
//       <Routes>
//         <Route path = "/" element = {<Home />}>
//           <Route path = "/about" element = {<About />} />
//           <Route path = "/book" element = {<BookList />} />
//           <Route path = "/book/:id" element = {<BookDetails />} />
//         </Route>
//       </Routes>
//     </BrowserRouter>
// );