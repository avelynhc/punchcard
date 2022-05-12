import { useState, useRef, useContext } from "react";
import { useHistory } from "react-router-dom";
import AuthContext from "../../store/auth-context";

import classes from "./AuthForm.module.css";

const AuthForm = (props) => {
  const usernameInputRef = useRef();
  const passwordInputRef = useRef();
  const [isLogin, setIsLogin] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  const authCtx = useContext(AuthContext);
  const history = useHistory();

  const switchAuthModeHandler = () => {
    setIsLogin((prevState) => !prevState);
  };

  const submitHandler = (event) => {
    event.preventDefault();
    setMessage("");
    const enteredUsername = usernameInputRef.current.value;
    const enteredPassword = passwordInputRef.current.value;

    setIsLoading(true);
    let url;
    const BACKEND_API = "http://127.0.0.1:4000";
    if (isLogin) {
      url = `${BACKEND_API}/login`;
    } else {
      url = `${BACKEND_API}/register`;
    }
    fetch(url, {
      method: "POST",
      body: JSON.stringify({
        username: enteredUsername,
        password: enteredPassword,
        returnSecureToken: true,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        setIsLoading(false);
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("authentication failed!");
        }
      })
      .then((data) => {
        if (isLogin) {
          authCtx.login(data.access_token);
          history.replace("/");
        }
        else {
          setMessage(data.message)
          authCtx.register(data.access_token);
          history.replace("/auth");
        } 
      })
      .catch((err) => {
        console.log(err);
        setMessage(err.message);
      });
  };

  return (
    <section className={classes.auth}>
      <h1>{isLogin ? "Login" : "Sign Up"}</h1>
      <form onSubmit={submitHandler}>
        <div className={classes.control}>
          <label htmlFor="username">Your Username</label>
          <input
            type="username"
            id="username"
            ref={usernameInputRef}
            required
          />
        </div>
        <div className={classes.control}>
          <label htmlFor="password">Your Password</label>
          <input
            type="password"
            id="password"
            ref={passwordInputRef}
            required
          />
        </div>
        {message && <p className={classes.error}>{message}</p>}
        <div className={classes.actions}>
          {isLoading ? (
            <p>Sending request...</p>
          ) : (
            <>
              <button>{isLogin ? "Login" : "Create Account"}</button>
              <button
                type="button"
                className={classes.toggle}
                onClick={switchAuthModeHandler}
              >
                {isLogin
                  ? "Create a new account"
                  : "Login with existing account"}
              </button>
            </>
          )}
        </div>
      </form>
    </section>
  );
};

export default AuthForm;
